from fastapi import APIRouter
from app.services.ml_service import ml_service
from app.services.translation_service import translate_content
import math
import logging

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

# ── Comprehensive crop knowledge database ─────────────────────────────────────
CROP_DB = {
    "Rice": {
        "emoji": "🌾", "category": "Cereal",
        "season": "Kharif (Jun–Nov)", "duration": "110–150 days",
        "ideal_n": (80, 120), "ideal_p": (40, 60), "ideal_k": (40, 60),
        "ideal_ph": (5.5, 7.0), "ideal_temp": (22, 35), "ideal_rain": (150, 300),
        "market_price": "₹1940–₹2183/quintal (MSP 2024)",
        "water_need": "High (1200–1600 mm/season)",
        "soil_types": ["Alluvial", "Clay loam", "Loamy"],
        "companion_crops": ["Jute", "Maize"],
        "why_suitable": "Your soil nitrogen and moisture conditions match paddy requirements perfectly.",
        "tips": [
            "Use SRI (System of Rice Intensification) method to save 30% water.",
            "Transplant 15–20 day old seedlings for best yield.",
            "Apply Zinc Sulphate (25 kg/ha) if yellowing is seen."
        ],
        "expected_yield": "4–6 tonnes/hectare",
        "profit_estimate": "₹40,000–₹60,000/acre (after input costs)"
    },
    "Wheat": {
        "emoji": "🌿", "category": "Cereal",
        "season": "Rabi (Nov–Apr)", "duration": "120–150 days",
        "ideal_n": (80, 120), "ideal_p": (40, 60), "ideal_k": (40, 60),
        "ideal_ph": (6.0, 7.5), "ideal_temp": (10, 25), "ideal_rain": (75, 150),
        "market_price": "₹2275/quintal (MSP 2024)",
        "water_need": "Moderate (4–6 irrigations)",
        "soil_types": ["Loam", "Clay loam", "Black"],
        "companion_crops": ["Mustard", "Chickpea"],
        "why_suitable": "Cool-season crop, best in your current soil NPK ratio.",
        "tips": [
            "Sow between Nov 1–15 for maximum yield.",
            "Critical irrigation at Crown Root Initiation (21 days), Tillering, Flowering.",
            "Use certified disease-resistant varieties like HD-2967 or GW-496."
        ],
        "expected_yield": "3.5–5 tonnes/hectare",
        "profit_estimate": "₹35,000–₹50,000/acre"
    },
    "Maize": {
        "emoji": "🌽", "category": "Cereal",
        "season": "Kharif + Rabi", "duration": "80–110 days",
        "ideal_n": (100, 140), "ideal_p": (50, 70), "ideal_k": (50, 70),
        "ideal_ph": (5.8, 7.0), "ideal_temp": (20, 35), "ideal_rain": (100, 200),
        "market_price": "₹2090/quintal (MSP 2024)",
        "water_need": "Moderate-High",
        "soil_types": ["Well-drained Loam", "Sandy Loam"],
        "companion_crops": ["Beans", "Soybean"],
        "why_suitable": "High-N and K demand matches your soil profile.",
        "tips": [
            "Maintain plant spacing of 60×25 cm for optimal yield.",
            "Apply 1/3 N as basal, 1/3 at knee-height, 1/3 at tasseling.",
            "Detassel male rows (every 4th row) for seed production."
        ],
        "expected_yield": "5–8 tonnes/hectare",
        "profit_estimate": "₹55,000–₹80,000/acre"
    },
    "Cotton": {
        "emoji": "☁️", "category": "Cash Crop",
        "season": "Kharif (Apr–Nov)", "duration": "150–180 days",
        "ideal_n": (80, 120), "ideal_p": (40, 60), "ideal_k": (40, 60),
        "ideal_ph": (6.0, 8.0), "ideal_temp": (25, 38), "ideal_rain": (75, 125),
        "market_price": "₹6620/quintal (MSP 2024)",
        "water_need": "Moderate (Deficit-sensitive at boll formation)",
        "soil_types": ["Black/Regur", "Alluvial"],
        "companion_crops": ["Pigeonpea", "Groundnut"],
        "why_suitable": "Black soil pH and K levels strongly support cotton.",
        "tips": [
            "Use Bt Cotton varieties for bollworm resistance.",
            "Do NOT irrigate during boll opening; reduce water stress.",
            "Spray Mepiquat Chloride for height control in dense canopy."
        ],
        "expected_yield": "15–25 quintals seed cotton/acre",
        "profit_estimate": "₹60,000–₹1,00,000/acre"
    },
    "Sugarcane": {
        "emoji": "🎋", "category": "Cash Crop",
        "season": "Feb–Nov (12–18 months)", "duration": "12–18 months",
        "ideal_n": (100, 150), "ideal_p": (50, 80), "ideal_k": (60, 100),
        "ideal_ph": (6.0, 7.5), "ideal_temp": (25, 38), "ideal_rain": (150, 250),
        "market_price": "₹315/quintal Fair & Remunerative Price (2024)",
        "water_need": "Very High (1800–2000 mm/season)",
        "soil_types": ["Deep Loam", "Clay Loam", "Alluvial"],
        "companion_crops": ["Onion", "Potato (inter-crop)"],
        "why_suitable": "High K and humid conditions match sugarcane profile.",
        "tips": [
            "Use single-bud setts for 40% savings in seed cost.",
            "Practice Trash Mulching to conserve soil moisture.",
            "Trash burning is banned — Use as mulch or vermicompost material."
        ],
        "expected_yield": "60–80 tonnes/acre",
        "profit_estimate": "₹1,00,000–₹1,50,000/acre"
    },
    "Groundnut": {
        "emoji": "🥜", "category": "Oilseed",
        "season": "Kharif + Rabi", "duration": "90–130 days",
        "ideal_n": (15, 30), "ideal_p": (40, 60), "ideal_k": (50, 80),
        "ideal_ph": (6.0, 7.0), "ideal_temp": (25, 33), "ideal_rain": (60, 125),
        "market_price": "₹6377/quintal (MSP 2024)",
        "water_need": "Low-Moderate",
        "soil_types": ["Sandy Loam", "Red", "Laterite"],
        "companion_crops": ["Bajra", "Sorghum"],
        "why_suitable": "Low N is ideal — groundnut fixes own nitrogen via Rhizobium.",
        "tips": [
            "Treat seed with Rhizobium culture for natural nitrogen fixation.",
            "Do NOT apply excess N — it reduces pod formation.",
            "Apply Gypsum (200 kg/ha) at pegging stage for strong pods."
        ],
        "expected_yield": "15–20 quintals/acre",
        "profit_estimate": "₹45,000–₹70,000/acre"
    },
    "Chickpea": {
        "emoji": "🫘", "category": "Pulse",
        "season": "Rabi (Oct–Mar)", "duration": "90–120 days",
        "ideal_n": (20, 40), "ideal_p": (40, 60), "ideal_k": (20, 40),
        "ideal_ph": (6.0, 7.5), "ideal_temp": (15, 28), "ideal_rain": (60, 100),
        "market_price": "₹5440/quintal (MSP 2024)",
        "water_need": "Low (1–2 critical irrigations only)",
        "soil_types": ["Medium Black", "Loam", "Sandy Clay"],
        "companion_crops": ["Wheat", "Mustard"],
        "why_suitable": "Dry cool climate and phosphorus-rich soil matches chickpea.",
        "tips": [
            "Treat seed with Rhizobium + PSB for natural P and N uptake.",
            "Irrigation at pre-flowering (40 days) and pod filling (70 days) is critical.",
            "Use Desi varieties (Kabuli varieties for better market price)."
        ],
        "expected_yield": "8–12 quintals/acre",
        "profit_estimate": "₹25,000–₹40,000/acre"
    },
    "Mustard": {
        "emoji": "🌼", "category": "Oilseed",
        "season": "Rabi (Oct–Feb)", "duration": "90–120 days",
        "ideal_n": (60, 90), "ideal_p": (30, 50), "ideal_k": (30, 50),
        "ideal_ph": (6.5, 7.5), "ideal_temp": (10, 25), "ideal_rain": (60, 100),
        "market_price": "₹5050/quintal (MSP 2024)",
        "water_need": "Low-Moderate (2–4 irrigations)",
        "soil_types": ["Loam", "Sandy Loam", "Light Clay"],
        "companion_crops": ["Wheat", "Chickpea"],
        "why_suitable": "Cool weather and moderate N levels favor mustard growth.",
        "tips": [
            "Sow by Oct 15–Nov 1 for optimal yield.",
            "Apply Sulphur (30–40 kg/ha) for improved oil content.",
            "Top dressing of N at 30 days greatly boosts pods."
        ],
        "expected_yield": "8–12 quintals/acre",
        "profit_estimate": "₹30,000–₹45,000/acre"
    },
    "Tomato": {
        "emoji": "🍅", "category": "Vegetable",
        "season": "All seasons", "duration": "60–90 days",
        "ideal_n": (80, 120), "ideal_p": (60, 90), "ideal_k": (80, 120),
        "ideal_ph": (6.0, 7.0), "ideal_temp": (18, 30), "ideal_rain": (40, 80),
        "market_price": "₹800–₹2000/quintal (market varies)",
        "water_need": "Moderate (Drip preferred)",
        "soil_types": ["Sandy Loam", "Loam", "Red"],
        "companion_crops": ["Basil", "Marigold"],
        "why_suitable": "High K and balanced pH matches tomato fruit quality needs.",
        "tips": [
            "Use drip + mulch to reduce disease and save 40% water.",
            "No overhead irrigation — prevents fungal spread.",
            "Stake plants when 30cm tall. Apply potash for fruit size."
        ],
        "expected_yield": "15–25 tonnes/acre",
        "profit_estimate": "₹60,000–₹1,50,000/acre (highly variable)"
    },
    "Potato": {
        "emoji": "🥔", "category": "Vegetable",
        "season": "Rabi (Oct–Feb)", "duration": "70–120 days",
        "ideal_n": (100, 150), "ideal_p": (80, 120), "ideal_k": (100, 150),
        "ideal_ph": (5.5, 7.0), "ideal_temp": (10, 22), "ideal_rain": (50, 100),
        "market_price": "₹650–₹1200/quintal (market varies)",
        "water_need": "Moderate-High",
        "soil_types": ["Sandy Loam", "Loam", "Alluvial"],
        "companion_crops": ["Peas", "Beans"],
        "why_suitable": "High N+K demand and cool climate conditions favored.",
        "tips": [
            "Plant healthy certified seed tubers. Avoid cutting if possible.",
            "Critical irrigation: at tuber initiation (20–25 days post planting).",
            "Earthing up is essential at 30 and 50 days."
        ],
        "expected_yield": "10–15 tonnes/acre",
        "profit_estimate": "₹40,000–₹80,000/acre"
    }
}

