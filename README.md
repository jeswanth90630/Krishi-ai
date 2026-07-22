<div align="center">

<!-- HEADER ANIMATION -->
<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&pause=1000&color=2E7D32&center=true&vCenter=true&width=600&lines=%F0%9F%8C%BE+KRISHI+AI%3A+SMART+AGRICULTURE;%F0%9F%A9BA+PRECISION+PLANT+DIAGNOSTICS;%F0%9F%A7A0+HYBRID+DEEP+LEARNING+%2B+LLM;%F0%9F%93%88+REAL-TIME+AGRICULTURAL+ADVISORY" alt="Typing SVG" />
</a>

# 🌾 KRISHI AI

### *Empowering Agriculture through Deep Learning & Generative AI*

<p align="center">
  <b>A next-generation, high-performance agricultural decision system combining Convolutional Neural Networks, Classical Machine Learning, and Large Language Models.</b>
</p>

<!-- BADGES & SHIELDS -->
<p align="center">
  <a href="#-key-features"><img src="https://img.shields.io/badge/Status-Production--Ready-2E7D32?style=for-the-badge&logo=rocket&logoColor=white" alt="Status"></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/PyTorch-MobileNetV3-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch"></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/AI Core-Google_Gemini-8E44AD?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Gemini AI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License"></a>
</p>

<!-- QUICK LINKS BAR -->
<p align="center">
  <a href="#-platform-architecture"><b>Architecture</b></a> •
  <a href="#-the-5-ai-intelligence-pillars"><b>AI Models</b></a> •
  <a href="#-key-features"><b>Features</b></a> •
  <a href="#-tech-stack"><b>Tech Stack</b></a> •
  <a href="#-quick-start"><b>Quick Start</b></a> •
  <a href="#-api-documentation"><b>API Docs</b></a>
</p>

<img src="https://raw.githubusercontent.com/andreyforfun/andreyforfun/main/assets/line.gif" width="100%" />

</div>

---

## 🌟 Executive Summary

**Krishi AI** is a multi-modal, end-to-end agricultural intelligence platform engineered to eliminate yield loss, misdiagnosis, and market opacity for modern farming operations. 

By unifying lightweight mobile-edge **Convolutional Neural Networks (MobileNetV3)**, texture-analyzing **Scikit-Learn Classifiers**, and context-aware **Google Gemini Generative AI**, Krishi AI converts raw field telemetry and leaf imagery into real-time, high-precision agronomical advisories.

---

## 🏛️ System Architecture

The ecosystem relies on an asynchronous event-driven backend built on **FastAPI**, serving zero-latency static assets alongside AI inference engines.

```mermaid
flowchart TD
    %% Custom Styling
    classDef client fill:#1E293B,stroke:#38BDF8,stroke-width:2px,color:#FFF;
    classDef gateway fill:#0F766E,stroke:#14B8A6,stroke-width:2px,color:#FFF;
    classDef model fill:#15803D,stroke:#22C55E,stroke-width:2px,color:#FFF;
    classDef external fill:#7E22CE,stroke:#A855F7,stroke-width:2px,color:#FFF;

    subgraph ClientLayer ["📱 Frontend Presentation Layer"]
        UI["Vanilla ES6+ Web UI (Glassmorphism + AOS)"]:::client
        Geo["Browser Geolocation API"]:::client
    end

    subgraph GatewayLayer ["⚡ Backend API Gateway (FastAPI)"]
        Router{"Modular API Routers"}:::gateway
        Sanitizer["Pydantic Payload Validation"]:::gateway
    end

    subgraph InferenceLayer ["🧠 Deep Learning & Machine Learning Core"]
        DiseaseNet["MobileNetV3 (Plant Health)
        20 Disease Classes | Softmax > 35%"]:::model
        PestNet["MobileNetV3 (Entomology)
        102 Pest Classes | Softmax > 20%"]:::model
        SoilForest["Random Forest (Soil Analysis)
        153 OpenCV Features | Softmax > 40%"]:::model
        CropSKL["Scikit-Learn Classifier
        NPK + pH + Climate Vectors"]:::model
    end

    subgraph ExternalLayer ["🌐 External Intelligence Services"]
        Gemini["Google Gemini Generative AI Core
        (Market Trends, Schemes & Schedules)"]:::external
        OpenMeteo["Open-Meteo Weather API"]:::external
    end

    UI -->|Multipart Upload / JSON Payload| Router
    Geo -->|Coordinates| Router
    Router --> Sanitizer
    Sanitizer --> DiseaseNet
    Sanitizer --> PestNet
    Sanitizer --> SoilForest
    Sanitizer --> CropSKL
    Sanitizer --> Gemini
    Sanitizer --> OpenMeteo

    DiseaseNet -->|JSON Diagnosis| UI
    PestNet -->|JSON Remedies| UI
    SoilForest -->|Soil Profile| UI
    CropSKL -->|Optimal Crop| UI
    Gemini -->|Structured Insights| UI
    OpenMeteo -->|Live Climate Data| UI
```

