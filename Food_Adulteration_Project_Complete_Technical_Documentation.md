# Food Adulteration & Quality Detection System
## Complete Technical Architecture and Codebase Documentation

---

### Document Overview
This document provides an exhaustive, source-code-verified breakdown of the **Food Adulteration & Food Quality Detection System** codebase. Every technology, route, schema, model, dataset, and algorithm described herein has been empirically verified from the project repository (`aakashsatyamjha/FoodAdulterationSystem`).

---

## 1. Executive Summary

### 1.1 Project Purpose & Problem Statement
Modern packaged food products frequently contain toxic chemical adulterants, excessive synthetic additives, unlabeled allergens, and harmful trans-fats. Consumer protection regulations vary significantly across global jurisdictions (e.g., additives permitted under US FDA may be banned by the European Union or Indian FSSAI). 

The **Food Adulteration & Food Quality Detection System** addresses this critical public health issue by providing a multi-criteria safety evaluation platform that combines:
1. **Optical Character Recognition (OCR)** for ingredient label scanning.
2. **Real-time GTIN Barcode Decoding** for instant product identification.
3. **Machine Learning Quality Scoring** (Gradient Boosting Classifier @ 99.86% accuracy).
4. **5-Country Statutory Regulatory Auditing** (India, USA, EU, Germany, UK).
5. **Personalized Consumer Dietary Risk Assessment** (Diabetic, Hypertensive, Vegan, Gluten-Free, etc.).

### 1.2 Target Users
* **Everyday Consumers:** Seeking rapid, non-technical health risk scores for packaged items.
* **Dietary-Sensitive Individuals:** Managing Diabetes, Hypertension, Celiac Disease, or Food Allergies.
* **Food Inspectors & Compliance Officers:** Auditing ingredient formulations against statutory country matrices.
* **Researchers & Students:** Benchmarking ML algorithms (Gradient Boosting, Random Forest) on food quality datasets.

### 1.3 Key Architectural Capabilities
1. **Multi-Modal Input:** Supports raw ingredient text, camera/upload label image OCR, and GTIN barcode scanning.
2. **4-Pillar Decision Engine:** Unifies Adulterant Screening, ML Scoring, Regulatory Auditing, and Consumer Personalization.
3. **5-Country Regulatory Matrix:** Compares ingredient legal status across India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), and UK (FSA).
4. **Offline / Hybrid Resilience:** Uses OpenFoodFacts REST API with a local rich offline catalog fallback.
5. **Deterministic AI Chatbot:** Natural language assistant querying internal ingredient intelligence without third-party API dependencies.

---

## 2. Complete Project Folder Structure

