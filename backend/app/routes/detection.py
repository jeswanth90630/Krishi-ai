from fastapi import APIRouter, UploadFile, File
import random
from app.services.ml_service import ml_service, get_advisory
from app.services.translation_service import translate_content

router = APIRouter(prefix="/api/detect", tags=["Detection"])

# ─── Confidence thresholds ─────────────────────────────────────────────────────
NOT_A_PLANT_THRESHOLD = 0.35

@router.post("/disease")
async def disease(lang: str = "en", file: UploadFile = File(...)):
    content = await file.read()
    raw_cls, confidence, meta = ml_service.predict_disease(content)

    if raw_cls == "Model not loaded":
        return {"error": "Plant Health Engine not initialized", "status": "error"}

    # ── Classification Layer 1: Not a plant (low confidence across all classes) ──
    if confidence < NOT_A_PLANT_THRESHOLD:
        return {
            "status": "⚠️ Not Recognized",
            "display_name": "Not a Recognizable Plant Leaf",
            "disease": "Unrecognized",
            "plant": "Unknown",
            "confidence": round(confidence * 100, 2),
            "is_healthy": False,
            "message": "The uploaded image does not match any known plant leaf in our database. Please upload a clear, close-up photo of a plant leaf.",
            "prediction": {
                "spread_risk": "N/A",
                "impact_forecast": "Image quality too low or not a recognized crop leaf.",
                "recommended_action": "Retake photo — ensure leaf fills frame, in natural light.",
                "next_checkpoint": "N/A"
            }
        }

    # ── Classification Layer 2: Healthy vs Diseased ────────────────────────────
    is_healthy = "healthy" in raw_cls.lower()

    parts      = raw_cls.split("___")
    plant_raw  = parts[0].replace(",_bell", " Bell Pepper")
    plant_name = plant_raw.replace("_", " ").strip()
    condition  = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Unknown"

    if meta:
        display_name = meta.get("display", f"{plant_name} — {condition}")
    else:
        display_name = f"{plant_name} — {'✅ Healthy' if is_healthy else '⚠️ ' + condition}"

    advisory = get_advisory(raw_cls)

    res = {
        "status": "✅ Healthy Plant" if is_healthy else "🔴 Disease Detected",
        "display_name": display_name,
        "disease": condition,
        "plant": plant_name,
        "raw_class": raw_cls,
        "confidence": round(confidence * 100, 2),
        "is_healthy": is_healthy,
        "prediction": {
            "spread_risk": advisory["spread_risk"],
            "impact_forecast": advisory["forecast"],
            "recommended_action": advisory["action"],
            "next_checkpoint": "No follow-up needed" if is_healthy else "Re-scan in 3 days after treatment"
        }
    }
    return translate_content(res, lang)


@router.post("/pest")
async def pest(lang: str = "en", file: UploadFile = File(...)):
    content = await file.read()
    pest_name, confidence, class_id = ml_service.predict_pest(content)

    if pest_name == "Model not loaded":
        return {"error": "Pest model not loaded"}

    if confidence < 0.20:
        return {
            "pest": "Unrecognized",
            "confidence": round(confidence * 100, 2),
            "status": "⚠️ Not Recognized",
            "message": "Image not matched to any known pest. Upload a clear, close-up pest photo.",
            "prediction": {
                "infestation_level": "Unknown",
                "strategic_recommendation": "Retake photo with better lighting and focus on the pest.",
                "outbreak_probability": "N/A",
                "forecast": "N/A",
                "endangered_crops": [],
                "chemical_control": "N/A",
                "biological_control": "N/A",
                "organic_control": "N/A",
                "season": "N/A",
                "spread_velocity": "N/A"
            }
        }

    advisory = ml_service.pest_advisory.get(class_id, {})

    endangered_crops = advisory.get("endangered_crops", ["Multiple crops"])
    control          = advisory.get("control", {})
    threat_level     = advisory.get("threat_level", "High")
    damage_desc      = advisory.get("damage", "Causes significant crop damage")
    symptoms         = advisory.get("symptoms", "Visual inspection required")
    season           = advisory.get("season", "Active during growing season")
    spread_velocity  = advisory.get("spread_velocity", "Moderate")
    scientific       = advisory.get("scientific", "")

    infestation_level = "🔴 Critical" if threat_level in ["Critical", "Devastating"] else \
                        "🟠 High Risk" if threat_level == "High" else "🟡 Moderate Risk"

    res = {
        "pest": pest_name,
        "scientific_name": scientific,
        "confidence": round(confidence * 100, 2),
        "class_id": class_id,
        "status": f"🐛 {pest_name} Detected",
        "threat_level": threat_level,
        "prediction": {
            "infestation_level": infestation_level,
            "strategic_recommendation": control.get("chemical", "Apply appropriate pesticide immediately"),
            "biological_control": control.get("biological", "Use natural predators"),
            "organic_control": control.get("organic", "Neem oil spray"),
            "cultural_control": control.get("cultural", "Crop rotation and field hygiene"),
            "outbreak_probability": "Very High" if threat_level in ["Critical", "Devastating"] else "Moderate",
            "forecast": f"Active season: {season}. Spread: {spread_velocity}.",
            "endangered_crops": endangered_crops,
            "damage_description": damage_desc,
            "symptoms": symptoms,
            "season": season,
            "spread_velocity": spread_velocity
        }
    }
    return translate_content(res, lang)