---

## 🧠 The 5 AI Intelligence Pillars

Krishi AI replaces single-model limitations with a **Hybrid Machine Learning Architecture**, deploying specialized models optimized for specific visual, tabular, and conversational domains.

| Pillar | Model / Algorithm | Input Data | Target Domain & Feature Extraction | Safety / Precision Net |
| :--- | :--- | :--- | :--- | :--- |
| **1. Plant Disease Scan** | **MobileNetV3-Large** *(PyTorch)* | Leaf Imagery (`224x224`) | CNN Spatial Feature Map trained on PlantVillage (20 classes like Late Blight, Apple Scab) | Confidence Threshold `< 35%` triggers rejection guardrail |
| **2. Pest Identification** | **MobileNetV3-Large** *(PyTorch)* | Pest Imagery (`224x224`) | Entomology Neural Net classifying **102 agricultural insect species** mapped to `pest_db.json` | Confidence Threshold `< 20%` triggers rejection guardrail |
| **3. Soil Texture Analyzer** | **Random Forest** *(Scikit-Learn)* | Soil Imagery (`256x256`) | Manual OpenCV extraction of **153 mathematical features** (96 HSV + 48 LAB + 6 RGB + 3 Sobel Gradients) | Confidence Threshold `< 40%` triggers non-soil rejection |
| **4. Crop Recommendation** | **Random Forest / ML** *(Scikit-Learn)* | Tabular NPK, pH & Weather | Vectorized matching of Nitrogen, Phosphorus, Potassium, Humidity, and Rainfall against optimal soil conditions | Deterministic Agronomical Bounds |
| **5. Generative Reasoning** | **Google Gemini LLM** | Structured JSON Prompts | Dynamic calculation of price elasticity, Mandi price trends, PM-KISAN eligibility, and daily farm tasks | Strict JSON schema enforcement & markdown sanitization |

---

## 🚀 Key Modules & Capabilities

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🔍 Multi-Modal Field Health Scan</h3>
      <ul>
        <li><b>Instant Plant Pathology:</b> Identifies 20 fungal, bacterial, and viral crop diseases.</li>
        <li><b>Pest Detection Engine:</b> Pinpoints 102 insect species with exact chemical & organic remedies.</li>
        <li><b>Vision Soil Profiling:</b> Measures soil texture, porosity, and organic suitability without physical lab kits.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>🌱 Smart Crop & Fertilizer Advisor</h3>
      <ul>
        <li><b>NPK Deficit Calculation:</b> Calculates exact kilogram shortfall per acre and provides customized fertilization timelines.</li>
        <li><b>Precision Water Planner:</b> Computes evapotranspiration-based daily irrigation needs.</li>
        <li><b>Yield Maximizer:</b> Recommends cash crops tailored to real-time micro-climate data.</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>📈 Mandi Market Intelligence</h3>
      <ul>
        <li><b>Dynamic Pricing Forecasts:</b> AI-driven price charts powered by Chart.js.</li>
        <li><b>Arbitrage Analyzer:</b> Compares local rural Mandis vs. city centers to evaluate transport profitability.</li>
        <li><b>Demand Sentiment:</b> Predicts market surges to advise farmers on ideal harvest-sale timing.</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h3>📜 Govt. Scheme & Welfare Matcher</h3>
      <ul>
        <li><b>AI Eligibility Engine:</b> Evaluates farmer demographics against state/national schemes (PM-KISAN, PMFBY, KUSUM).</li>
        <li><b>Direct Portal Bridge:</b> Connects verified eligible farmers directly to official government application portals.</li>
        <li><b>Zero-Fund Waste:</b> Ensures financial subsidies reach eligible smallholder farmers.</li>
      </ul>
    </td>
  </tr>
</table>