```
FINALYEARPROJECT/
├── api/
│   └── index.py                      # Vercel serverless gateway entrypoint
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── adulteration_service.py   # Regex chemical dye & adulterant screening engine
│   │   │   ├── chat_service.py           # Ingredient knowledge-base NLP chatbot handler
│   │   │   ├── consumer_service.py       # Personal dietary risk evaluation engine
│   │   │   ├── decision_engine.py        # Master 4-Pillar safety evaluation orchestrator
│   │   │   ├── fssai_service.py          # FSSAI statutory standards & regulations service
│   │   │   ├── ingredient_intelligence.py# Master ingredient database (~39 E-numbers/INS)
│   │   │   ├── ocr_service.py            # OpenCV computer vision preprocessor & Tesseract OCR
│   │   │   ├── openfoodfacts_service.py  # Barcode resolution (OpenFoodFacts API + Offline Catalog)
│   │   │   └── regulatory_service.py     # 5-Country statutory compliance matrix builder
│   │   ├── database.py               # SQLAlchemy SQLite engine & session factory
│   │   ├── main.py                   # FastAPI app routes, CORS, middleware, & lifecycle
│   │   ├── models.py                 # SQLAlchemy ORM ScanRecord model
│   │   ├── mongo_db.py               # PyMongo MongoDB Atlas integration & CRUD
│   │   └── schemas.py                # Pydantic data validation & response models
│   ├── db/
│   │   └── food_quality.db           # SQLite database file (scan_history table)
│   ├── ml/
│   │   ├── data/
│   │   │   └── food_products_dataset.csv # 3,500 samples ML dataset (16 features)
│   │   ├── models/
│   │   │   ├── best_food_quality_model.joblib # Serialized GradientBoosting + StandardScaler
│   │   │   └── model_comparison_metrics.json  # Benchmarking metrics across 4 algorithms
│   │   ├── dataset_generator.py      # Synthetic dataset generator script
│   │   ├── predict.py                # ML inference singleton wrapper
│   │   └── train_models.py           # ML training, cross-validation & evaluation script
│   ├── test_backend.py               # FastAPI TestClient integration test suite
│   └── test_scores.py                # Decision engine score unit test suite
├── frontend/
│   ├── public/
│   │   ├── favicon.svg               # Application icon
│   │   └── icons.svg                 # SVG sprite icons
│   ├── src/
│   │   ├── assets/                   # Static images (hero.png, vite.svg, react.svg)
│   │   ├── components/
│   │   │   ├── Chatbot.jsx           # Floating AI Chatbot modal component
│   │   │   ├── Header.jsx            # Top navigation bar component
│   │   │   ├── HelpModal.jsx         # User user-guide modal dialog
│   │   │   ├── Navbar.jsx            # Secondary navigation bar
│   │   │   ├── SettingsModal.jsx     # User settings modal dialog
│   │   │   ├── Sidebar.jsx           # Navigation drawer sidebar
│   │   │   └── SplashAnimation.jsx    # Application startup splash loader
│   │   ├── context/
│   │   │   ├── AuthContext.jsx       # Client-side user auth state (localStorage)
│   │   │   └── ThemeContext.jsx      # Light / Dark theme context provider
│   │   ├── pages/
│   │   │   ├── AuthPage.jsx          # Login & registration view
│   │   │   ├── BarcodeScanner.jsx    # Real-time camera barcode scanner view
│   │   │   ├── ConsumerIntelligence.jsx# Health profile & allergy manager view
│   │   │   ├── Home.jsx              # Dashboard home page view
│   │   │   ├── IngredientScanner.jsx # OCR label scanner & image upload view
│   │   │   ├── LandingPage.jsx       # Public landing page view
│   │   │   ├── ModelExplorer.jsx     # Interactive ML algorithm benchmark view
│   │   │   ├── ProductAnalysis.jsx   # Multi-pillar detailed audit report view
│   │   │   ├── RegulatoryIntelligence.jsx # 5-Country statutory matrix explorer view
│   │   │   └── ScanHistory.jsx       # Historical scan record log view
│   │   ├── utils/
│   │   │   └── pdfGenerator.js       # Client-side jsPDF audit report generator
│   │   ├── App.css                   # Global component styles
│   │   ├── App.jsx                   # React root router & layout component
│   │   ├── index.css                 # Tailwind CSS v4 directives
│   │   └── main.jsx                  # DOM entrypoint
│   ├── index.html                    # Single-page HTML document
│   ├── package.json                  # Node.js dependencies & scripts
│   ├── vite.config.js                # Vite build configuration
│   └── vercel.json                   # Frontend deployment settings
├── .env                              # Active environment variables
├── .env.example                      # Template environment variables
├── README.md                         # Project documentation overview
├── requirements.txt                  # Python dependencies
├── run_backend.bat                   # Windows batch script for backend startup
├── run_frontend.bat                  # Windows batch script for frontend startup
├── run_server.py                     # Uvicorn backend launcher script
└── vercel.json                       # Root Vercel routing configuration
```

---

## 3. Complete File-by-File Explanation

