<div align="center">

  <!-- DYNAMIC TYPING HEADER SVG -->
  <a href="https://github.com/jeswanth90630/Krishi-ai">
    <img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=28&pause=1000&color=10B981&center=true&vCenter=true&width=750&height=50&lines=%F0%9F%8C%BE+KRISHI+AI%3A+HYBRID+AGRI-INTELLIGENCE;%F0%9F%A9BA+REAL-TIME+PLANT+PATHOLOGY+%2B+PEST+VISION;%F0%9F%A7A0+FASTAPI+%2B+PYTORCH+%2B+GEMINI+GEN-AI;%F0%9F%93%88+MANDI+ANALYTICS+%2B+GOVT+SCHEME+MATCHER" alt="Krishi AI Header Banner" />
  </a>

  <br/>
  <br/>

  <h1>🌾 KRISHI AI</h1>
  <h3>Next-Generation Multimodal Precision Agriculture & Agronomic Decision System</h3>
  <p><i>Unifying Edge Computer Vision, Classical Agronomic Machine Learning & LLM Reasoning to Protect Crop Yields</i></p>

  <br/>

  <!-- BADGES MATRIX -->
  <p align="center">
    <a href="https://github.com/jeswanth90630/Krishi-ai">
      <img src="https://img.shields.io/badge/System_Status-Production--Ready-059669?style=for-the-badge&logo=rocket&logoColor=white" alt="Status" />
    </a>
    <a href="https://python.org">
      <img src="https://img.shields.io/badge/Python-3.9+-065F46?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    </a>
    <a href="https://fastapi.tiangolo.com/">
      <img src="https://img.shields.io/badge/FastAPI-0.100+-0D9488?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    </a>
    <a href="https://pytorch.org/">
      <img src="https://img.shields.io/badge/PyTorch-MobileNetV3-0F766E?style=for-the-badge&logo=pytorch&logoColor=white" alt="PyTorch" />
    </a>
    <a href="https://scikit-learn.org/">
      <img src="https://img.shields.io/badge/Scikit--Learn-ML_Core-10B981?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
    </a>
    <a href="https://ai.google.dev/">
      <img src="https://img.shields.io/badge/Gen_AI-Google_Gemini-14B8A6?style=for-the-badge&logo=google&logoColor=white" alt="Gemini AI" />
    </a>
    <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-047857?style=for-the-badge" alt="License" />
    </a>
  </p>

  <br/>

  <!-- METRICS HIGHLIGHT BOARD -->
  <table align="center" width="100%">
    <tr>
      <td align="center" valign="top" width="20%">
        <h3>🧬 20+</h3>
        <p><b>Leaf Diseases</b><br/><sub>PyTorch MobileNetV3</sub></p>
      </td>
      <td align="center" valign="top" width="20%">
        <h3>🐛 102</h3>
        <p><b>Pest Species</b><br/><sub>Deep Entomological Vision</sub></p>
      </td>
      <td align="center" valign="top" width="20%">
        <h3>🧪 153</h3>
        <p><b>Soil Features</b><br/><sub>OpenCV Gradients & Color</sub></p>
      </td>
      <td align="center" valign="top" width="20%">
        <h3>⚡ &lt;150ms</h3>
        <p><b>Inference Speed</b><br/><sub>Asynchronous FastAPI API</sub></p>
      </td>
      <td align="center" valign="top" width="20%">
        <h3>🤖 Gemini</h3>
        <p><b>Gen-AI Advisor</b><br/><sub>Contextual Local Guidance</sub></p>
      </td>
    </tr>
  </table>

  <br/>

  <!-- QUICK NAVIGATION CHIPS -->
  <p align="center">
    <a href="#-executive-overview"><b>Overview</b></a> &nbsp;•&nbsp;
    <a href="#-system-architecture"><b>Architecture</b></a> &nbsp;•&nbsp;
    <a href="#-ai--ml-model-pipeline"><b>AI Models</b></a> &nbsp;•&nbsp;
    <a href="#-core-platform-modules"><b>Core Capabilities</b></a> &nbsp;•&nbsp;
    <a href="#-technology-ecosystem"><b>Tech Stack</b></a> &nbsp;•&nbsp;
    <a href="#-project-structure"><b>Project Structure</b></a> &nbsp;•&nbsp;
    <a href="#-installation--setup"><b>Getting Started</b></a> &nbsp;•&nbsp;
    <a href="#-api-endpoint-reference"><b>API Docs</b></a>
  </p>