# ── Irrigation method data ─────────────────────────────────────────────────────
IRRIGATION_METHODS = {
    "Drip": {
        "name": "Drip Irrigation", "emoji": "💧",
        "savings": "40–60% water saved",
        "best_for": "Vegetables, Fruits, Cotton",
        "cost": "₹30,000–₹60,000/acre (subsidy available)",
        "how": "Small emitters placed at root zone slowly release water.",
        "tip": "Run drip in morning (5–8 AM) for best absorption."
    },
    "Sprinkler": {
        "name": "Sprinkler Irrigation", "emoji": "🌧️",
        "savings": "25–40% water saved",
        "best_for": "Wheat, Groundnut, Potato",
        "cost": "₹10,000–₹25,000/acre (subsidy available)",
        "how": "Water sprayed in air like rain over the crop.",
        "tip": "Avoid running during afternoon heat (12–3 PM)."
    },
    "Flood": {
        "name": "Flood / Furrow Irrigation", "emoji": "🌊",
        "savings": "Traditional method",
        "best_for": "Rice, Sugarcane, Maize",
        "cost": "Lowest cost — just channel/bund labour",
        "how": "Water flooded into channels between crop rows.",
        "tip": "Use Alternate Wetting & Drying (AWD) for Rice to save 30% water."
    }
}