| File Path | Type | Purpose & Responsibilities | Inputs / Outputs | Used By |
| :--- | :--- | :--- | :--- | :--- |
| **backend/app/main.py** | Python (FastAPI) | Central REST API gateway, router definitions, CORS middleware, DB lifecycle. | HTTP Requests -> JSON / HTTP Errors | Frontend Client |
| **backend/app/database.py** | Python (SQLAlchemy) | Creates SQLite engine (`food_quality.db`), SessionLocal factory, and Base. | DB Path -> Session Object | `main.py`, `models.py` |
| **backend/app/models.py** | Python (ORM) | Defines `ScanRecord` SQLAlchemy model mapped to `scan_history` table. | Python Objects -> DB Rows | `main.py`, `database.py` |
| **backend/app/schemas.py** | Python (Pydantic) | Defines 12 Pydantic schemas for request validation and response serialization. | Raw Dicts -> Validated Models | `main.py`, `decision_engine.py` |
| **backend/app/mongo_db.py** | Python (PyMongo) | MongoDB Atlas connection helper and CRUD functions for cloud scan log backup. | Scan Dict -> Mongo Doc ID | `main.py` |
| **backend/app/services/adulteration_service.py** | Python (Service) | Regex pattern matcher for 12+ toxic adulterants (Metanil Yellow, Sudan Dyes, etc.). | Ingredient String -> Risk Flags | `decision_engine.py` |
| **backend/app/services/chat_service.py** | Python (Service) | Rule-based NLP engine for AI Chatbot querying `ingredient_intelligence` database. | Query + Context -> Bot Response | `main.py` (/api/chat) |
| **backend/app/services/consumer_service.py** | Python (Service) | Evaluates food formulation against 8 personalized health profiles (Diabetic, Vegan). | Ingredients + Prefs -> Suitability | `decision_engine.py` |
| **backend/app/services/decision_engine.py** | Python (Engine) | Master orchestrator executing 4-pillar evaluation & calculating unified health score. | Request -> Full Safety Report | `main.py` (/api/analyze) |
| **backend/app/services/fssai_service.py** | Python (Service) | Provides FSSAI statutory standards, regulation guidelines, and licensing rules. | Category -> Standards Dict | `decision_engine.py` |
| **backend/app/services/ingredient_intelligence.py** | Python (Knowledge) | Master ingredient database of ~39 E-numbers/INS codes with statutory approval matrix. | Ingredient Name -> E-Number Meta | All Services |
| **backend/app/services/ocr_service.py** | Python (CV / OCR) | OpenCV preprocessor (CLAHE, bilateral filter, thresholding) & Tesseract OCR engine. | Image Bytes -> Extracted Text | `main.py` (/api/ocr) |
| **backend/app/services/openfoodfacts_service.py** | Python (Service) | Fetches GTIN barcode metadata from OpenFoodFacts REST API with offline fallback catalog. | Barcode -> Product Meta Dict | `main.py` (/api/barcode) |
| **backend/app/services/regulatory_service.py** | Python (Service) | Evaluates ingredients against 5 jurisdictions (India, USA, EU, Germany, UK). | Ingredients -> 5-Country Matrix | `decision_engine.py` |
| **backend/ml/dataset_generator.py** | Python (Script) | Generates 3,500 food product training samples with 16 features into CSV format. | Seed Rules -> Dataset CSV | Developer / Trainer |
| **backend/ml/train_models.py** | Python (Training) | Benchmarks 4 algorithms (Logistic Reg, Decision Tree, Random Forest, Gradient Boosting). | Dataset CSV -> Joblib Binary | Developer / Trainer |
| **backend/ml/predict.py** | Python (Inference) | Singleton class `FoodQualityPredictor` loading `best_food_quality_model.joblib`. | Feature Vector -> Risk & Score | `decision_engine.py` |
| **backend/ml/data/food_products_dataset.csv** | Dataset (CSV) | 3,500 rows x 16 columns ML training dataset containing nutritional & additive attributes. | Tabular Data -> Model Input | `train_models.py` |
| **backend/ml/models/best_food_quality_model.joblib** | Model Artifact | Serialized dictionary containing trained GradientBoostingClassifier and StandardScaler. | Binary Object -> In-Memory Model | `predict.py` |
| **frontend/src/App.jsx** | React Component | Main application layout, React Router configuration, modal state management. | URL Route -> Rendered UI View | `main.jsx` |
| **frontend/src/context/AuthContext.jsx** | React Context | Manages client-side authentication state and localStorage user token persistence. | User Credentials -> Auth State | App UI |
| **frontend/src/pages/IngredientScanner.jsx** | React View | Interface for ingredient image capture, file upload, and backend OCR trigger. | Image -> Extracted Text | `App.jsx` |
| **frontend/src/pages/BarcodeScanner.jsx** | React View | Real-time web camera GTIN barcode scanning using `html5-qrcode` library. | Camera Stream -> Product Dict | `App.jsx` |
| **frontend/src/pages/ProductAnalysis.jsx** | React View | Detailed safety audit report view displaying 4-pillar scores & 5-country matrix. | Full Safety Report -> UI Render | `App.jsx` |
| **frontend/src/utils/pdfGenerator.js** | JavaScript Utility | Client-side PDF report generator using `jsPDF` and `jsPDF-AutoTable`. | Report Dict -> Downloadable PDF | `ProductAnalysis.jsx` |