</div>

---

## 📌 Executive Overview

**Krishi AI** is an enterprise-grade, multi-modal agronomic intelligence platform designed to eliminate crop yield loss, diagnose plant diseases in real time, and eliminate market opacity for agricultural communities.

By orchestrating **Convolutional Neural Networks (MobileNetV3 / ResNet)** for visual field scans, **Scikit-Learn Ensemble Models** for soil texture and crop-fertilizer recommendations, and **Google Gemini Generative AI** for localized advisory generation, Krishi AI converts a simple smartphone photo into a full agronomical diagnostic report.

> [!TIP]
> ### 💡 30-Second Recruiter & Technical Summary
> - **The Problem:** Smallholder farmers lose up to **40% of crop yields** due to undetected leaf diseases, pest infestations, and unoptimized soil fertilization.
> - **The Architecture:** Asynchronous **FastAPI REST Gateway** running PyTorch neural nets, Scikit-Learn tabular predictors, and LLM reasoning engines with zero-latency response pipelines.
> - **Key Highlights:** Instant visual pathology diagnosis, automated NPK fertilizer deficit calculation, weather-aware irrigation scheduling, live Mandi commodity tracking, and multi-lingual voice output.

---

## 🏛️ System Architecture

Krishi AI utilizes an asynchronous, event-driven microservice architecture powered by **FastAPI**, with strict Pydantic payload validation, RAM/VRAM inference pipelines, and automated fallback guardrails.

```mermaid
flowchart TD
    %% Custom Styling - Cohesive Green-to-Blue Color Grading
    classDef client fill:#064E3B,stroke:#10B981,stroke-width:2px,color:#FFF;
    classDef gateway fill:#0F766E,stroke:#14B8A6,stroke-width:2px,color:#FFF;
    classDef model fill:#047857,stroke:#34D399,stroke-width:2px,color:#FFF;
    classDef external fill:#1E3A8A,stroke:#60A5FA,stroke-width:2px,color:#FFF;

    subgraph ClientLayer ["📱 Frontend Presentation Layer"]
        UI["Glassmorphic Dashboard (HTML5 / CSS3 / ES6 JS)"]:::client
        Geo["Browser Geolocation & Multi-Lang i18n Engine"]:::client
    end

    subgraph GatewayLayer ["⚡ Backend API Gateway (FastAPI)"]
        Router{"FastAPI Endpoint Router"}:::gateway
        Validator["Pydantic Payload Validation & Image Sanitization"]:::gateway
    end

    subgraph InferenceLayer ["🧠 Deep Learning & Machine Learning Engine"]
        DiseaseNet["MobileNetV3 Leaf Pathology Classifier\n(20 Diseases | PyTorch)"]:::model
        PestNet["Entomological Pest Detector\n(102 Species | PyTorch)"]:::model
        SoilNet["Random Forest Soil Texture Vision\n(153 OpenCV Features)"]:::model
        CropML["Scikit-Learn Agronomic Recommender\n(NPK + Climate Vectors)"]:::model
    end

    subgraph ExternalLayer ["🌐 External Intelligence Services"]
        Gemini["Google Gemini LLM\n(Localized Action Plans & Govt. Schemes)"]:::external
        OpenMeteo["Open-Meteo Weather API\n(Real-Time Telemetry)"]:::external
    end

    UI -->|Multipart Upload / JSON| Router
    Geo -->|Coords & i18n Pref| Router
    Router --> Validator
    Validator --> DiseaseNet
    Validator --> PestNet
    Validator --> SoilNet
    Validator --> CropML
    Validator --> Gemini
    Validator --> OpenMeteo

    DiseaseNet -->|Diagnostic Metrics| UI
    PestNet -->|Insect Remedy Vectors| UI
    SoilNet -->|Soil Composition Profile| UI
    CropML -->|Optimal Crop & Fertilizer Matrix| UI
    Gemini -->|Actionable Farm Guidance| UI
    OpenMeteo -->|Live Forecast Inputs| UI
```

