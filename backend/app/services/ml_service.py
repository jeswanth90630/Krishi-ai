import os
import json
import joblib
import numpy as np
import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ── Fallback pest name map (numeric → human readable) ────────────────────────
PEST_NAME_FALLBACK = {
    "0":"Aphids","1":"Armyworm","2":"Thrips","3":"Whitefly",
    "4":"Stem Borer","5":"Brown Plant Hopper","6":"Mealybug","7":"Red Spider Mite",
    "8":"Fruit Borer","9":"Locust","10":"Leaf Folder","11":"Cutworm",
    "12":"Scale Insects","13":"Pink Bollworm","14":"Grasshopper","15":"Leaf Miner",
    "16":"Diamondback Moth","17":"Jassid/Leafhopper","18":"Termite","19":"Chilli Thrips",
    "20":"Green Stink Bug","21":"Tobacco Caterpillar","22":"Corn Rootworm",
    "23":"Colorado Potato Beetle","24":"Hessian Fly","25":"Fall Armyworm",
    "26":"Rice Hispa","27":"Gall Midge","28":"Thrips (Rice)","29":"Green Leafhopper",
    "30":"Bean Fly","31":"Tomato Leafminer","32":"Oriental Fruit Fly",
    "33":"Mediterranean Fruit Fly","34":"Sugarcane Pyrilla","35":"Shoot Bug",
    "36":"Sugarcane Top Borer","37":"Wooly Aphid","38":"Codling Moth",
    "39":"San Jose Scale","40":"Cotton Bollworm","41":"Tobacco Whitefly",
    "42":"Cotton Jassid","43":"Spotted Bollworm","44":"American Bollworm",
    "45":"Cotton Mealybug","46":"Sucking Pest","47":"Brinjal Fruit Borer",
    "48":"Brinjal Shoot Borer","49":"Epilachna Beetle","50":"Pea Aphid",
    "51":"Pea Moth","52":"Bean Stem Fly","53":"Legume Pod Borer",
    "54":"Pulse Beetle","55":"Pod Bug","56":"Hairy Caterpillar",
    "57":"Gram Pod Borer","58":"Groundnut Aphid","59":"Groundnut Leaf Miner",
    "60":"Groundnut Thrips","61":"Groundnut Jassid","62":"Mustard Aphid",
    "63":"Mustard Saw Fly","64":"Cabbage Butterfly","65":"Cabbage Aphid",
    "66":"Root Aphid","67":"Potato Thrips","68":"Potato Tuber Moth",
    "69":"Potato Jassid","70":"Mango Stem Borer","71":"Mango Fruit Fly",
    "72":"Mango Hopper","73":"Mango Mealybug","74":"Mango Shoot Gall Psyllid",
    "75":"Citrus Psylla","76":"Citrus Leafminer","77":"Citrus Aphid",
    "78":"Fruit Piercing Moth","79":"Onion Thrips","80":"Banana Aphid",
    "81":"Banana Stem Weevil","82":"Banana Skipper","83":"Coconut Rhinoceros Beetle",
    "84":"Red Palm Weevil","85":"Coconut Caterpillar","86":"Coconut Mite",
    "87":"Coffee Berry Borer","88":"Coffee Green Bug","89":"Tea Mosquito Bug",
    "90":"Red Spider Mite (Tea)","91":"Tea Thrips","92":"Grape Mealybug",
    "93":"Grape Berry Moth","94":"Grape Thrips","95":"Strawberry Spider Mite",
    "96":"Strawberry Crown Borer","97":"Soybean Pod Borer","98":"Soybean Aphid",
    "99":"Soybean Stem Fly","100":"Paddy Bug","101":"Rice Weevil"
}

