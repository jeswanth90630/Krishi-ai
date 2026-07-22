from fastapi import APIRouter
import random

router = APIRouter(prefix="/api/water", tags=["Water"])

@router.post("/predict")
def predict_water(data: dict):
    # Predict based on: Crop, Area, Temperature, Humidity
    crop = data.get("crop", "Rice")
    area = float(data.get("area", 1)) # Acres
    temp = float(data.get("temperature", 25))
    hum = float(data.get("humidity", 50))
    
    # Simple logic: higher temp, lower humidity => more water
    base_water = 2000 # Liters/acre/day
    if crop.lower() == "rice":
        base_water = 5000
    elif crop.lower() == "maize":
        base_water = 3000
    
    factor = (temp / 25) * (150 / (hum + 50))
    daily = round(base_water * area * factor, 1)
    weekly = round(daily * 7, 0)
    
    return {
        "crop": crop,
        "area": area,
        "daily_requirement_liters": daily,
        "weekly_requirement_liters": weekly,
        "irrigation_mode": "Drip Irrigation Recommended" if daily < 3000 else "Flood Irrigation Recommended",
        "guidance": "Avoid irrigating in peak heat hours (12 PM - 3 PM) to prevent evaporation losses."
    }
