from fastapi import APIRouter
from pydantic import BaseModel
import requests
import json

router = APIRouter(prefix="/api/schemes", tags=["Schemes"])

GEMINI_KEY = "AIzaSyARwPFM0IqEQW094bfo9eQ3Qx1XAMIQ6Tc"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}"

class Profile(BaseModel):
    need: str

SCHEMES_DB = [
    {
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "benefit": "₹6,000 per year in three installments",
        "description": "Direct financial support to landholding farmer families to help with agricultural and domestic needs.",
        "eligibility": "All landholding farmers families",
        "url": "https://pmkisan.gov.in/"
    },
    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "benefit": "Comprehensive crop insurance coverage",
        "description": "Protection against crop failure due to natural calamities, pests, or disease outbreaks.",
        "eligibility": "Farmers growing notified crops in notified areas",
        "url": "https://pmfby.gov.in/"
    },
    {
        "name": "Pradhan Mantri Kisan MaanDhan Yojana (PM-KMY)",
        "benefit": "₹3,000 monthly pension after age 60",
        "description": "A voluntary and contributory pension scheme providing financial security in old age for farmers.",
        "eligibility": "Small and marginal farmers aged 18-40 years",
        "url": "https://maandhan.in/"
    },
    {
        "name": "Kisan Credit Card (KCC) Scheme",
        "benefit": "Short-term credit at low interest rates",
        "description": "Provides short-term credit to farmers for cultivating crops and animal husbandry needs.",
        "eligibility": "All farmers, sharecroppers, and tenant farmers",
        "url": "https://sbi.co.in/web/agri-rural/agriculture-banking/crop-loan/kisan-credit-card"
    },
    {
        "name": "Pradhan Mantri Krishi Sinchai Yojana (PMKSY)",
        "benefit": "Subsidies for irrigation technologies",
        "description": "Aims to improve on-farm water use efficiency ('More Crop Per Drop') and expand irrigation coverage.",
        "eligibility": "Farmers with arable land",
        "url": "https://pmksy.gov.in/"
    },
    {
        "name": "Soil Health Card (SHC) Scheme",
        "benefit": "Free soil testing & nutrient recommendations",
        "description": "Issues cards to farmers providing information on soil nutrients to promote judicious fertilizer use.",
        "eligibility": "All active farmers",
        "url": "https://soilhealth.dac.gov.in/"
    },
    {
        "name": "e-National Agriculture Market (e-NAM)",
        "benefit": "Unified online national trading platform",
        "description": "An online trading platform creating a unified national market for agricultural produce.",
        "eligibility": "All registered farmers and FPOs",
        "url": "https://enam.gov.in/"
    },
    {
        "name": "Agriculture Infrastructure Fund (AIF)",
        "benefit": "Medium-long term debt financing",
        "description": "Provides medium-long term debt financing for post-harvest management and community farming assets.",
        "eligibility": "Farmers, FPOs, PACS, and Agri-entrepreneurs",
        "url": "https://agriinfra.dac.gov.in/"
    },
    {
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "benefit": "₹50,000 per hectare for 3 years",
        "description": "Promotes organic farming through cluster-based approaches and participatory guarantee systems.",
        "eligibility": "Farmers operating in clusters of 20 hectares",
        "url": "https://pgsindia-ncof.gov.in/pkvy/"
    },
    {
        "name": "Pradhan Mantri Annadata Aay SanraksHan Abhiyan (PM-AASHA)",
        "benefit": "Remunerative prices for harvest",
        "description": "Ensures remunerative prices for farmers through price support and market intervention schemes.",
        "eligibility": "Farmers selling registered crops at mandis",
        "url": "https://agricoop.nic.in/"
    },
    {
        "name": "Namo Drone Didi",
        "benefit": "Drones provided for agricultural spraying",
        "description": "Provides drones to women self-help groups (SHGs) to offer agricultural spraying services.",
        "eligibility": "Women SHGs in rural networks",
        "url": "https://droa.gov.in/"
    },
    {
        "name": "National Beekeeping and Honey Mission (NBHM)",
        "benefit": "Funding for scientific beekeeping",
        "description": "Promotes scientific beekeeping (Sweet Revolution) for higher income generation.",
        "eligibility": "Beekeepers, farmers, and FPOs",
        "url": "https://nbhm.gov.in/"
    },
    {
        "name": "Rashtriya Krishi Vikas Yojana-Raftaar (RKVY-RAFTAAR)",
        "benefit": "Grants for agri-entrepreneurship",
        "description": "Focuses on strengthening infrastructure, promoting agri-entrepreneurship, and value addition.",
        "eligibility": "Farmers and Agri-startups",
        "url": "https://rkvy.nic.in/"
    },
    {
        "name": "Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyan (PM-KUSUM)",
        "benefit": "Subsidies for solar agricultural pumps",
        "description": "Subsidizes solar pumps and supports solarizing existing grid-connected agricultural pumps.",
        "eligibility": "Individual farmers, cooperatives, panchayats",
        "url": "https://pmkusum.mnre.gov.in/"
    },
    {
        "name": "National Mission on Edible Oils – Oil Palm (NMEO-OP)",
        "benefit": "Support for oil palm cultivation",
        "description": "Aims to increase domestic oil palm production to reduce import dependence.",
        "eligibility": "Farmers in designated oil-palm states",
        "url": "https://minis.gov.in/"
    }
]

@router.get("/")
def get_schemes():
    return {"schemes": SCHEMES_DB}

@router.post("/match")
def match_scheme(profile: Profile):
    prompt = f"""
    Act as an Indian Govt scheme advisor for a farmer. The farmer selected this specific requirement category from a drop-down list: "{profile.need}".
    From the active Indian central government agricultural schemes (like PM-KISAN, KCC, PMFBY, PKVY, PMKSY, PM-KUSUM, etc.), recommend the absolute best matching scheme.
    Return JSON format exactly like this:
    {{
      "recommended": "Name of Scheme",
      "reason": "Why this is perfectly suited for their requirement (1-2 sentences).",
      "eligibility": "Bullet points or short list of exact eligibility criteria.",
      "documents": "Comma separated list of exactly what documents they need to prepare.",
      "next_steps": "What immediate action the farmer should take to apply."
    }}
    Provide only valid JSON.
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=15)
        res_json = response.json()
        gemini_text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean_text = gemini_text.strip().strip('```json').strip('```').strip()
        return json.loads(clean_text)
    except Exception:
        return {
            "recommended": "Kisan Credit Card (KCC)",
            "reason": "This is a versatile scheme that can help with various ongoing financial needs for cultivation.",
            "eligibility": "All landholding farmers, tenant farmers, and sharecroppers.",
            "documents": "Aadhaar Card, PAN Card, Land Ownership Records, Passport Size Photos.",
            "next_steps": "Visit your nearest rural bank branch with the documents to apply."
        }