# ─── Rich disease advisory database ───────────────────────────────────────────
DISEASE_ADVISORY = {
    "healthy": {
        "action": "No treatment needed. Maintain current irrigation and fertilization.",
        "severity": "None",
        "spread_risk": "None",
        "forecast": "Optimal yield expected this season."
    },
    "default_disease": {
        "action": "Apply targeted fungicide/bactericide. Isolate affected plants.",
        "severity": "Moderate",
        "spread_risk": "High",
        "forecast": "Without treatment, yield loss of 20-40% expected in 2 weeks."
    },
    "late_blight": {
        "action": "Apply Mancozeb or Metalaxyl immediately. Remove infected leaves.",
        "severity": "Critical",
        "spread_risk": "Very High",
        "forecast": "Can destroy entire crop within 10 days under humid conditions."
    },
    "early_blight": {
        "action": "Spray Chlorothalonil fungicide. Improve field drainage.",
        "severity": "Moderate",
        "spread_risk": "Medium",
        "forecast": "Manageable if treated within 5 days."
    },
    "bacterial_spot": {
        "action": "Apply copper-based bactericide spray. Avoid overhead watering.",
        "severity": "Moderate",
        "spread_risk": "High",
        "forecast": "Spreads rapidly in wet weather. Act within 48 hours."
    },
    "mosaic_virus": {
        "action": "Remove and destroy infected plants. Control aphid vectors.",
        "severity": "High",
        "spread_risk": "High",
        "forecast": "No chemical cure. Prevention through vector control is key."
    },
    "yellow_leaf_curl": {
        "action": "Control whitefly population with imidacloprid. Use reflective mulch.",
        "severity": "High",
        "spread_risk": "Very High",
        "forecast": "Can cause 100% loss if unchecked in dry season."
    },
}

def get_advisory(raw_class: str) -> dict:
    c = raw_class.lower()
    if "healthy" in c:
        return DISEASE_ADVISORY["healthy"]
    if "late_blight" in c:
        return DISEASE_ADVISORY["late_blight"]
    if "early_blight" in c:
        return DISEASE_ADVISORY["early_blight"]
    if "bacterial_spot" in c:
        return DISEASE_ADVISORY["bacterial_spot"]
    if "mosaic_virus" in c:
        return DISEASE_ADVISORY["mosaic_virus"]
    if "yellow_leaf_curl" in c:
        return DISEASE_ADVISORY["yellow_leaf_curl"]
    return DISEASE_ADVISORY["default_disease"]


# ── Crop requirements for Forecasting (N, P, K, pH, temp_min, temp_max, humidity_min, humidity_max, rainfall_min, rainfall_max)
CROP_DATA = {
    "Rice": {"N": 80, "P": 40, "K": 40, "ph": 6.0, "temp": (20, 35), "hum": (60, 95), "rain": (150, 300)},
    "Maize": {"N": 100, "P": 50, "K": 40, "ph": 6.5, "temp": (18, 30), "hum": (50, 80), "rain": (60, 110)},
    "Chickpea": {"N": 40, "P": 60, "K": 80, "ph": 7.0, "temp": (15, 25), "hum": (40, 60), "rain": (40, 70)},
    "Kidneybeans": {"N": 20, "P": 65, "K": 20, "ph": 6.8, "temp": (15, 25), "hum": (40, 60), "rain": (60, 100)},
    "Pigeonpeas": {"N": 20, "P": 70, "K": 20, "ph": 6.0, "temp": (18, 35), "hum": (45, 75), "rain": (90, 150)},
    "Mothbeans": {"N": 20, "P": 40, "K": 20, "ph": 6.5, "temp": (25, 35), "hum": (40, 65), "rain": (30, 80)},
    "Mungbean": {"N": 20, "P": 40, "K": 20, "ph": 6.7, "temp": (28, 35), "hum": (45, 60), "rain": (60, 90)},
    "Blackgram": {"N": 40, "P": 65, "K": 30, "ph": 7.5, "temp": (25, 35), "hum": (60, 70), "rain": (60, 100)},
    "Lentil": {"N": 20, "P": 60, "K": 20, "ph": 7.0, "temp": (18, 30), "hum": (40, 55), "rain": (40, 60)},
    "Pomegranate": {"N": 20, "P": 10, "K": 40, "ph": 6.4, "temp": (18, 25), "hum": (85, 95), "rain": (100, 120)},
    "Banana": {"N": 100, "P": 80, "K": 50, "ph": 6.0, "temp": (25, 30), "hum": (75, 85), "rain": (90, 110)},
    "Mango": {"N": 25, "P": 30, "K": 35, "ph": 5.8, "temp": (27, 35), "hum": (45, 55), "rain": (90, 100)},
    "Grapes": {"N": 30, "P": 130, "K": 20, "ph": 6.0, "temp": (10, 40), "hum": (80, 85), "rain": (65, 75)},
    "Watermelon": {"N": 100, "P": 20, "K": 50, "ph": 6.5, "temp": (25, 28), "hum": (80, 90), "rain": (40, 60)},
    "Muskmelon": {"N": 100, "P": 20, "K": 50, "ph": 6.5, "temp": (27, 30), "hum": (90, 95), "rain": (20, 30)},
    "Apple": {"N": 20, "P": 130, "K": 200, "ph": 6.0, "temp": (22, 24), "hum": (90, 95), "rain": (110, 130)},
    "Orange": {"N": 20, "P": 15, "K": 10, "ph": 7.5, "temp": (10, 45), "hum": (90, 95), "rain": (110, 120)},
    "Papaya": {"N": 45, "P": 50, "K": 30, "ph": 6.8, "temp": (23, 45), "hum": (90, 95), "rain": (240, 250)},
    "Coconut": {"N": 25, "P": 15, "K": 30, "ph": 6.0, "temp": (25, 30), "hum": (55, 65), "rain": (140, 230)},
    "Cotton": {"N": 120, "P": 45, "K": 20, "ph": 7.5, "temp": (22, 26), "hum": (75, 85), "rain": (60, 100)},
    "Jute": {"N": 80, "P": 40, "K": 40, "ph": 6.8, "temp": (23, 26), "hum": (70, 90), "rain": (150, 200)},
    "Coffee": {"N": 100, "P": 30, "K": 35, "ph": 6.8, "temp": (23, 28), "hum": (50, 65), "rain": (140, 200)}
}