### 🔄 Data Orchestration Lifecycle

1. **Presentation Layer (Client)**: User uploads leaf/pest/soil photos or inputs geographic location via the dashboard interface.
2. **API Routing (FastAPI Gateway)**: Sanitizes input payload, validates data shapes via Pydantic, and handles asynchronous requests.
3. **ML Inference Pipeline**: Parallel execution of visual classifiers (PyTorch) and tabular predictors (Scikit-Learn) to output raw analytics vectors.
4. **Context Orchestration**: Aggregates model outputs, live meteorology feeds (Open-Meteo), and market pricing telemetry.
5. **Generative Synthesis (Google Gemini)**: Synthesizes structured agronomic contexts to draft localized action plans, government subsidy matches, and crop advisors.

---

## 🧠 AI & ML Model Pipeline

Krishi AI replaces single-model architectures with a **Hybrid Machine Learning Pipeline**, deploying specialized models fine-tuned for visual, tabular, and conversational domains.

### 📋 Model Specifications

| Layer / Model | Framework / Algorithm | Input Dimensions | Domain & Feature Space Extraction | Guardrail / Confidence Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **1️⃣ Plant Pathology** | `PyTorch MobileNetV3-Large` | Leaf Image `224x224 RGB` | Spatial CNN feature mapping across **20 disease classes** (Blight, Rust, Scab, Mosaic) | Confidence threshold `< 35%` triggers automated re-scan prompt |
| **2️⃣ Entomology Net** | `PyTorch MobileNetV3 Deep` | Pest Image `224x224 RGB` | Deep visual classification across **102 agricultural insect species** mapped to treatment DB | Confidence threshold `< 20%` triggers secondary verification |
| **3️⃣ Soil Classifier** | `Scikit-Learn Random Forest` | Soil Photo `256x256 RGB` | Manual extraction of **153 mathematical features** (96 HSV + 48 LAB + 6 RGB + 3 Sobel Gradients) | Confidence threshold `< 40%` rejects non-soil artifacts |
| **4️⃣ Crop Recommendation** | `Scikit-Learn Random Forest/XGB` | NPK, pH, Temp, Humidity | Multi-variable decision trees matching soil chemistry with optimal crop yield profiles | Hard agronomical deterministic boundary checks |
| **5️⃣ Advisory LLM** | `Google Gemini-1.5-Flash` | Structured JSON Context | Generates localized treatment steps, Mandi price trends, and Govt. scheme eligibility | Strict JSON schema enforcement & XSS sanitization |

---

## 🌟 Core Platform Modules

### 🔬 Multi-Modal Field Diagnostics
*Instant visual crop pathology, pest detection, and soil profiling at the edge.*
- **🌱 Instant Crop Pathology** — Identifies fungal, bacterial, and viral crop infections in milliseconds.
- **🐛 Entomology Engine** — Pinpoints insect species with organic & chemical remedy options.
- **🧪 Soil Vision Profiler** — Estimates soil texture, porosity, and suitability visually.
- **📊 Severity Grading** — Evaluates infection severity to determine urgent vs. standard interventions.

---

### 🌾 Precision Crop & Water Advisory
*Evapotranspiration-based irrigation, NPK deficit chemistry calculation, and TTS translation.*
- **⚖️ NPK Deficit Calculator** — Measures nitrogen, phosphorus, and potassium shortfall per acre with dosage schedules.
- **💧 Smart Irrigation Engine** — Calculates evapotranspiration-based daily watering recommendations.
- **📈 Yield Maximizer** — Recommends high-value alternative cash crops based on soil microclimate.
- **🔊 Voice-Assisted Insights** — Built-in Text-To-Speech (TTS) support for regional language accessibility.

---

### 📈 Mandi Market Intelligence
*Real-time pricing feeds, forecasting charts, and transportation cost calculators.*
- **📊 Live Commodity Tracker** — Tracks real-time price fluctuations across regional agricultural markets (Mandis).
- **📉 Interactive Trend Analytics** — Visualized price forecasting powered by Chart.js.
- **🚚 Arbitrage Analyzer** — Compares local rural Mandis vs. city centers to evaluate net transport profit margins.
- **📅 Harvest Timing Guidance** — Predicts market demand surges to advise on optimal harvest dates.

