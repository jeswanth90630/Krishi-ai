import json
import os
from fastapi import APIRouter

router = APIRouter(prefix="/api/advisory")

ADVISORY_PATH = "data/advisory_rules.json"

def load_advisory():
    if os.path.exists(ADVISORY_PATH):
        with open(ADVISORY_PATH, "r") as f:
            return json.load(f)
    return {}

@router.post("/")
def advisory(data: dict):
    query = data.get("disease") or data.get("pest") or data.get("soil") or "Unknown"
    rules = load_advisory()
    
    result = rules.get(query, {
        "cause": f"{query} - No specific data found",
        "treatment": "Consult a local agricultural expert",
        "prevention": "Maintain standard soil sanitation and hygiene"
    })
    
    return result