def score_crop(crop_data, n, p, k, ph, temp, rain):
    score = 100
    # N scoring
    n_lo, n_hi = crop_data["ideal_n"]
    if n < n_lo: score -= min(30, (n_lo - n) * 0.5)
    elif n > n_hi: score -= min(20, (n - n_hi) * 0.4)
    # P scoring
    p_lo, p_hi = crop_data["ideal_p"]
    if p < p_lo: score -= min(20, (p_lo - p) * 0.4)
    elif p > p_hi: score -= min(15, (p - p_hi) * 0.3)
    # K scoring
    k_lo, k_hi = crop_data["ideal_k"]
    if k < k_lo: score -= min(20, (k_lo - k) * 0.4)
    elif k > k_hi: score -= min(15, (k - k_hi) * 0.3)
    # pH scoring
    ph_lo, ph_hi = crop_data["ideal_ph"]
    if ph < ph_lo: score -= min(25, (ph_lo - ph) * 10)
    elif ph > ph_hi: score -= min(25, (ph - ph_hi) * 10)
    # Temp scoring
    t_lo, t_hi = crop_data["ideal_temp"]
    if temp < t_lo: score -= min(20, (t_lo - temp) * 2)
    elif temp > t_hi: score -= min(20, (temp - t_hi) * 2)
    # Rainfall
    r_lo, r_hi = crop_data["ideal_rain"]
    if rain < r_lo * 0.5:  score -= 15  # very dry
    elif rain > r_hi * 1.5: score -= 10  # too wet

    return max(0, round(score))


