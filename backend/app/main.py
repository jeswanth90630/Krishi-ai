from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import detection, advisory, prediction, weather, market, schemes, fertilizer, water, resources, chatbot
import os

app = FastAPI(title="Krishi AI")


# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project root is the current working directory if running from the root
frontend_path = os.path.join(os.getcwd(), "frontend")

# Include API routers (NOT dual-prefixed, as they already define /api in prediction.py etc.)
app.include_router(detection.router)
app.include_router(advisory.router)
app.include_router(prediction.router)
app.include_router(weather.router)
app.include_router(market.router)
app.include_router(schemes.router)
app.include_router(fertilizer.router)
app.include_router(water.router)
app.include_router(resources.router)

app.include_router(chatbot.router)

# Serve static files from frontend
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/api/health")
def home():
    return {"status": "healthy", "service": "Krishi AI"}