---

## 4. Technology Stack

### 4.1 Frontend / UI
* **Framework:** React v19.2.8 + Vite v6.2.0 (Single Page Application, Fast HMR)
* **Styling:** Tailwind CSS v4.3.3 (`@tailwindcss/vite`) + Lucide Icons v1.39
* **Camera / Barcode Library:** `html5-qrcode v2.3.8` (WebRTC HTML5 video stream EAN-13 decoding)
* **Browser OCR:** `Tesseract.js v7.0.0` (Client-side WebAssembly OCR fallback)
* **PDF Export:** `jsPDF v4.2.1` + `jsPDF-AutoTable v5.0.8`

### 4.2 Backend & API Architecture
* **Framework:** FastAPI >= 0.100.0 (Python 3.10+)
* **ASGI Web Server:** Uvicorn >= 0.22.0
* **Data Validation:** Pydantic v2.0.0
* **CORS Middleware:** `CORSMiddleware` (Configured in `main.py`)

### 4.3 Databases & ORM
* **Relational Database:** SQLite3 (`backend/db/food_quality.db`)
* **ORM:** SQLAlchemy v2.0.0 (`backend/app/database.py`, `backend/app/models.py`)
* **NoSQL Cloud Backup:** MongoDB Atlas (`food_quality_db`, collection `scans`) via PyMongo v4.0+

### 4.4 Machine Learning Stack
* **Core Libraries:** Scikit-Learn v1.2.0, NumPy v1.24.0, Pandas v2.0.0
* **Algorithms Benchmarked:** Logistic Regression, Decision Tree Classifier, Random Forest Classifier, **Gradient Boosting Classifier (Best Model)**
* **Model Persistence:** Joblib v1.3.0 (`best_food_quality_model.joblib`)

### 4.5 Computer Vision & OCR
* **Image Processing:** OpenCV (`opencv-python-headless v4.8.0`), Pillow v10.0.0
* **Native OCR Engine:** Pytesseract v0.3.10 + Tesseract-OCR binary engine

---

## 5. System Architecture & Diagram

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                               CLIENT LAYER (React 19 + Vite)                           │
│  [ Ingredient Scanner ]       [ Barcode Scanner ]      [ Model Explorer ] [ AI Chat ]  │
│   (Camera / File Upload)      (html5-qrcode GTIN)      (Metrics Dashboard) (NLP UI)    │
└──────────────┬──────────────────────────┬───────────────────────┬──────────────┬───────┘
               │                          │                       │              │
               ▼                          ▼                       ▼              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                             REST API GATEWAY (FastAPI / Uvicorn)                       │
│  POST /api/ocr              GET /api/barcode/{id}   GET /api/models/metrics POST /api/chat│
└──────────────┬──────────────────────────┬───────────────────────┬──────────────┬───────┘
               │                          │                       │              │
               ▼                          ▼                       │              │
┌──────────────────────────────────────────────────┐              │              │
│        INGESTION & PREPROCESSING MODULE          │              │              │
│  • OpenCV CV Filter (CLAHE + Adaptive Thresh)    │              │              │
│  • Pytesseract OCR Engine -> Text Normalization  │              │              │
│  • OpenFoodFacts REST API + Offline Catalog Fallback            │              │
└──────────────────────────────┬───────────────────┘              │              │
                               │                                  │              │
                               ▼                                  ▼              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      MASTER DECISION ENGINE (decision_engine.py)                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │ PILLAR 1:         │  │ PILLAR 2:        │  │ PILLAR 3:        │  │ PILLAR 4:      │  │