---

## 🛠️ Technology Stack

<table align="center">
  <tr>
    <td align="center" width="20%"><b>Core AI & ML</b></td>
    <td>
      <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" />
      <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" />
      <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" />
      <img src="https://img.shields.io/badge/Google_Gemini-8E44AD?style=flat-square&logo=googlegemini&logoColor=white" />
      <img src="https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white" />
      <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" />
    </td>
  </tr>
  <tr>
    <td align="center" width="20%"><b>Backend Infrastructure</b></td>
    <td>
      <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
      <img src="https://img.shields.io/badge/Uvicorn-499848?style=flat-square&logo=uvicorn&logoColor=white" />
      <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" />
      <img src="https://img.shields.io/badge/Python_3.9+-3776AB?style=flat-square&logo=python&logoColor=white" />
    </td>
  </tr>
  <tr>
    <td align="center" width="20%"><b>Frontend & Visuals</b></td>
    <td>
      <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" />
      <img src="https://img.shields.io/badge/CSS3_Glassmorphism-1572B6?style=flat-square&logo=css3&logoColor=white" />
      <img src="https://img.shields.io/badge/JavaScript_ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black" />
      <img src="https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white" />
      <img src="https://img.shields.io/badge/SweetAlert2-8B5CF6?style=flat-square&logo=sweetalert2&logoColor=white" />
    </td>
  </tr>
  <tr>
    <td align="center" width="20%"><b>External Services</b></td>
    <td>
      <img src="https://img.shields.io/badge/Open--Meteo_API-00A8E8?style=flat-square&logo=cloud&logoColor=white" />
      <img src="https://img.shields.io/badge/PlantVillage_Dataset-2E7D32?style=flat-square&logo=leaf&logoColor=white" />
    </td>
  </tr>
</table>

---

## 📂 Project Architecture

```text
krishi-ai/
├── backend/backend/                # Core FastAPI Microservices
│   ├── app/                        # Application Domain Modules
│   │   ├── routers/                # Endpoints (detection, prediction, advisory, market)
│   │   ├── services/               # Inference Pipelines & Gemini API Integration
│   │   └── config.py               # Application Settings & Guardrails
│   └── run.py                      # Server Entry Point & Static File Server
├── frontend/                       # Client UI Application
│   ├── assets/                     # Stylesheets (CSS variables, Glassmorphic UI), Scripts
│   ├── components/                 # Shared UI Components & Navbars
│   └── pages/                      # Application Interfaces (index.html, scan.html, etc.)
├── models/exports/                 # Production AI Artifacts (.pth, .pkl, metadata)
├── data/                           # Training & Validation Datasets
└── requirements.txt                # Production Dependencies
```

---

## ⚙️ Quick Start & Installation

### 1. Repository Setup & Environment

```bash
# Clone the repository
git clone https://github.com/vigneshaadepu/Krishi-Ai.git
cd Krishi-Ai

# Create and activate Python virtual environment
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate
```

### 2. Dependency Installation

```bash
# Install core dependencies
pip install -r requirements.txt

# Install PyTorch engine (CPU optimized or CUDA enabled)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 3. Launching the Platform

```powershell
# Set backend execution path (Windows PowerShell)
$env:PYTHONPATH="backend/backend"

# Start unified server
python backend/backend/run.py
```

The system will initialize at: **`http://127.0.0.1:8000`**

---

## 📋 Interactive API Documentation

Once the backend service is running, interact with live endpoint specs:

- **Swagger UI**: [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
- **ReDoc Interface**: [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

---

## 🔒 Privacy & Operational Safety

1. **Zero Data Retention:** Image uploads during Field Health Scans are processed entirely in RAM/VRAM during inference and purged immediately.
2. **Confidence Safety Net:** Any input falling below minimum statistical confidence thresholds is gracefully rejected to protect farmers from misdiagnosis.
3. **Structured AI Guardrails:** Generative AI responses pass through strict JSON schema validation to guarantee deterministic API outputs.

---

<div align="center">

<img src="https://raw.githubusercontent.com/andreyforfun/andreyforfun/main/assets/line.gif" width="100%" />

### 🌾 Krishi AI — *Architecting the Future of Smart Agriculture*

<p align="center">
  Designed & Built with ❤️ for Global Farming Communities
</p>

<p align="center">
  <a href="#"><b>⬆ Back to Top</b></a>
</p>

</div>
