from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import requests
import json

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])

GEMINI_KEY = "AIzaSyARwPFM0IqEQW094bfo9eQ3Qx1XAMIQ6Tc"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    message: str
    page_context: Optional[str] = "general"
    history: Optional[List[Message]] = []
    lang: Optional[str] = "en"

LANG_NAMES = {"hi": "Hindi", "te": "Telugu", "en": "English"}

SYSTEM_PROMPT = """You are Kisaan, an expert AI agricultural advisor built into the Krishi AI platform. 
You are warm, helpful, and speak like a knowledgeable farmer-friend.

Your expertise covers:
- Crop selection, seasonal planning, and yield optimization
- Soil health, NPK ratios, pH management, and fertilizer advice
- Pest and disease identification, treatment, and prevention
- Irrigation scheduling, water management, and drought strategies
- Weather impact on crops and adaptive farming techniques
- Government schemes, subsidies, and MSP for Indian farmers
- Market prices, post-harvest management, and storage
- Organic farming, sustainable practices, and biocontrol agents

Behavior rules:
- Always give PRACTICAL, ACTIONABLE advice a farmer can immediately follow
- Use simple, clear language avoiding complex jargon
- If asked about something outside agriculture, gently redirect: "I'm specialized in farming — let me help with your field!"
- Keep responses concise (2-4 sentences for simple queries, up to a paragraph for complex ones)
- Always end complex responses with ONE specific next-step action
- Use emojis sparingly but effectively (🌾 🌱 💧 🐛 etc.)

IMPORTANT: Respond in {lang}. The farmer prefers {lang}.
Current page context: {page_context}
"""

@router.post("/")
def chat(req: ChatRequest):
    target_lang = LANG_NAMES.get(req.lang, "English")
    
    system = SYSTEM_PROMPT.format(
        lang=target_lang,
        page_context=req.page_context
    )
    
    # Build conversation history for Gemini
    # Gemini uses alternating user/model turns
    contents = []
    
    # Add system context as first user message (Gemini Pro doesn't have system role)
    contents.append({
        "role": "user",
        "parts": [{"text": f"[Instructions: {system}]\n\nHello Kisaan!"}]
    })
    contents.append({
        "role": "model",
        "parts": [{"text": f"Namaste! 🌾 I'm Kisaan, your personal farming advisor. Ask me anything about your crops, soil, weather, pests, or government schemes — I'm here to help you grow better!"}]
    })
    
    # Add conversation history
    for msg in req.history[-8:]:  # Keep last 8 messages for context
        role = "user" if msg.role == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg.content}]
        })
    
    # Add current message
    contents.append({
        "role": "user",
        "parts": [{"text": req.message}]
    })
    
    try:
        resp = requests.post(GEMINI_URL, json={
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
                "topP": 0.9
            }
        }, timeout=20)
        
        raw = resp.json()
        
        if "candidates" not in raw:
            print(f"Gemini error: {raw}")
            return {"reply": "I'm having trouble connecting right now. Please try again in a moment! 🌱"}
        
        reply = raw["candidates"][0]["content"]["parts"][0]["text"].strip()
        return {"reply": reply}
        
    except Exception as e:
        print(f"Chatbot error: {e}")
        return {"reply": "Connection issue — please check your internet and try again. Your crops depend on it! 🌾"}


@router.post("/weather-advisory")
def weather_advisory(req: dict):
    """Get AI crop recommendations based on current weather data."""
    weather = req.get("weather", {})
    location = req.get("location", "India")
    
    prompt = f"""As an expert agricultural weather advisor for {location}:

Current conditions:
- Temperature: {weather.get('temperature', 28)}°C
- Humidity: {weather.get('humidity', 65)}%
- Condition: {weather.get('condition', 'Sunny')}
- UV Index: {weather.get('uv_index', 6)}
- Wind Speed: {weather.get('wind_speed', 12)} kph
- Soil Temperature: {weather.get('soil_temp', 26)}°C
- Pest Risk: {weather.get('pest_risk', 'Medium')}

Provide a comprehensive agricultural forecast and recommendation in this EXACT JSON format:
{{
  "forecast_summary": "One compelling sentence about today's farming outlook",
  "best_crops": [
    {{"name": "Crop Name", "reason": "Why ideal for today", "action": "What to do now", "icon": "emoji"}},
    {{"name": "Crop Name", "reason": "Why ideal for today", "action": "What to do now", "icon": "emoji"}},
    {{"name": "Crop Name", "reason": "Why ideal for today", "action": "What to do now", "icon": "emoji"}}
  ],
  "irrigation_advice": "Specific watering advice for today",
  "pest_warning": "Any pest threats based on current humidity/temp",
  "soil_action": "What to do with soil today",
  "best_time_to_work": "Optimal time window for field work today",
  "yield_tip": "One high-impact tip to increase yield this week",
  "risk_level": "Low/Medium/High",
  "risk_reason": "Why this risk level"
}}

Return ONLY JSON. NO PREAMBLE."""

    try:
        resp = requests.post(GEMINI_URL, json={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2048}
        }, timeout=20)
        
        raw = resp.json()
        content = raw["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        if "{" in content:
            content = content[content.find("{"):content.rfind("}")+1]
        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(content)
        return {"success": True, "advisory": data}
        
    except Exception as e:
        print(f"Weather advisory error: {e}")
        return {
            "success": True,
            "advisory": {
                "forecast_summary": "Good farming conditions today with moderate temperature.",
                "best_crops": [
                    {"name": "Rice", "reason": "Ideal humidity", "action": "Water moderately", "icon": "🌾"},
                    {"name": "Maize", "reason": "Good sun exposure", "action": "Apply nitrogen fertilizer", "icon": "🌽"},
                    {"name": "Tomato", "reason": "Warm soil temperature", "action": "Check for fungal signs", "icon": "🍅"}
                ],
                "irrigation_advice": "Irrigate in early morning to reduce evaporation loss.",
                "pest_warning": "Monitor for aphids in humid conditions.",
                "soil_action": "Test soil pH before next fertilizer application.",
                "best_time_to_work": "Early morning (6-9 AM) to avoid heat stress",
                "yield_tip": "Apply micronutrient spray (zinc sulfate) for 15-20% yield boost.",
                "risk_level": "Low",
                "risk_reason": "Stable weather with manageable humidity."
            }
        }
