from fastapi import APIRouter
import random

router = APIRouter(prefix="/api/fertilizer", tags=["Fertilizer"])

@router.post("/recommend")
def recommend(data: dict):
    # Logic based on NPK and Crop
    crop = data.get("crop", "Rice")
    n = float(data.get("N", 0))
    p = float(data.get("P", 0))
    k = float(data.get("K", 0))
    
    recommendations = []
    
    if n < 50:
        recommendations.append({"type": "Urea", "amount": "50kg/acre", "timing": "Basal dose"})
    if p < 30:
        recommendations.append({"type": "DAP", "amount": "30kg/acre", "timing": "At sowing"})
    if k < 30:
        recommendations.append({"type": "MOP", "amount": "20kg/acre", "timing": "Vegetative phase"})
        
    if not recommendations:
        recommendations.append({"type": "Organic Manure", "amount": "2 tons/acre", "timing": "Soil preparation"})
        
    return {
        "crop": crop,
        "recommendations": recommendations,
        "guidance": f"Ensure moisture in soil before applying {recommendations[0]['type']}."
    }