---

### 📜 Welfare & Subsidy Matcher
*Algorithmic criteria matching, portal links, and emergency guides.*
- **🎯 Automated Eligibility Engine** — Evaluates landholding and crop profiles against PM-KISAN, PMFBY, KUSUM, and regional schemes.
- **🔗 Direct Portal Integration** — Provides direct links to official state and national application portals.
- **📚 Resource Knowledge Base** — Comprehensive repository of agronomical best practices and disaster recovery guides.

---

## 🛠️ Technology Ecosystem

### ⚡ Core Backend
* **FastAPI** <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" /> - Asynchronous REST API serving and request routing.
* **Uvicorn** <img src="https://img.shields.io/badge/Uvicorn-4051B5?style=flat-square&logo=python&logoColor=white" /> - High-performance ASGI web server wrapper.
* **Pydantic** <img src="https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white" /> - Asynchronous payload validation and schema safety.

### 🧠 Neural Vision & Machine Learning
* **PyTorch** <img src="https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white" /> - MobileNetV3 Convolutional Neural Network execution.
* **Scikit-Learn** <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" /> - Tabular machine learning & classifier matrices.
* **OpenCV** <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white" /> - Custom soil vision image feature calculations.

### 🤖 Generative Cognition & Speech
* **Google Gemini API** <img src="https://img.shields.io/badge/Google_Gemini-8E44AD?style=flat-square&logo=google&logoColor=white" /> - Dynamic local-first agronomist advice engine.
* **gTTS** <img src="https://img.shields.io/badge/gTTS-10B981?style=flat-square&logo=python&logoColor=white" /> - Text-to-Speech voice translation for regional farmers.

### 💻 Client Interface
* **HTML5 / CSS3 Glassmorphism** <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" /> <img src="https://img.shields.io/badge/CSS3_Glass-1572B6?style=flat-square&logo=css3&logoColor=white" /> - Interactive, beautiful responsive web dashboards.
* **ES6 JS / Chart.js** <img src="https://img.shields.io/badge/ES6_JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black" /> <img src="https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white" /> - Client state scripting & mandi commodity visual statistics.

### 🌐 Live External APIs
* **Open-Meteo API** <img src="https://img.shields.io/badge/Open--Meteo-0284C7?style=flat-square&logo=icloud&logoColor=white" /> - Evapotranspiration and live climate weather data feeds.
* **AgMarket Feeds** <img src="https://img.shields.io/badge/AgMarket_Feeds-059669?style=flat-square&logo=rss&logoColor=white" /> - Real-time mandi rates from local agricultural yards.

---

## 📂 Project Structure

```text
Krishi-Ai-main/
│
├── ⚡ backend/
│   ├── app/
│   │   ├── routers/            # FastAPI Endpoint Handlers (detection, prediction, advisory, market, schemes)
│   │   ├── services/           # ML Inference Engines & Gemini API Integration
│   │   └── config.py           # Application Settings & Confidence Threshold Guardrails
│   ├── model_store/            # Trained Weights (.h5, .pkl AI Artifacts)
│   └── run.py                  # Server Entrypoint (FastAPI + Uvicorn Async Launcher)
│
├── 💻 frontend/
│   ├── assets/                 # Custom Glassmorphism CSS, JS Drivers (i18n.js, kisaan.js)
│   ├── components/             # Dynamic UI Components (Navbar, Footer, Loader, Modals)
│   ├── vendor/                 # Vendor Assets (Chart.js, AOS.js, SweetAlert2)
│   ├── detection.html          # Plant Disease, Pest & Soil Vision Scanner
│   ├── prediction.html         # Crop Selection & NPK Fertilizer Deficit Calculator
│   ├── advisory.html           # Real-Time Agronomic Action Plan Dashboard
│   ├── market.html             # Mandi Commodity Price Chart Analytics
│   ├── schemes.html            # Government Welfare Subsidy Matcher
│   └── index.html              # Core Landing Page Gateway
│
├── 🛠️ scripts/                 # Utility Scripts (expand_pest_advisory.py)
├── 📦 requirements.txt         # Production Dependencies
└── 📄 README.md                # Platform Documentation
```