@router.post("/crop")
def crop_recommendation(data: dict, lang: str = "en"):
    try:
        n    = float(data.get("N", 80))
        p    = float(data.get("P", 40))
        k    = float(data.get("K", 40))
        ph   = float(data.get("ph", 6.5))
        temp = float(data.get("temperature", 28))
        rain = float(data.get("rainfall", 120))
        season_hint = data.get("season", "").lower()  # "kharif" or "rabi"

        # Score all crops
        scored = []
        for name, db in CROP_DB.items():
            sc = score_crop(db, n, p, k, ph, temp, rain)
            # Season filter bonus
            if season_hint and season_hint in db.get("season", "").lower():
                sc = min(100, sc + 10)
            scored.append((name, sc, db))

        scored.sort(key=lambda x: x[1], reverse=True)
        top_crop_name, top_score, top_db = scored[0]

        # Build top-5 alternatives
        alternatives = [
            {
                "name": n, "score": s,
                "emoji": db["emoji"], "season": db["season"],
                "category": db["category"]
            }
            for n, s, db in scored[1:6]
        ]

        # Determine what's missing/surplus
        deficits = []
        if n < top_db["ideal_n"][0]: deficits.append(f"Increase soil Nitrogen (current ~{n} kg/ha, need {top_db['ideal_n'][0]}+)")
        if p < top_db["ideal_p"][0]: deficits.append(f"Boost Phosphorus (current ~{p}, need {top_db['ideal_p'][0]}+)")
        if k < top_db["ideal_k"][0]: deficits.append(f"Add Potassium (current ~{k}, need {top_db['ideal_k'][0]}+)")

        res = {
            "crop": top_crop_name,
            "emoji": top_db["emoji"],
            "suitability_score": top_score,
            "category": top_db["category"],
            "season": top_db["season"],
            "duration": top_db["duration"],
            "market_price": top_db["market_price"],
            "expected_yield": top_db["expected_yield"],
            "profit_estimate": top_db["profit_estimate"],
            "water_need": top_db["water_need"],
            "soil_types": top_db["soil_types"],
            "why_suitable": top_db["why_suitable"],
            "farmer_tips": top_db["tips"],
            "soil_prep_needed": deficits,
            "companion_crops": top_db["companion_crops"],
            "alternatives": alternatives
        }
        return translate_content(res, lang)
    except Exception as e:
        return {"error": str(e)}