def extract_soil_features(image_bytes):

    """Advanced feature extraction matching the training pipeline (153 features)."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img_bgr is None:
        return np.zeros(153)

    # 1. Color: HSV Histogram (32 bins * 3) = 96
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    h_hist = cv2.calcHist([hsv], [0], None, [32], [0, 180]).flatten()
    s_hist = cv2.calcHist([hsv], [1], None, [32], [0, 256]).flatten()
    v_hist = cv2.calcHist([hsv], [2], None, [32], [0, 256]).flatten()
    hsv_hist = np.concatenate([h_hist, s_hist, v_hist])
    hsv_hist = hsv_hist / (np.sum(hsv_hist) + 1e-7)

    # 2. Color: LAB Histogram (16 bins * 3) = 48
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l_hist = cv2.calcHist([lab], [0], None, [16], [0, 256]).flatten()
    a_hist = cv2.calcHist([lab], [1], None, [16], [0, 256]).flatten()
    b_hist = cv2.calcHist([lab], [2], None, [16], [0, 256]).flatten()
    lab_hist = np.concatenate([l_hist, a_hist, b_hist])
    lab_hist = lab_hist / (np.sum(lab_hist) + 1e-7)

    # 3. Stats: RGB Mean/Std (2 * 3) = 6
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    means = np.mean(rgb, axis=(0, 1)) / 255.0
    stds  = np.std(rgb, axis=(0, 1)) / 255.0
    stats = np.concatenate([means, stds])

    # 4. Texture: Gradient Magnitude Stats (3) = 3
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.sqrt(sobelx**2 + sobely**2)
    grad_stats = np.array([np.mean(mag), np.std(mag), np.max(mag)]) / 255.0

    return np.concatenate([hsv_hist, lab_hist, stats, grad_stats]).astype("float32")


class MLService:
    def __init__(self):
        self.base_dir  = os.getcwd()
        self.model_dir = os.path.join(self.base_dir, "models", "exports")
        self.models    = {}
        self.encoders  = {}
        self.class_meta      = {}   # plant disease class metadata
        self.pest_class_names = {}  # pest numeric -> human name
        self.pest_advisory   = {}   # pest advisory database
        self.soil_advisory   = {}   # rich soil advisory database

        # Standard transform for Torch models (Disease/Pest) - 224 for accuracy
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        self.load_models()

    def _load_mobilenetv3(self, pth_path, num_classes):
        """Load a MobileNetV3-Small model from saved .pth checkpoint."""
        model = models.mobilenet_v3_small(pretrained=False)
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.Hardswish(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        data = torch.load(pth_path, map_location=device)
        model.load_state_dict(data["state_dict"])
        model.eval()
        return model.to(device), data["classes"]

    def _load_mobilenetv2(self, pth_path, num_classes):
        """Load a MobileNetV2 model from saved .pth checkpoint (legacy)."""
        model = models.mobilenet_v2(pretrained=False)
        model.classifier[1] = nn.Sequential(
            nn.Linear(model.last_channel, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes)
        )
        data = torch.load(pth_path, map_location=device)
        model.load_state_dict(data["state_dict"])
        model.eval()
        return model.to(device), data["classes"]

    def load_models(self):
        # ── Crop (SKLearn) ────────────────────────────────────────────────────
        crop_path = os.path.join(self.model_dir, "crop_model.pkl")
        if os.path.exists(crop_path):
            self.models["crop"] = joblib.load(crop_path)
            print("MLService: ✔ Crop model (SKLearn)")

        # ── Disease (MobileNetV3 preferred, V2 fallback, SKLearn last) ────────
        disease_v3 = os.path.join(self.model_dir, "disease_model_torch.pth")
        disease_v2 = os.path.join(self.model_dir, "disease_model.pkl")
        label_json  = os.path.join(self.model_dir, "disease_classes.json")

        if os.path.exists(disease_v3):
            try:
                data_check = torch.load(disease_v3, map_location=device)
                n = len(data_check["classes"])
                try:
                    mdl, cls = self._load_mobilenetv3(disease_v3, n)
                    print(f"MLService: ✔ Plant Health model (MobileNetV3, {n} classes)")
                except Exception:
                    mdl, cls = self._load_mobilenetv2(disease_v3, n)
                    print(f"MLService: ✔ Plant Health model (MobileNetV2-compat, {n} classes)")
                self.models["disease_torch"] = mdl
                self.encoders["disease"]     = cls
            except Exception as e:
                print(f"MLService: ⚠ Failed to load disease torch model: {e}")

        elif os.path.exists(disease_v2):
            data = joblib.load(disease_v2)
            self.models["disease"] = data["model"]
            self.encoders["disease"] = data["classes"]
            print("MLService: ✔ Plant Health model (SKLearn baseline)")

        if os.path.exists(label_json):
            with open(label_json) as f:
                self.class_meta = json.load(f)
            print(f"MLService: ✔ Disease class metadata loaded ({len(self.class_meta)} classes)")

        # ── Soil ──────────────────────────────────────────────────────────────
        soil_path = os.path.join(self.model_dir, "soil_model.pkl")
        if os.path.exists(soil_path):
            data = joblib.load(soil_path)
            self.models["soil"] = data["model"]
            self.encoders["soil"] = data["classes"]
            print(f"MLService: ✔ Soil model (SKLearn, {len(data['classes'])} classes)")

        # ── Pest (MobileNetV3 preferred, SKLearn fallback) ────────────────────
        pest_torch_path   = os.path.join(self.model_dir, "pest_model_torch.pth")
        pest_pkl_path    = os.path.join(self.model_dir, "pest_model.pkl")
        pest_label_path  = os.path.join(self.model_dir, "pest_classes.json")
        pest_advisory_path = os.path.join(self.model_dir, "pest_advisory.json")

        if os.path.exists(pest_torch_path):
            try:
                data_check = torch.load(pest_torch_path, map_location=device)
                n = len(data_check["classes"])
                mdl, cls = self._load_mobilenetv3(pest_torch_path, n)
                self.models["pest_torch"] = mdl
                self.encoders["pest"] = cls
                print(f"MLService: ✔ Pest model (MobileNetV3, {n} classes)")
            except Exception as e:
                print(f"MLService: ⚠ Pest Torch load failed: {e}")

        elif os.path.exists(pest_pkl_path):
            data = joblib.load(pest_pkl_path)
            self.models["pest"] = data["model"]
            self.encoders["pest"] = data["classes"]
            print(f"MLService: ✔ Pest model (SKLearn, {len(data['classes'])} classes)")

        if os.path.exists(pest_label_path):
            with open(pest_label_path) as f:
                self.pest_class_names = json.load(f)
            print(f"MLService: ✔ Pest class names loaded ({len(self.pest_class_names)} entries)")

        if os.path.exists(pest_advisory_path):
            with open(pest_advisory_path) as f:
                self.pest_advisory = json.load(f)
            print(f"MLService: ✔ Pest advisory DB loaded ({len(self.pest_advisory)} entries)")

        # ── Soil Advisory ─────────────────────────────────────────────────────
        soil_adv_path = os.path.join(self.model_dir, "soil_advisory.json")
        if os.path.exists(soil_adv_path):
            with open(soil_adv_path) as f:
                self.soil_advisory = json.load(f)
            print(f"MLService: ✔ Soil advisory DB loaded ({len(self.soil_advisory)} soil types)")


    def _torch_infer(self, model_key, image_bytes):
        """Run inference with a Torch model, return (class_idx, confidence, all_probs)."""
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img_t = self.transform(img).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = self.models[model_key](img_t)
            probs   = torch.nn.functional.softmax(outputs[0], dim=0)
        idx  = torch.argmax(probs).item()
        conf = float(probs[idx])
        return idx, conf, probs.cpu().numpy()

    def _sklearn_infer(self, model_key, image_bytes):
        """Run inference with SKLearn model."""
        if model_key == "soil":
            # Advanced soil feature extraction
            features = extract_soil_features(image_bytes)
            probs = self.models["soil"].predict_proba([features])[0]
        else:
            # Legacy simple flatten (e.g. crop or baseline disease)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img   = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return 0, 0.0, []
            img   = cv2.resize(img, (32, 32)).flatten().astype("float32") / 255.0
            probs = self.models[model_key].predict_proba([img])[0]
            
        idx   = int(np.argmax(probs))
        return idx, float(probs[idx]), probs

    # ── Public API ─────────────────────────────────────────────────────────────
    def predict_crop(self, features):
        if "crop" not in self.models:
            return "Model not loaded"
        pred = self.models["crop"].predict(np.array([features]))
        return str(pred[0])

    def predict_disease(self, image_bytes):
        """Returns (raw_class, confidence, meta_dict)."""
        meta = {}
        if "disease_torch" in self.models:
            idx, conf, probs = self._torch_infer("disease_torch", image_bytes)
            raw_cls = self.encoders["disease"][idx]
            meta = self.class_meta.get(raw_cls, {})
            return raw_cls, conf, meta

        if "disease" in self.models:
            idx, conf, _ = self._sklearn_infer("disease", image_bytes)
            raw_cls = self.encoders["disease"][idx]
            meta = self.class_meta.get(raw_cls, {})
            return raw_cls, conf, meta

        return "Model not loaded", 0.0, {}

    def predict_soil(self, image_bytes):
        if "soil" in self.models:
            idx, conf, _ = self._sklearn_infer("soil", image_bytes)
            # Ensure class name is a standard string for JSON serialization
            soil_class = str(self.encoders["soil"][idx])
            advisory = self.soil_advisory.get(soil_class, {})
            return soil_class, conf, advisory
        return "Model not loaded", 0.0, {}

    def predict_pest(self, image_bytes):
        """Returns (pest_name, confidence, class_id_str)."""
        # Preferred: Torch MobileNetV3 model
        if "pest_torch" in self.models:
            idx, conf, _ = self._torch_infer("pest_torch", image_bytes)
            class_id = self.encoders["pest"][idx]  # e.g. "0", "42"
            # Look up human name from pest_class_names dict (loaded from JSON)
            pest_name = self.pest_class_names.get(class_id,
                            PEST_NAME_FALLBACK.get(class_id, f"Pest #{class_id}"))
            return pest_name, conf, class_id

        # Fallback: SKLearn
        if "pest" in self.models:
            idx, conf, _ = self._sklearn_infer("pest", image_bytes)
            class_id = str(self.encoders["pest"][idx])
            pest_name = self.pest_class_names.get(class_id,
                            PEST_NAME_FALLBACK.get(class_id, f"Pest #{class_id}"))
            return pest_name, conf, class_id

        return "Model not loaded", 0.0, "-1"


# Singleton
ml_service = MLService()