@router.post("/soil")
async def soil(lang: str = "en", file: UploadFile = File(...)):
    content = await file.read()
    pred, confidence, advisory = ml_service.predict_soil(content)

    if pred == "Model not loaded":
        return {"error": "Soil model not loaded"}

    soil_name = pred.replace("_Soil", "").replace("_", " ").strip()

    # ── Pull rich data from advisory database ─────────────────────────────────
    display_name       = advisory.get("display_name", soil_name)
    ph_range           = advisory.get("ph_range", "6.0 – 7.5")
    texture            = advisory.get("texture", "Loamy")
    organic_matter     = advisory.get("organic_matter", "Moderate")
    water_retention    = advisory.get("water_retention", "Moderate")
    drainage           = advisory.get("drainage", "Moderate")
    characteristics    = advisory.get("characteristics", "")
    health_verdict     = advisory.get("soil_health_verdict", f"{soil_name} soil analysis complete.")
    key_deficiencies   = advisory.get("key_deficiencies", [])
    irrigation_info    = advisory.get("irrigation", "As needed")
    productivity_index = advisory.get("productivity_index", 70)
    annual_yield_pot   = advisory.get("annual_yield_potential", "Moderate")
    color_hex          = advisory.get("color", "#8B7355")

    # Recommended crops
    crops_raw  = advisory.get("recommended_crops", [])
    crop_names = ", ".join(c["name"] for c in crops_raw[:6]) if crops_raw else "Consult agronomist"
    top_crops  = [
        {
            "name":        c["name"],
            "season":      c.get("season", "—"),
            "yield":       c.get("yield", "—"),
            "suitability": c.get("suitability", 80)
        }
        for c in crops_raw[:6]
    ]

    # Fertilizer plan
    fert           = advisory.get("fertilizer_plan", {})
    base_fert      = fert.get("base_application", {})
    top_dress      = fert.get("top_dressing", {})
    organic_inputs = fert.get("organic", {})
    micronutrients = fert.get("micronutrients", {})
    fert_schedule  = fert.get("schedule", "Apply as per soil test.")

    # pH management
    ph_mgmt     = advisory.get("ph_management", {})
    ideal_ph    = ph_mgmt.get("ideal_ph", 6.5)
    if_acidic   = ph_mgmt.get("if_acidic", "Apply agricultural lime.")
    if_alkaline = ph_mgmt.get("if_alkaline", "Apply gypsum.")

    conf_pct = round(confidence * 100, 2)

    res = {
        "soil":         soil_name,
        "display_name": display_name,
        "confidence":   conf_pct,
        "soil_color":   color_hex,
        "profile": {
            "ph_range":         ph_range,
            "ideal_ph":         ideal_ph,
            "texture":          texture,
            "organic_matter":   organic_matter,
            "water_retention":  water_retention,
            "drainage":         drainage,
            "key_deficiencies": key_deficiencies,
            "characteristics":  characteristics
        },
        "crops": {
            "top_list":   top_crops,
            "crop_names": crop_names,
            "irrigation": irrigation_info
        },
        "fertilizer": {
            "base_application": base_fert,
            "top_dressing":     top_dress,
            "organic_inputs":   organic_inputs,
            "micronutrients":   micronutrients,
            "schedule":         fert_schedule
        },
        "ph_management": {
            "ideal_ph":    ideal_ph,
            "if_acidic":   if_acidic,
            "if_alkaline": if_alkaline
        },
        "verdict": {
            "health_verdict":     health_verdict,
            "productivity_index": productivity_index,
            "annual_yield":       annual_yield_pot,
            "suitability_index":  f"{min(conf_pct + 10, 98):.1f}%",
            "status": "🟢 Healthy Soil Profile" if productivity_index >= 80 else
                      "🟡 Moderate Fertility" if productivity_index >= 60 else
                      "🔴 Low Fertility — Soil Amendment Required"
        }
    }
    return translate_content(res, lang)


@router.post("/severity")
async def severity():
    return {"severity": random.choice(["Low", "Medium", "High"])}