@router.post("/water")
def water_needs(data: dict, lang: str = "en"):
    try:
        crop   = data.get("crop", "Rice")
        area   = float(data.get("area", 1))
        temp   = float(data.get("temperature", 28))
        hum    = float(data.get("humidity", 60))
        rain   = float(data.get("monthly_rain", 0))
        stage  = data.get("crop_stage", "vegetative")  # sowing/vegetative/flowering/ripening
        soil   = data.get("soil_type", "Loam")

        # Base ET0 (Penman-Monteith simplified)
        et0 = 0.0023 * (temp + 17.8) * math.sqrt(max(0, temp + (hum / 10))) * 0.408
        et0 = max(2.0, et0)

        # Crop coefficient (Kc) by stage
        kc_table = {
            "sowing":     {"Rice": 1.05, "Wheat": 0.7, "Maize": 0.7, "Cotton": 0.35, "Sugarcane": 0.4,
                           "Groundnut": 0.5, "Tomato": 0.6, "Potato": 0.5, "default": 0.7},
            "vegetative": {"Rice": 1.2, "Wheat": 1.15, "Maize": 1.15, "Cotton": 1.1, "Sugarcane": 1.0,
                           "Groundnut": 0.95, "Tomato": 1.0, "Potato": 1.05, "default": 1.0},
            "flowering":  {"Rice": 1.35, "Wheat": 1.15, "Maize": 1.2, "Cotton": 1.2, "Sugarcane": 1.25,
                           "Groundnut": 1.15, "Tomato": 1.15, "Potato": 1.15, "default": 1.15},
            "ripening":   {"Rice": 1.0, "Wheat": 0.7, "Maize": 0.8, "Cotton": 0.8, "Sugarcane": 1.0,
                           "Groundnut": 0.65, "Tomato": 0.9, "Potato": 0.75, "default": 0.8},
        }
        kc_row = kc_table.get(stage, kc_table["vegetative"])
        kc = kc_row.get(crop, kc_row.get("default", 1.0))

        # Soil holding factor
        soil_factor = {"Clay": 0.85, "Black": 0.82, "Loam": 1.0, "Sandy Loam": 1.15,
                       "Red": 1.1, "Alluvial": 0.95}.get(soil, 1.0)

        etc = et0 * kc * soil_factor * 10_000  # mm/day → Liters/ha/day
        etc_per_acre = etc / 2.47
        rain_offset = (rain / 30) * 10_000 / 2.47  # mm month → L/acre/day

        daily_net = max(0, round(etc_per_acre - rain_offset))
        total_daily = round(daily_net * area)
        weekly = round(total_daily * 7)

        # Irrigation interval
        freq_days = {"Clay": 10, "Black": 10, "Loam": 7, "Sandy Loam": 5, "Red": 5, "Alluvial": 7}.get(soil, 7)
        per_irrigation = round(daily_net * freq_days)

        # Recommended method
        if daily_net < 1500 and crop not in ["Rice", "Sugarcane"]:
            method = "Drip"
        elif crop in ["Wheat", "Groundnut", "Potato"]:
            method = "Sprinkler"
        else:
            method = "Flood"

        meth_info = IRRIGATION_METHODS[method]

        # Critical water stages
        critical_stages = {
            "Rice":      ["Transplanting", "Tillering", "Panicle initiation", "Heading"],
            "Wheat":     ["Crown root (21 days)", "Tillering (45 days)", "Flowering (65 days)", "Grain fill (80 days)"],
            "Maize":     ["Knee-height", "Tasseling", "Silking", "Grain fill"],
            "Cotton":    ["Squaring", "Flowering", "Boll development"],
            "Sugarcane": ["Germination", "Tillering", "Grand growth"],
            "Groundnut": ["Pegging", "Pod development", "Pod fill"],
            "Tomato":    ["Transplanting", "Flowering", "Fruit set", "Fruit enlarge"],
            "Potato":    ["Tuber initiation", "Tuber bulking", "Maturity"],
        }

        saving_tips = [
            "🕐 Water early morning (5–8 AM) — avoids evaporation loss.",
            "🌱 Mulching with dry straw/leaves saves 25–35% water.",
            "📊 Use a soil finger/tensiometer test: if top 8 cm is dry → irrigate.",
            f"♻️ {meth_info['name']} can save {meth_info['savings']}.",
        ]
        if crop == "Rice":
            saving_tips.append("🔄 Practice AWD (Alternate Wetting & Drying): save up to 30% water in paddies.")

        res = {
            "crop": crop,
            "area_acres": area,
            "crop_stage": stage,
            "soil_type": soil,
            "daily_per_acre_liters": daily_net,
            "total_daily_liters": total_daily,
            "weekly_liters": weekly,
            "per_irrigation_liters": per_irrigation,
            "irrigation_frequency_days": freq_days,
            "recommended_method": meth_info["name"],
            "method_emoji": meth_info["emoji"],
            "method_how": meth_info["how"],
            "method_savings": meth_info["savings"],
            "method_cost": meth_info["cost"],
            "method_tip": meth_info["tip"],
            "critical_stages": critical_stages.get(crop, ["At sowing", "At flowering", "At grain fill"]),
            "water_saving_tips": saving_tips,
            "government_scheme": "PM-KUSUM / PMKSY Drip Subsidy available — check krishi.nic.in for your state."
        }
        return translate_content(res, lang)
    except Exception as e:
        return {"error": str(e)}