│  │ Adulterant        │  │ ML Quality       │  │ 5-Country        │  │ Consumer       │  │
│  │ Screening         │  │ Predictor        │  │ Statutory Matrix │  │ Personal Risk  │  │
│  │ (Regex Patterns)  │  │ (GradientBoost)  │  │ (FSSAI/FDA/EFSA) │  │ (8 Profiles)   │  │
│  └─────────┬────────┘  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘  │
└────────────┼────────────────────┼─────────────────────┼────────────────────┼───────────┘
             ▼                    ▼                     ▼                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                DATABASE & PERSISTENCE TIER                              │
│   • SQLite3 (backend/db/food_quality.db)  -->  ScanRecord Table (SQLAlchemy ORM)        │
│   • MongoDB Atlas (food_quality_db)       -->  Cloud Backup Scans Collection            │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Authentication & Authorization Trace

> [!CAUTION]
> **CODEBASE VERIFICATION FINDING:** Inspection of `backend/app/main.py`, `backend/app/models.py`, and `backend/app/schemas.py` confirms that **NO backend authentication endpoints or user database tables exist in the Python backend**. There are no `/api/auth/login` routes, no bcrypt password hashing, and no JWT middleware in Python.

### Actual Client-Side Implementation (`AuthContext.jsx`)
1. **Registration:** User submits email/password in `AuthPage.jsx`. `AuthContext` creates a mock user object with a synthetic token string (`'mock-jwt-token-xyz...'`) and saves it to browser `localStorage` under key `'food_app_user'`.
2. **Login:** `AuthContext` reads credentials, validates non-empty strings, and updates the reactive `user` state object.
3. **Persistence:** `useEffect` reads `localStorage.getItem('food_app_user')` on page refresh to restore state.
4. **Logout:** Invoking `logout()` clears `user` state and removes key from `localStorage`.
5. **Protected Routes:** Handled in React Router. Redirects unauthenticated users to `/auth`.

---

## 7. Database Architecture & Schemas

### 7.1 SQLite Table Schema: `scan_history`
* **File Location:** `backend/db/food_quality.db`
* **Model Class:** `ScanRecord` (`backend/app/models.py`)

| Column Name | Data Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | Primary Key (Autoincrement) | Unique record ID |
| `product_name` | `VARCHAR(255)` | Nullable | Product name or 'Scanned Label' |
| `brand` | `VARCHAR(255)` | Nullable | Brand / Manufacturer |
| `barcode` | `VARCHAR(64)` | Indexed | 13-digit GTIN / EAN barcode string |
| `scan_type` | `VARCHAR(64)` | NotNull | Scan method (`barcode`, `ocr`, `manual`) |
| `category` | `VARCHAR(128)` | Nullable | Food category (e.g., Noodles, Dairy) |
| `quality_score` | `INTEGER` | NotNull | Dynamic ML safety score (0 to 100) |
| `risk_level` | `VARCHAR(64)` | NotNull | Risk classification (`Low`, `Moderate`, `High`) |
| `ingredients` | `TEXT` | Nullable | Comma-separated raw ingredient text |
| `adulteration_flags` | `TEXT (JSON)` | Nullable | Serialized list of adulterants detected |
| `concerning_additives` | `TEXT (JSON)` | Nullable | Serialized list of concerning E-numbers |
| `allergens` | `TEXT (JSON)` | Nullable | Serialized list of allergen strings |
| `nutritional_data` | `TEXT (JSON)` | Nullable | Serialized dict of macros (sugar, sodium) |
| `image_url` | `VARCHAR(512)` | Nullable | Image path / URL string |
| `explanation` | `TEXT` | Nullable | Textual audit justification summary |
| `created_at` | `DATETIME` | Default: `utcnow` | Audit execution timestamp |

### 7.2 Cloud Backup: MongoDB Atlas
`backend/app/mongo_db.py` uses PyMongo to connect to `MONGODB_URI`. When scans complete, `save_mongo_scan()` asynchronously inserts the record into the `scans` collection in `food_quality_db`. If MongoDB connection fails, the system safely continues using SQLite.

