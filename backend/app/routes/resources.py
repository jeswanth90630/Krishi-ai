from fastapi import APIRouter
from pydantic import BaseModel
import requests
import json

router = APIRouter(prefix="/api/resources", tags=["Resources"])

GEMINI_KEY = "AIzaSyARwPFM0IqEQW094bfo9eQ3Qx1XAMIQ6Tc"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

class TaskReq(BaseModel):
    task: str

@router.post("/equipment")
def get_dynamic_equipment(req: TaskReq):
    if req.task == "default":
        return {"equipment": [
            {"name": "Combine Harvester", "price": "₹1500/hr", "availability": "3 Available", "location": "Nearby Sub-Plot A", "reason": "Standard high-yield harvesting equipment."},
            {"name": "Mini Tractor (35HP)", "price": "₹500/hr", "availability": "2 Available", "location": "District Service Hub", "reason": "Essential for general field plowing and prep."},
            {"name": "Power Tiller", "price": "₹300/hr", "availability": "1 Available", "location": "Local Agri Center", "reason": "Ideal for small fields and tight inter-cultivation."},
            {"name": "Drip Irrigation Kit", "price": "₹1200/day", "availability": "5 Available", "location": "Water Management Hub", "reason": "Highly efficient deep watering system."}
        ]}
        
    prompt = f"""
    Act as an Indian agricultural equipment rental AI advisor. The farmer has provided the following context: "{req.task}".
    Based strictly on this profile, strongly recommend a comprehensive list of exactly 8 to 10 highly relevant pieces of precision farming equipment available for rent.
    Ensure a wide variety of choices are provided for the farmer's comfort in selecting the best tool based on their specific budget and capability scale.
    Return JSON format exactly like this:
    {{
      "equipment": [
        {{
           "name": "Equipment Name (e.g., Heavy Duty Rotavator)",
           "price": "Price rate (e.g., ₹800/hr)",
           "availability": "e.g. 2 Available",
           "location": "e.g. Local Agri Center",
           "reason": "Why this equipment specifically helps given the context provided (1 sentence max)"
        }}
      ]
    }}
    Provide only valid JSON.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=12)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        return json.loads(clean_text)
    except Exception:
        return {"equipment": [
            {"name": f"Standard {req.task} Tool", "price": "₹500/hr", "availability": "1 Available", "location": "Local Agri Center", "reason": f"Fallback tool suited for {req.task}."}
        ]}

class WasteReq(BaseModel):
    profile: str

@router.post("/waste")
def get_waste(req: WasteReq):
    if req.profile == "default":
        prompt = """
        Act as an Agricultural Biomass & Waste Exchange platform for Indian farmers. 
        Generate a dynamic list of exactly 6 active, highly realistic marketplace listings. 
        HALF of these 6 listings must be "BUY" listings (commercial factories looking to buy waste).
        The OTHER HALF must be "SELL" listings (other farmers selling their agricultural waste).
        Return JSON exactly mimicking this strict structure:
        {
          "waste": [
            {
              "trade_type": "BUY",
              "type": "Sugarcane Bagasse",
              "quantity": "Required/Available: 100 Tons",
              "price": "₹350 per Ton",
              "entity": "GreenEnergy Bio-Refinery (for BUY) or Ramesh Kumar (for SELL)",
              "usage": "Converted into Bio-ethanol and clean energy fuel (or quality description for SELL).",
              "status": "High Demand - Open Bid (or Active Listing)",
              "urgency": "High"
            }
          ]
        }
        Provide only valid JSON.
        """
    else:
        prompt = f"""
        Act as an Agricultural Biomass & Waste Exchange platform for Indian farmers.
        The farmer has provided the following waste profile they desperately want to sell: "{req.profile}".
        Based STRICTLY on this specific profile, strongly recommend a comprehensive list of exactly 6 active, highly realistic commercial buyers (Refineries, Mills, Power Plants, or Fertilizer Plants) who are actively looking to buy THIS EXACT TYPE of biomass.
        Provide accurate price estimates they are willing to pay based on current Indian agricultural markets.
        Return JSON exactly mimicking this strict structure:
        {{
          "waste": [
            {{
              "trade_type": "BUY",
              "type": "The exact waste type requested",
              "quantity": "The quantity they are willing to buy",
              "price": "Price per Ton/Quintal exactly formatted (e.g., ₹350 per Ton)",
              "entity": "Realistic Company Name (e.g., GreenEnergy Bio-Refinery)",
              "usage": "Exactly what the company will convert this specific waste into.",
              "status": "High Demand - Active Bid",
              "urgency": "High"
            }}
          ]
        }}
        Provide only valid JSON.
        """
        
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=12)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        return json.loads(clean_text)
    except Exception:
        return {
            "waste": [
                {
                    "trade_type": "BUY",
                    "type": "Rice Husk", 
                    "quantity": "Required: 50 Quintals", 
                    "price": "₹200/qt", 
                    "entity": "Local Biofuel Bio-Refinery", 
                    "usage": "Used for generating pure thermal bio-mass energy.",
                    "status": "Open Bid",
                    "urgency": "Medium"
                }
            ]
        }

class SellReq(BaseModel):
    crop_type: str
    quantity: str

@router.post("/waste_sell")
def create_sell_listing(req: SellReq):
    prompt = f"""
    An Indian farmer wants to aggressively sell their crop waste.
    Crop Waste Type: {req.crop_type}
    Quantity: {req.quantity}
    
    Using these core requirements from the farmer, generate the remaining details to create a highly professional, attractive marketplace listing for this waste.
    Estimate a fair market price based on current Indian agricultural norms.
    Create an attractive description highlighting the usage potential or condition.
    
    Return JSON exactly mimicking this strict structure:
    {{
       "trade_type": "SELL",
       "type": "{req.crop_type}",
       "quantity": "Available: {req.quantity}",
       "price": "Generated Price (e.g. ₹2000 per Ton)",
       "entity": "You (Local Farmer)",
       "usage": "Generated attractive description of quality and potential industrial usage.",
       "status": "Active Listing",
       "urgency": "Normal"
    }}
    Provide only valid JSON.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=12)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        return json.loads(clean_text)
    except Exception:
        return {
           "trade_type": "SELL",
           "type": req.crop_type,
           "quantity": f"Available: {req.quantity}",
           "price": "₹1500 per Ton",
           "entity": "You (Local Farmer)",
           "usage": "Premium dry crop waste ready for immediate transit.",
           "status": "Active Listing",
           "urgency": "Normal"
        }

@router.post("/chat")
def chatbot(data: dict):
    # Simplistic LLM-like response for hackathon chatbot
    user_msg = data.get("message", "How to grow rice?").lower()
    
    responses = {
        "rice": "Rice grows best in standing water. Maintain 5-10cm level till flowering phase.",
        "wheat": "Wheat requires 4-6 irrigations. The Crown Root Initiation (CRI) phase is most critical.",
        "pests": "We recommend using Neem oil sprays for initial pest control before moving to heavy pesticides.",
        "price": "Market prices are currently stable. We suggest holding your harvest for 2 more weeks if possible.",
        "help": "I can help with crop diagnostics, weather alerts, and market intelligence. Just ask."
    }
    
    for key, val in responses.items():
        if key in user_msg:
            return {"reply": val}
            
    return {"reply": "That's a great question. Based on regional climate data, we recommend focusing on soil health currently. Anything else?"}