---

## ⚡ Installation & Setup

> [!NOTE]
> Ensure you have **Python 3.9+** and **Git** installed on your system before proceeding.

### Setup Wizard

```bash
# 1. Clone the repository and navigate into the workspace
git clone https://github.com/jeswanth90630/Krishi-Ai.git
cd Krishi-Ai-main

# 2. Build the Python virtual sandbox environment
python -m venv .venv

# 3. Activate the environment (Platform Specific)
# For Windows (PowerShell):
.\.venv\Scripts\activate
# For Linux / macOS:
source .venv/bin/activate

# 4. Install standard production requirements
pip install -r requirements.txt

# 5. Install CPU-optimized neural processing engines
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 6. Set project execution variable & Launch application gateway
# Windows (PowerShell):
$env:PYTHONPATH="backend"
python backend/run.py
# Linux / macOS:
PYTHONPATH=backend python backend/run.py
```

> [!SUCCESS]
> The server will start running locally at **`http://127.0.0.1:8000`** 🚀

---

## 📡 API Endpoint Reference

Once the server is running, explore interactive API documentation directly in your browser:

* 📑 **Interactive Swagger UI:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
* 📖 **ReDoc OpenAPI Documentation:** [`http://127.0.0.1:8000/redoc`](http://127.0.0.1:8000/redoc)

### Core Endpoints

* `POST /api/v1/detect/disease` - **Plant Pathology Scan**
  * *Payload / Format:* `multipart/form-data`
  * *Role:* Processes leaf image through MobileNetV3; returns pathology diagnosis & confidence.

* `POST /api/v1/detect/pest` - **Entomology Identification**
  * *Payload / Format:* `multipart/form-data`
  * *Role:* Identifies pest species; returns organic & chemical treatment options.

* `POST /api/v1/detect/soil` - **Soil Texture Vision**
  * *Payload / Format:* `multipart/form-data`
  * *Role:* Extracts 153 OpenCV visual features; predicts soil texture composition.

* `POST /api/v1/predict/crop` - **Crop Selection Predictor**
  * *Payload / Format:* `application/json`
  * *Role:* Analyzes NPK, pH, and microclimate vectors to recommend top 3 optimal crops.

* `POST /api/v1/predict/fertilizer` - **NPK Fertilizer Deficit Calculator**
  * *Payload / Format:* `application/json`
  * *Role:* Calculates NPK shortfall (kg/acre) and outputs custom dosage timeline.

* `GET /api/v1/market/prices` - **Mandi Market Rates**
  * *Payload / Format:* `Query Parameters`
  * *Role:* Returns real-time Mandi market rates and 7-day price trend forecasts.

* `POST /api/v1/schemes/match` - **Welfare & Subsidy Matcher**
  * *Payload / Format:* `application/json`
  * *Role:* Matches landholding profile with government agricultural welfare subsidies.

---

## 🛡️ Operational Safety & Privacy Guardrails

> [!IMPORTANT]
> * **🔒 Ephemeral Processing:** All images uploaded during visual scans are processed strictly in RAM and discarded immediately after inference.
> * **🛡️ Low-Confidence Rejection:** Diagnostic predictions falling below statistical threshold boundaries (e.g., `<35%`) prompt automatic user re-scans to prevent erroneous agricultural treatments.
> * **⚡ Strict Schema Validation:** Generative AI responses pass through deterministic Pydantic validation schemas to safeguard against hallucinated outputs.

---

<div align="center">

  <br/>

  <h3>🌾 Krishi AI — <i>Architecting the Future of Precision Agriculture</i></h3>
  <p><b>Engineered with 💚 for Farming Ecosystems Worldwide</b></p>

  <br/>

  <a href="#-krishi-ai">
    <img src="https://img.shields.io/badge/Back_to_Top-%E2%86%91-10B981?style=for-the-badge" alt="Back to Top" />
  </a>

  <br/>
  <br/>

</div>