---

## 8. Dataset Documentation & Inventory

### Primary Dataset: `food_products_dataset.csv`
* **Location:** `backend/ml/data/food_products_dataset.csv`
* **Rows:** 3,500 rows | **Columns:** 16 columns | **Format:** CSV (UTF-8)

| Feature Column Name | Data Type | Domain Range | Description & Formula |
| :--- | :--- | :--- | :--- |
| `energy_kcal` | Float64 | 10.0 to 900.0 | Energy density per 100g serving |
| `sugar_g` | Float64 | 0.0 to 80.0 | Total sugar content in grams per 100g |
| `sodium_mg` | Float64 | 5.0 to 3500.0 | Sodium content in milligrams per 100g |
| `saturated_fat_g` | Float64 | 0.0 to 45.0 | Saturated fatty acids in grams per 100g |
| `trans_fat_g` | Float64 | 0.0 to 10.0 | Trans-fatty acids in grams per 100g |
| `protein_g` | Float64 | 0.0 to 50.0 | Dietary protein in grams per 100g |
| `fiber_g` | Float64 | 0.0 to 30.0 | Dietary fiber in grams per 100g |
| `additives_count` | Int64 | 0 to 15 | Total count of food additives present |
| `artificial_colors_count` | Int64 | 0 to 5 | Count of synthetic food dyes |
| `artificial_sweeteners_count` | Int64 | 0 to 4 | Count of artificial sweeteners |
| `preservatives_count` | Int64 | 0 to 6 | Count of chemical preservatives |
| `is_suspected_adulterant` | Int64 | 0 or 1 | 1 if toxic adulterant detected, else 0 |
| `sugar_to_fiber_ratio` | Float64 | 0.0 to 80.0 | Derived: `sugar_g / (fiber_g + 1e-5)` |
| `additive_density` | Float64 | 0.0 to 0.15 | Derived: `additives_count / (energy_kcal + 1)` |
| `bad_fat_index` | Float64 | 0.0 to 65.0 | Derived: `saturated_fat_g + 2 * trans_fat_g` |
| `health_risk_level` [TARGET] | Categorical | Low/Moderate/High | Target class for ML model classification |

---

## 9. Machine Learning Pipeline & Training

### 9.1 Model Benchmark Results (`model_comparison_metrics.json`)

| Algorithm Name | Accuracy | Precision | Recall | F1-Score | Selection Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting Classifier** | **99.86%** | **0.9986** | **0.9986** | **0.9986** | **SELECTED BEST MODEL** |
| Random Forest Classifier | 99.71% | 0.9972 | 0.9971 | 0.9971 | Runner-Up |
| Decision Tree Classifier | 99.43% | 0.9943 | 0.9943 | 0.9943 | Baseline Tree |
| Logistic Regression | 98.57% | 0.9859 | 0.9857 | 0.9857 | Linear Baseline |

### 9.2 Confusion Matrix (Gradient Boosting Classifier)
Out of 700 test samples, Gradient Boosting misclassified only **1 sample**:
```
Actual \ Predicted    Low Risk    Moderate Risk    High Risk
Low Risk               297               0              0
Moderate Risk            0             200              1  (1 sample misclassified)
High Risk                0               0            202
```

### 9.3 Top Predictive Feature Importance Weights
1. **`is_suspected_adulterant`**: 46.87% weight
2. **`additive_density`**: 28.72% weight
3. **`preservatives_count`**: 9.03% weight
4. **`sodium_mg`**: 4.18% weight
5. **`sugar_g`**: 3.90% weight

---

## 10. 5-Country Regulatory Compliance Matrix

