import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Skip on Cover Page)
        if self._pageNumber > 1:
            self.drawString(54, 750, "FOODGUARD AI PLATFORM — SYSTEM ARCHITECTURE & TECHNICAL SPECIFICATIONS")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
            # Footer
            self.setFont("Helvetica", 8)
            self.drawString(54, 36, "Confidential — Final Year Academic & Technical Report")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(558, 36, page_text)
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 46, 558, 46)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Dark Slate
    ACCENT = colors.HexColor("#059669")     # Emerald Green
    SECONDARY = colors.HexColor("#2563EB")  # Royal Blue
    TEXT_DARK = colors.HexColor("#1E293B")  # Charcoal
    BG_LIGHT = colors.HexColor("#F8FAFC")   # Light Gray
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        alignment=TA_LEFT,
        spaceAfter=10
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        alignment=TA_LEFT,
        spaceAfter=20
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=TA_LEFT
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=TEXT_DARK,
        alignment=TA_LEFT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=PRIMARY,
        alignment=TA_LEFT
    )

    story = []

    # ---------------------------------------------------------
    # COVER / HEADER BANNER
    # ---------------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("FOODGUARD AI PLATFORM", title_style))
    story.append(Paragraph("System Architecture, Folder Classification & Technical Implementation Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=5, spaceAfter=15))

    story.append(Paragraph("<b>Executive Summary:</b> FoodGuard AI is a comprehensive, multi-layered food safety intelligence platform. It integrates Computer Vision OCR, EAN-13 Barcode Scanning, Machine Learning Quality Scoring (Gradient Boosting Classifier), 5-Country Statutory Regulation (India FSSAI, USA FDA, EU EFSA, Germany BVL, UK FSA), and Personalized Consumer Health Guidance into a unified React + FastAPI architecture.", body_style))
    story.append(Spacer(1, 10))

    # ---------------------------------------------------------
    # SECTION 1: COMPLETE FOLDER & FILE CLASSIFICATION
    # ---------------------------------------------------------
    story.append(Paragraph("1. Complete Codebase Folder & File Classification", h1_style))
    story.append(Paragraph("The codebase is structured into a decoupled client-server model. Below is the exhaustive classification of every directory and file in the system:", body_style))

    folder_data = [
        [
            Paragraph("Folder / Path", table_header_style),
            Paragraph("File Name", table_header_style),
            Paragraph("Role & Primary Responsibility", table_header_style)
        ],
        # Root Files
        [Paragraph("<b>Root</b>", table_cell_bold), Paragraph("run_server.py", table_cell_style), Paragraph("Local server startup script initializing FastAPI Uvicorn engine on port 8000.", table_cell_style)],
        [Paragraph("<b>Root</b>", table_cell_bold), Paragraph("requirements.txt", table_cell_style), Paragraph("Python package dependencies list for backend (FastAPI, scikit-learn, OpenCV, Pillow, PyTesseract).", table_cell_style)],
        [Paragraph("<b>Root</b>", table_cell_bold), Paragraph("vercel.json", table_cell_style), Paragraph("Vercel production configuration handling SPA route rewrites and API proxies to Render backend.", table_cell_style)],
        [Paragraph("<b>Root</b>", table_cell_bold), Paragraph(".gitignore", table_cell_style), Paragraph("Version control exclusion rule definitions (ignoring node_modules, __pycache__, .env, database files).", table_cell_style)],
        [Paragraph("<b>Root / api</b>", table_cell_bold), Paragraph("api/index.py", table_cell_style), Paragraph("Vercel Python serverless function entrypoint exposing FastAPI instance.", table_cell_style)],
        
        # Backend Core
        [Paragraph("<b>backend/app/</b>", table_cell_bold), Paragraph("main.py", table_cell_style), Paragraph("Core FastAPI application file containing CORS middleware, route handlers (/api/analyze/full, /api/barcode, /api/ocr/extract, /api/history).", table_cell_style)],
        [Paragraph("<b>backend/app/</b>", table_cell_bold), Paragraph("database.py", table_cell_style), Paragraph("SQLAlchemy ORM database engine setup and SessionLocal session lifecycle management.", table_cell_style)],
        [Paragraph("<b>backend/app/</b>", table_cell_bold), Paragraph("models.py", table_cell_style), Paragraph("SQLAlchemy database schema models (ScanRecord, AuditTrail, UserPreference).", table_cell_style)],
        [Paragraph("<b>backend/app/</b>", table_cell_bold), Paragraph("schemas.py", table_cell_style), Paragraph("Pydantic request/response payload validation schemas.", table_cell_style)],
        [Paragraph("<b>backend/app/</b>", table_cell_bold), Paragraph("mongo_db.py", table_cell_style), Paragraph("MongoDB PyMongo client integration for non-relational scan log archival.", table_cell_style)],

        # Backend Services
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("decision_engine.py", table_cell_style), Paragraph("Central orchestrator unifying all 4 pillars, computing quality scores (0-100), generating score deduction arrays, and executing 5-country pre-evaluations.", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("adulteration_service.py", table_cell_style), Paragraph("Screening engine for illegal dye adulterants (Rhodamine B, Metanil Yellow, Sudan Dyes), trans-fat violations, and heavy metals.", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("ingredient_intelligence.py", table_cell_style), Paragraph("Standardized food additive database (~39 E-numbers/INS codes) with per-country regulatory status codes (IN, US, EU, DE, UK).", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("regulatory_service.py", table_cell_style), Paragraph("Cross-border statutory engine evaluating matched ingredients against country authority rules (FSSAI, FDA, EFSA, BVL, FSA).", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("consumer_service.py", table_cell_style), Paragraph("Consumer personalization engine filtering ingredients against dietary profiles (Diabetic, Hypertensive, Vegan, Gluten-Free).", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("ocr_service.py", table_cell_style), Paragraph("Computer Vision & OCR preprocessing service (OpenCV grayscale, CLAHE contrast enhancement, Otsu thresholding, Tesseract extraction).", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("openfoodfacts_service.py", table_cell_style), Paragraph("External Barcode API client with offline local catalog fallback for instant product nutritional resolution.", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("chat_service.py", table_cell_style), Paragraph("AI Safety Assistant chatbot service responding to statutory & ingredient safety queries.", table_cell_style)],
        [Paragraph("<b>backend/app/services/</b>", table_cell_bold), Paragraph("fssai_service.py", table_cell_style), Paragraph("FSSAI regulatory rule compliance lookup and statutory guideline provider.", table_cell_style)],

        # Machine Learning
        [Paragraph("<b>backend/ml/</b>", table_cell_bold), Paragraph("dataset_generator.py", table_cell_style), Paragraph("Synthetic food product dataset generation script outputting food_products_dataset.csv.", table_cell_style)],
        [Paragraph("<b>backend/ml/</b>", table_cell_bold), Paragraph("train_models.py", table_cell_style), Paragraph("Model training pipeline comparing Logistic Regression, Decision Tree, Random Forest, and Gradient Boosting.", table_cell_style)],
        [Paragraph("<b>backend/ml/</b>", table_cell_bold), Paragraph("predict.py", table_cell_style), Paragraph("Production ML inference module wrapping trained Gradient Boosting joblib model.", table_cell_style)],
        [Paragraph("<b>backend/ml/models/</b>", table_cell_bold), Paragraph("best_food_quality_model.joblib", table_cell_style), Paragraph("Serialized trained Gradient Boosting Machine Learning model artifact.", table_cell_style)],
        [Paragraph("<b>backend/ml/data/</b>", table_cell_bold), Paragraph("food_products_dataset.csv", table_cell_style), Paragraph("Training dataset containing multi-parameter food composition records.", table_cell_style)],

        # Frontend Application
        [Paragraph("<b>frontend/src/</b>", table_cell_bold), Paragraph("App.jsx", table_cell_style), Paragraph("Main React SPA component managing global view navigation ('auth', 'app'), sessionStorage state persistence, and active tab rendering.", table_cell_style)],
        [Paragraph("<b>frontend/src/</b>", table_cell_bold), Paragraph("main.jsx", table_cell_style), Paragraph("React DOM entrypoint wrapping App with AuthProvider and ThemeProvider.", table_cell_style)],
        [Paragraph("<b>frontend/src/context/</b>", table_cell_bold), Paragraph("AuthContext.jsx", table_cell_style), Paragraph("User authentication state context (handling login, logout, inspector profile).", table_cell_style)],
        [Paragraph("<b>frontend/src/context/</b>", table_cell_bold), Paragraph("ThemeContext.jsx", table_cell_style), Paragraph("Dark/Light mode UI theme context.", table_cell_style)],
        
        # Frontend Pages
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("LandingPage.jsx", table_cell_style), Paragraph("Public marketing & hero landing page highlighting platform features.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("AuthPage.jsx", table_cell_style), Paragraph("Inspector Sign In & Authentication screen.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("Home.jsx", table_cell_style), Paragraph("Main Dashboard displaying key metrics, audit trail history, and sample product cards.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("BarcodeScanner.jsx", table_cell_style), Paragraph("Camera EAN-13 barcode scanning page powered by HTML5-QRCode.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("IngredientScanner.jsx", table_cell_style), Paragraph("Label OCR camera & file upload page with live image preprocessing feedback.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("ProductAnalysis.jsx", table_cell_style), Paragraph("Detailed 4-pillar analysis report view with quality scores, score deduction cards, prohibited items comparison, and PDF download.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("RegulatoryIntelligence.jsx", table_cell_style), Paragraph("Interactive 5-country ingredient regulation database browser.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("ConsumerIntelligence.jsx", table_cell_style), Paragraph("Personalized health profile customization (Diabetic, Hypertensive, Sodium limits).", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("ScanHistory.jsx", table_cell_style), Paragraph("Historical scan audit log page with re-inspection capabilities.", table_cell_style)],
        [Paragraph("<b>frontend/src/pages/</b>", table_cell_bold), Paragraph("ModelExplorer.jsx", table_cell_style), Paragraph("ML model performance benchmark page displaying accuracy, F1 score, and confusion matrix.", table_cell_style)],
        [Paragraph("<b>frontend/src/utils/</b>", table_cell_bold), Paragraph("pdfGenerator.js", table_cell_style), Paragraph("Client-side PDF report generator using jsPDF + jsPDF-AutoTable.", table_cell_style)]
    ]

    t_folder = Table(folder_data, colWidths=[110, 110, 284])
    t_folder.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_folder)
    story.append(Spacer(1, 15))

    # ---------------------------------------------------------
    # SECTION 2: TECHNICAL IMPLEMENTATION & SCANNING FLOWS
    # ---------------------------------------------------------
    story.append(Paragraph("2. Technical Implementation & Scanning Workflows", h1_style))
    
    # 2.1 OCR Scanning
    story.append(Paragraph("2.1 OCR-Based Ingredient Scanning Pipeline", h2_style))
    story.append(Paragraph("The Optical Character Recognition (OCR) pipeline extracts ingredient text from physical food packaging labels through a multi-stage Computer Vision workflow:", body_style))
    
    ocr_points = [
        "<b>1. Image Capture / Upload:</b> The user captures a label photo via the HTML5 Camera API (<input capture='environment'>) or uploads an image file.",
        "<b>2. OpenCV Computer Vision Preprocessing (backend/app/services/ocr_service.py):</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Grayscale Conversion:</i> cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) removes color noise.",
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Contrast Enhancement (CLAHE):</i> Contrast Limited Adaptive Histogram Equalization increases text-to-background contrast.",
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Binarization (Otsu Thresholding):</i> cv2.threshold() converts pixel intensities into stark black-and-white text mask.",
        "<b>3. Tesseract OCR Engine Extraction:</b> pytesseract.image_to_string() scans the preprocessed image tensor and extracts raw text string.",
        "<b>4. Tokenization & Standardization:</b> The raw text is cleaned using regex separators, lowercased, and matched against the standardized ingredient intelligence database (ingredient_intelligence.py) containing ~39 E-numbers / INS codes."
    ]
    for pt in ocr_points:
        story.append(Paragraph(pt, bullet_style))
    story.append(Spacer(1, 10))

    # 2.2 Barcode Scanning
    story.append(Paragraph("2.2 Barcode Scanning & Catalog Resolution Flow", h2_style))
    story.append(Paragraph("The Barcode scanning pipeline resolves product identities instantaneously using standard international GTIN / EAN-13 barcodes:", body_style))
    
    barcode_points = [
        "<b>1. Camera Stream Decoding:</b> html5-qrcode library continuously samples video frames from the user's web camera and decodes 13-digit EAN barcode patterns.",
        "<b>2. API Lookup (backend/app/services/openfoodfacts_service.py):</b> The frontend issues an HTTP GET request to /api/barcode/{code}.",
        "<b>3. Hybrid Resolution Strategy:</b>",
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Primary:</i> Query OpenFoodFacts REST API (https://world.openfoodfacts.org/api/v0/product/{code}.json).",
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Offline Fallback:</i> If offline or API fails, queries local catalog database containing offline product profiles.",
        "<b>4. Data Normalization:</b> Extracts product name, brand, category, ingredient list string, and nutritional macros (sugar, sodium, saturated fat, energy per 100g) for processing."
    ]
    for pt in barcode_points:
        story.append(Paragraph(pt, bullet_style))
    story.append(Spacer(1, 10))

    # 2.3 Decision Engine & 4 Pillars
    story.append(Paragraph("2.3 Decision Engine & 4-Pillar Safety Architecture", h2_style))
    story.append(Paragraph("The central Decision Engine (backend/app/services/decision_engine.py) unifies 4 distinct safety pillars into a singular audit verdict:", body_style))

    pillars_table_data = [
        [Paragraph("Pillar Name", table_header_style), Paragraph("Technology & Algorithm", table_header_style), Paragraph("Evaluation Logic & Output", table_header_style)],
        [
            Paragraph("<b>Pillar 1: Adulterant Screening</b>", table_cell_bold),
            Paragraph("Regex Pattern Matcher<br/>(adulteration_service.py)", table_cell_style),
            Paragraph("Screens for illegal chemical dyes (Rhodamine B, Metanil Yellow, Sudan Dyes), trans-fats, and heavy metals. Immediate critical alert if detected.", table_cell_style)
        ],
        [
            Paragraph("<b>Pillar 2: ML Quality Scorer</b>", table_cell_bold),
            Paragraph("Gradient Boosting Classifier<br/>(predict.py)", table_cell_style),
            Paragraph("ML model computes dynamic score (0-100). Starts at baseline 100 and applies mathematical deductions for high sugar, sodium, saturated fat, and artificial additives.", table_cell_style)
        ],
        [
            Paragraph("<b>Pillar 3: 5-Country Regulatory Engine</b>", table_cell_bold),
            Paragraph("Statutory Matrix Matcher<br/>(regulatory_service.py)", table_cell_style),
            Paragraph("Evaluates formulation against 5 jurisdictions: India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), UK (FSA). Displays INS/E-numbers and country approval status.", table_cell_style)
        ],
        [
            Paragraph("<b>Pillar 4: Consumer Guidance</b>", table_cell_bold),
            Paragraph("Personalization Engine<br/>(consumer_service.py)", table_cell_style),
            Paragraph("Checks ingredients against user's health profile (Diabetic, Hypertensive, Vegan, Gluten-Free) and flags specific personal risk ingredients.", table_cell_style)
        ]
    ]
    t_pillars = Table(pillars_table_data, colWidths=[120, 130, 254])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 10))

    # 2.4 Legality vs Health Explanation
    story.append(Paragraph("2.4 Legality vs. Health Quality Score Logic", h2_style))
    story.append(Paragraph("<b>Why can a product score 72/100 while passing legally in all 5 countries?</b>", body_style))
    story.append(Paragraph("• <b>Legality</b> is binary (PASS/FAIL): A product passes legally in India, USA, EU, Germany, and UK as long as it contains <i>zero illegal adulterants or banned substances</i>, and all additives remain under maximum statutory limits.", body_style))
    story.append(Paragraph("• <b>Quality Score (0-100)</b> measures overall nutritional healthiness. Deductions are calculated for high sugar (-10 pts), artificial food dyes (-15 pts), chemical preservatives (-8 pts), and excessive sodium (-5 pts). Therefore, a legally approved product can receive 72/100 due to non-fatal nutritional penalties.", body_style))
    story.append(Spacer(1, 10))

    # 2.5 PDF Generator
    story.append(Paragraph("2.5 PDF Report Generation Engine", h2_style))
    story.append(Paragraph("The PDF Report export feature (frontend/src/utils/pdfGenerator.js) uses <b>jsPDF</b> and <b>jsPDF-AutoTable</b>. It runs entirely client-side, dynamically rendering product metadata, 4-pillar scores, score deduction breakdowns, prohibited items comparison table, and decision trace into a downloadable PDF document.", body_style))

    doc.build(story, canvasmaker=NumberedCanvas)

if __name__ == '__main__':
    project_pdf_path = r"c:\Users\lapto\Desktop\FINALYEARPROJECT\FoodGuard_AI_System_Architecture_and_Technical_Documentation.pdf"
    artifact_pdf_path = r"C:\Users\lapto\.gemini\antigravity\brain\a680a472-9868-4aac-bcb9-e65a9d04a1a4\FoodGuard_AI_System_Architecture_and_Technical_Documentation.pdf"
    
    build_pdf(project_pdf_path)
    build_pdf(artifact_pdf_path)
    print("Successfully generated both PDF documentation files!")
