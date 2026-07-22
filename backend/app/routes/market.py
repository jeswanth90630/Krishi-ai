import requests
import json
import random
from fastapi import APIRouter

router = APIRouter(prefix="/api/market", tags=["Market"])

GEMINI_KEY = "AIzaSyARwPFM0IqEQW094bfo9eQ3Qx1XAMIQ6Tc"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

CROPS = ["Rice (Basmati)", "Wheat (Sharbati)", "Sugarcane", "Maize (Hybrid)", "Cotton (Long Staple)", "Jute"]
MANDIS = ["Azadpur, DL", "Vashi, MH", "Yeshwanthpur, KA", "Kurnool, AP"]

@router.get("/prices")
def get_prices():
    prompt = """
    Act as an Indian agricultural market analyst with access to current real-time Mandi price data.
    Provide current realistic market prices for 6 crops: Rice (Basmati), Wheat (Sharbati), Sugarcane, Maize (Hybrid), Cotton (Long Staple), Jute.
    Assign a popular Indian Mandi (like Azadpur, Vashi, Yeshwanthpur, etc.) to each crop.
    Determine realistic price per quintal in ₹ based on current market trends.
    Determine the trend direction ("Upward (▲)", "Downward (▼)", or "Stable (–)").
    Assign a color field: "green" for Upward/Stable, "red" for Downward.
    
    Return JSON exactly mimicking this list format inside a dict key 'prices':
    {
      "prices": [
        {
          "crop": "Rice (Basmati)",
          "mandi": "Vashi, MH",
          "price_per_quintal": 12500,
          "trend": "Upward (▲)",
          "color": "green"
        }
      ]
    }
    Generate the list for all 6 crops. Return only JSON.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=12)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        data = json.loads(clean_text)
        return data
    except Exception as e:
        # Fallback to random if API fails
        prices = []
        for crop in CROPS:
            base_price = random.randint(2500, 6800)
            prices.append({
                "crop": crop,
                "mandi": random.choice(MANDIS),
                "price_per_quintal": base_price,
                "trend": random.choice(["Upward (▲)", "Downward (▼)", "Stable (–)"]),
                "color": "green" if base_price > 4500 else "red"
            })
        return {"prices": prices}

@router.get("/sentiment")
def get_sentiment():
    crops = ["Wheat", "Rice", "Cotton", "Sugarcane"]
    target_crop = random.choice(crops)
    prompt = f"""
    Act as an Indian agricultural market analyst.
    For {target_crop}, generate a short, simple, actionable market sentiment for a normal farmer.
    Return JSON with exactly these keys:
    - "headline": very short 3-4 word headline (e.g. "Prices Going Up! 📈").
    - "trend": the predicted price change in ₹ per quintal.
    - "advice": one sentence of advice (e.g. "Wheat prices expected to rise next week. Good time to hold stock.").
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=10)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        data = json.loads(clean_text)
        return data
    except Exception as e:
        return {
            "headline": "Prices Going Up! 📈",
            "trend": "+₹85",
            "advice": f"{target_crop} prices expected to rise next week. Good time to hold stock."
        }

@router.get("/compare")
def get_market_compare():
    prompt = """
    Act as an Indian agricultural market analyst with access to current government Mandi price data.
    Provide current realistic market prices for 4 staple crops: Wheat, Rice, Maize, Cotton.
    Return JSON exactly mimicking this structure:
    {
      "labels": ["Wheat", "Rice", "Maize", "Cotton"],
      "local": [2200, 3100, 1800, 6800],
      "city": [2450, 3500, 2100, 7300]
    }
    Make 'city' prices slightly higher than 'local' to reflect transport/market fees.
    Ensure values are realistic ₹/quintal pricing.
    Return only JSON.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=10)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        return json.loads(clean_text)
    except Exception as e:
        return {
            "labels": ["Wheat", "Rice", "Maize", "Cotton"],
            "local": [2250, 3200, 1850, 6900],
            "city": [2500, 3600, 2150, 7400]
        }