| E-Number / Additive Name | India (FSSAI) | USA (FDA) | EU (EFSA) | Germany (BVL) | UK (FSA) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **E102 (Tartrazine)** | Restricted (100ppm) | Approved (FD&C Yellow 5) | Warning Label Req. | Strictly Controlled | Warning Label Req. |
| **E110 (Sunset Yellow FCF)** | Restricted (100ppm) | Approved (FD&C Yellow 6) | Banned in Soft Drinks | Strictly Controlled | Warning Label Req. |
| **E127 (Erythrosine)** | Restricted | Banned in Cosmetics | Banned except Cherries | Banned except Cherries | Restricted |
| **E171 (Titanium Dioxide)** | Under Review | Approved (<1%) | **BANNED (2022)** | **BANNED** | Under Review |
| **E211 (Sodium Benzoate)** | Restricted | GRAS (<0.1%) | Restricted | Restricted | Restricted |
| **E951 (Aspartame)** | Warning Label Req. | Approved | Under Review (IARC 2B) | Under Review | Approved |

---

## 11. Complete REST API Endpoint Documentation

| Method | Route Endpoint | Purpose & Function | Auth | Request Body / Params | Response Model |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Root API health ping | None | None | Welcome JSON |
| `GET` | `/api/health` | System health & ML status | None | None | Status & Model Dict |
| `POST` | `/api/analyze` | Executes 4-pillar safety audit | None | `AnalyzeProductRequest` JSON | `FullFoodSafetyReport` |
| `POST` | `/api/ocr` | Extracts text from label image | None | `UploadFile` image bytes | OCR Text Dict |
| `GET` | `/api/barcode/{code}` | Resolves barcode product | None | `code` (path param) | Product Meta Dict |
| `GET` | `/api/barcodes/sample` | Lists sample offline barcodes | None | None | List of Barcodes |
| `POST` | `/api/chat` | AI Chatbot query handler | None | `ChatRequest` JSON | Bot Response JSON |
| `POST` | `/api/consumer-evaluation` | Evaluates dietary profile fit | None | `ConsumerEvalRequest` JSON | Profile Suitability Dict |
| `GET` | `/api/ingredients/search` | Ingredient database query | None | `q` (query param) | List of Ingredients |
| `GET` | `/api/regulatory/matrix` | 5-Country compliance grid | None | None | 5-Country Matrix Dict |
| `GET` | `/api/history` | Retrieves scan audit logs | None | `limit` (query param) | List of `ScanHistoryItem` |
| `GET` | `/api/history/{scan_id}` | Retrieves single scan log | None | `scan_id` (path param) | `ScanHistoryItem` JSON |
| `GET` | `/api/models/metrics` | Returns ML benchmark JSON | None | None | Model Metrics JSON |

---

## 12. Quick Project Map (Cheat Sheet)

| Requirement | Responsible File / Module | Dataset / Model / API | Output Artifact |
| :--- | :--- | :--- | :--- |
| **User Login / Auth** | `frontend/src/context/AuthContext.jsx` | `localStorage` (`food_app_user`) | Client Auth State |
| **Label Image Upload** | `frontend/src/pages/IngredientScanner.jsx` | HTML5 File / Camera API | Uploaded File Bytes |
| **OCR Text Extraction** | `backend/app/services/ocr_service.py` | OpenCV + Pytesseract / Tesseract.js | Cleaned Text String |
| **Barcode Resolution** | `backend/app/services/openfoodfacts_service.py` | OpenFoodFacts REST / Offline Catalog | Product Meta Dict |
| **Adulterant Screening** | `backend/app/services/adulteration_service.py` | Regex Pattern Database | Adulterant Flags |
| **ML Quality Scoring** | `backend/ml/predict.py` | `best_food_quality_model.joblib` | Quality Score (0-100) |
| **5-Country Audit** | `backend/app/services/regulatory_service.py` | `ingredient_intelligence.py` Matrix | 5-Country Status Grid |
| **Consumer Risk Check** | `backend/app/services/consumer_service.py` | 8 Profile Rules Database | Personal Suitability |
| **AI Chatbot Queries** | `backend/app/services/chat_service.py` | Ingredient Intelligence Database | Bot Response JSON |
| **Scan History Logs** | `backend/app/database.py` & `models.py` | `backend/db/food_quality.db` | `ScanRecord` Rows |
| **PDF Report Export** | `frontend/src/utils/pdfGenerator.js` | `jsPDF` + `jsPDF-AutoTable` | Downloadable PDF |

---
