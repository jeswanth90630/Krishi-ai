import requests
import json
import logging

GEMINI_KEY = "AIzaSyARwPFM0IqEQW094bfo9eQ3Qx1XAMIQ6Tc"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

def translate_content(content_dict: dict, target_lang: str) -> dict:
    """
    Translates a dictionary of agricultural data into the target language using Gemini.
    target_lang: 'en', 'hi', 'te'
    """
    if target_lang == 'en' or not target_lang:
        return content_dict
        
    lang_map = {
        'hi': 'Hindi',
        'te': 'Telugu'
    }
    
    target_name = lang_map.get(target_lang, 'English')
    
    # We only translate the text values, keeping the keys and structure intact
    prompt = f"""
    Translate the following JSON object into {target_name}. 
    Ensure the agricultural terminology is accurate for an Indian farmer.
    Keep the JSON keys exactly the same. Only translate the values.
    JSON to translate:
    {json.dumps(content_dict)}
    
    Return only the translated valid JSON. No other text.
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=12)
        res_json = response.json()
        if 'candidates' in res_json:
            gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
            # Clean possible markdown markers
            clean_text = gemini_text.strip().strip('```json').strip('```').strip()
            return json.loads(clean_text)
        else:
            logging.error(f"Gemini Translation Error: {res_json}")
            return content_dict
    except Exception as e:
        logging.error(f"Translation Exception: {e}")
        return content_dict