@router.post("/fertilizer")
def fertilizer_rx(data: dict, lang: str = "en"):
    try:
        crop  = data.get("crop", "Rice")
        n     = float(data.get("N", 60))
        p     = float(data.get("P", 30))
        k     = float(data.get("K", 30))
        ph    = float(data.get("ph", 6.5))
        area  = float(data.get("area", 1))
        stage = data.get("crop_stage", "basal")  # basal/vegetative/flowering/harvest
        soil  = data.get("soil_type", "Loam")
        org   = data.get("has_organic", False)  # has farmyard manure?

        # ── Target NPK per crop (kg/ha) ───────────────────────────────────────
        CROP_NPK = {
            "Rice":      {"N": 120, "P": 60, "K": 60},
            "Wheat":     {"N": 120, "P": 60, "K": 40},
            "Maize":     {"N": 150, "P": 75, "K": 75},
            "Cotton":    {"N": 120, "P": 60, "K": 60},
            "Sugarcane": {"N": 180, "P": 80, "K": 100},
            "Groundnut": {"N": 25,  "P": 50, "K": 75},
            "Chickpea":  {"N": 20,  "P": 60, "K": 20},
            "Mustard":   {"N": 80,  "P": 40, "K": 40},
            "Tomato":    {"N": 150, "P": 75, "K": 100},
            "Potato":    {"N": 150, "P": 90, "K": 120},
        }
        target = CROP_NPK.get(crop, {"N": 100, "P": 50, "K": 50})
        n_target = target["N"] / 2.47  # kg/ha per acre
        p_target = target["P"] / 2.47
        k_target = target["K"] / 2.47

        # Organic manure substitution (FYM replaces ~30% NPK budget)
        fym_note = ""
        if org:
            n_target *= 0.7
            p_target *= 0.7
            fym_note = "FYM @ 5 tonnes/acre applied (replaces 30% of chemical N–P requirement)."

        # Deficit calculation
        n_deficit = max(0, n_target - n)
        p_deficit = max(0, p_target - p)
        k_deficit = max(0, k_target - k)

        # Convert deficit to fertilizer quantity (for 1 acre)
        urea_kg   = round(n_deficit / 0.46 * area, 1)  # Urea is 46% N
        dap_kg    = round(p_deficit / 0.46 * area, 1)  # DAP is 46% P₂O₅
        mop_kg    = round(k_deficit / 0.60 * area, 1)  # MOP is 60% K₂O

        # pH based amendments
        ph_fix = []
        if ph < 5.5:
            ph_fix.append({"action": "Apply Agricultural Lime (Calcium Carbonate)",
                           "dose": "200–300 kg/acre", "when": "1 month before sowing",
                           "why": f"Your soil pH is {ph} (very acidic). Lime raises it to safe 6.0–6.5."})
        elif ph < 6.0:
            ph_fix.append({"action": "Apply Dolomite Lime",
                           "dose": "100–150 kg/acre", "when": "21 days before sowing",
                           "why": f"Soil pH {ph} is mildly acidic. Dolomite adds Ca + Mg + raises pH."})
        elif ph > 8.0:
            ph_fix.append({"action": "Apply Gypsum (Calcium Sulphate)",
                           "dose": "200 kg/acre", "when": "Before final plowing",
                           "why": f"Your soil pH {ph} is alkaline. Gypsum reduces pH and adds Sulphur."})
        elif ph > 7.5:
            ph_fix.append({"action": "Apply Sulphur 90%",
                           "dose": "10–15 kg/acre", "when": "Mix into topsoil",
                           "why": f"Soil pH {ph} is slightly alkaline — Sulphur will neutralize effectively."})

        # Application schedule
        schedule = []
        if stage in ["basal", "sowing"]:
            # Basal: P + K full dose + 1/3 N
            basal_n = round(urea_kg / 3)
            schedule.append({
                "phase": "🌱 Basal Dose (At Sowing / Field Preparation)",
                "fertilizers": [
                    {"name": "DAP (Di-Ammonium Phosphate)", "qty": f"{dap_kg} kg/acre", "note": "Full P dose at root zone"},
                    {"name": "MOP (Muriate of Potash)", "qty": f"{mop_kg} kg/acre", "note": "Full K at sowing"},
                    {"name": "Urea", "qty": f"{basal_n} kg/acre", "note": "1/3 N — mixed with soil before sowing"},
                ],
                "tip": "Mix all into top 6–8 inches of soil. Apply when soil is moist."
            })
            schedule.append({
                "phase": "🌿 First Top Dressing (25–30 days after sowing)",
                "fertilizers": [
                    {"name": "Urea", "qty": f"{round(urea_kg / 3)} kg/acre", "note": "1/3 N — ring placement near plants"},
                ],
                "tip": "Apply after a light irrigation or rain. Avoid applying on dry soil."
            })
            schedule.append({
                "phase": "🌸 Second Top Dressing (Before flowering / 50–60 days)",
                "fertilizers": [
                    {"name": "Urea", "qty": f"{round(urea_kg - 2 * round(urea_kg/3))} kg/acre",
                     "note": "Final 1/3 N — boosts grain/fruit size"},
                ],
                "tip": "Do NOT apply N after flowering — triggers leaf growth instead of yield."
            })
        else:
            schedule.append({
                "phase": f"🌿 Current Stage ({stage.title()}) — Top Dressing",
                "fertilizers": [
                    {"name": "Urea", "qty": f"{round(urea_kg * 0.4)} kg/acre", "note": "Foliar spray or soil application"},
                    {"name": "MOP", "qty": f"{round(mop_kg * 0.3)} kg/acre", "note": "Apply near root zone"},
                ],
                "tip": "Always water after applying granular fertilizer."
            })

        # Micronutrient recommendations
        micros = []
        if crop in ["Rice", "Wheat", "Maize"]:
            micros.append({"name": "Zinc Sulphate (21%)", "dose": "25 kg/ha (10 kg/acre)",
                           "tip": "If leaf yellowing or stunted growth appear — Zinc deficiency sign."})
        if ph > 7.0:
            micros.append({"name": "Iron Sulphate (FeSO₄)", "dose": "10 kg/acre spray (2%)",
                           "tip": "Alkaline soil locks out Iron. Foliar spray delivers it directly."})
        if crop in ["Cotton", "Mustard", "Groundnut"]:
            micros.append({"name": "Borax (Boron)", "dose": "1–2 kg/acre",
                           "tip": "Critical for flower setting and pod/boll formation."})

        # Cost estimate
        cost = round(urea_kg * 6.5 + dap_kg * 27 + mop_kg * 17, 0) * area

        # Government schemes
        subsidy_info = "Soil Health Card (SHC) from your nearest Krishi Vigyan Kendra gives FREE soil test. Apply at pmksy.gov.in for subsidized DAP/Urea."

        res = {
            "crop": crop,
            "area_acres": area,
            "soil_type": soil,
            "soil_ph": ph,
            "current_npk": {"N": n, "P": p, "K": k},
            "target_npk_per_acre": {"N": round(n_target, 1), "P": round(p_target, 1), "K": round(k_target, 1)},
            "deficit": {"N": round(n_deficit, 1), "P": round(p_deficit, 1), "K": round(k_deficit, 1)},
            "fertilizer_qty": {"Urea_kg": urea_kg, "DAP_kg": dap_kg, "MOP_kg": mop_kg},
            "schedule": schedule,
            "ph_correction": ph_fix,
            "micronutrients": micros,
            "organic_note": fym_note,
            "estimated_cost_inr": cost,
            "subsidy_info": subsidy_info,
            "golden_rules": [
                "💧 Always test soil before applying fertilizer — blindly adding NPK wastes money.",
                "🌧️ Never apply Urea before rain — it will wash off and cause water pollution.",
                "⏰ Morning application (6–9 AM) is most effective for foliar sprays.",
                "♻️ FYM + compost improves soil structure AND reduces chemical fertilizer need by 30%.",
                f"🏥 Get FREE Soil Health Card from your local KVK. Shows exact NPK, pH, micronutrients."
            ]
        }
        return translate_content(res, lang)
    except Exception as e:
        return {"error": str(e)}