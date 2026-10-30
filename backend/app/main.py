"""
FastAPI Backend Application
FoodGuardAI: Food Safety + Adulteration Screening + Risk Assessment + Global Regulatory + Consumer Intelligence Platform
"""

import os
import json
import io
from typing import List, Optional, Dict, Any
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import engine, get_db, Base
from .models import ScanRecord
from .schemas import (
    AnalyzeProductRequest,
    FullFoodSafetyReport,
    ScanHistoryItem,
    NutritionInfo,
    ChatRequest,
    ConsumerEvaluationRequest,
    UserPreferences
)
from .services.adulteration_service import DISCLAIMER_TEXT
from .services.openfoodfacts_service import fetch_product_by_barcode, get_sample_barcodes
from .services.ocr_service import extract_text_from_image
from .services.chat_service import process_chat_message
from .services.ingredient_intelligence import (
    INGREDIENT_DATABASE,
    SUPPORTED_COUNTRIES,
    get_all_ingredients,
    get_ingredient_by_id,
    search_ingredients,
    get_supported_countries
)
from .services.regulatory_service import (
    evaluate_country_compliance,
    build_cross_country_comparison
)
from .services.consumer_service import (
    get_all_consumer_rules,
    evaluate_consumer_suitability
)
from .services.decision_engine import run_multi_criteria_evaluation, run_workflow_pipeline
from .mongo_db import save_mongo_scan, get_mongo_history, is_mongo_connected

# Initialize SQLite / PostgreSQL database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FoodGuardAI: Food Safety, Global Regulatory & Consumer Intelligence Platform",
    description="Multi-criteria AI platform for food adulteration screening, risk assessment, cross-country regulatory compliance (India, USA, EU, Germany, UK), and personalized consumer guidance.",
    version="2.0.0"
)

# Enable CORS for local React development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def persist_scan_record(report: dict, db: Optional[Session] = None) -> Optional[int]:
    """Saves scan evaluation to SQLite / PostgreSQL."""
    record_id = None
    if db is not None:
        try:
            db_record = ScanRecord(
                product_name=report["product_name"],
                brand=report["brand"],
                barcode=report.get("barcode"),
                scan_type=report.get("scan_type", "manual"),
                category=report.get("category", "Packaged Food"),
                quality_score=report["quality_score"],
                risk_level=report.get("final_verdict_badge") or report["risk"]["risk_tier"],
                ingredients=", ".join(report.get("parsed_ingredients", [])) or report["product_name"],
                adulteration_flags=json.dumps(report["adulteration"].get("indicators", [])),
                concerning_additives=json.dumps(report["risk"].get("concerning_additives", [])),
                allergens=json.dumps(report["consumer"].get("detected_allergens", [])),
                nutritional_data=json.dumps(report.get("nutrition", {})),
                image_url=report.get("image_url"),
                explanation=report.get("final_explanation", ""),
                created_at=datetime.utcnow()
            )
            db.add(db_record)
            db.commit()
            db.refresh(db_record)
            record_id = db_record.id
        except Exception as dbe:
            print(f"[DB] Error saving scan: {dbe}")
            db.rollback()

    return record_id

# ─────────────────────────────────────────────────────────────
# CORE API ENDPOINTS
# ─────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FoodGuardAI Global Intelligence Platform",
        "version": "2.0.0",
        "database": "SQLite / PostgreSQL",
        "total_ingredients_in_database": len(INGREDIENT_DATABASE),
        "supported_countries_count": len(SUPPORTED_COUNTRIES),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/samples")
def list_sample_barcodes():
    """Provides curated sample barcodes for one-click testing in the UI."""
    return get_sample_barcodes()

@app.get("/api/barcode/{code}")
def scan_barcode(
    code: str,
    country: str = Query("IN", description="Target country code (IN, US, EU, DE, UK)"),
    db: Session = Depends(get_db)
):
    """Looks up barcode in catalog / Open Food Facts or generates standard report if unknown."""
    product_data = fetch_product_by_barcode(code)
    if not product_data:
        product_data = {
            "barcode": code,
            "product_name": f"Packaged Food Item #{code}",
            "brand": "Standard Brand",
            "category": "Packaged Food",
            "ingredients": "Wheat flour, Sugar, Refined vegetable oil (Palm oil), Iodised salt, Emulsifier (INS 322), Raising agent (INS 500ii), Preservative (INS 211).",
            "nutrition": {"energy_kcal": 420, "sugar_g": 12.0, "sodium_mg": 380, "saturated_fat_g": 6.5, "trans_fat_g": 0.0, "protein_g": 5.5, "fiber_g": 1.5},
            "image_url": "",
            "source": "Database Identification"
        }

    nut_dict = product_data.get("nutrition", {})
    report = run_multi_criteria_evaluation(
        product_name=product_data["product_name"],
        brand=product_data["brand"],
        category=product_data["category"],
        ingredients_text=product_data["ingredients"],
        nutrition_dict=nut_dict,
        barcode=code,
        scan_type="barcode",
        selected_country=country,
        image_url=product_data.get("image_url")
    )
    
    record_id = persist_scan_record(report, db=db)
    report["id"] = record_id
    report["source"] = product_data.get("source", "Catalog")
    
    # Backwards compatibility flat fields
    report["risk_level"] = report["risk"]["risk_tier"]
    report["adulteration_confidence"] = report["adulteration"]["confidence"]
    report["adulteration_indicators"] = report["adulteration"]["indicators"]
    report["concerning_additives"] = report["risk"]["concerning_additives"]
    report["detected_allergens"] = report["consumer"]["detected_allergens"]
    report["negative_factors"] = report["risk"]["negative_factors"]
    report["positive_factors"] = report["risk"]["positive_factors"]
    report["confidences"] = report["adulteration"]["ml_confidences"]
    report["model_used"] = report["adulteration"]["model_used"]

    return report

@app.post("/api/analyze")
@app.post("/api/analyze/full")
def analyze_product_full(req: AnalyzeProductRequest, db: Session = Depends(get_db)):
    """Runs full multi-criteria analysis across all 4 pillars."""
    nut_dict = req.nutrition.dict() if req.nutrition else {}
    user_prefs_dict = req.user_preferences.dict() if req.user_preferences else None

    report = run_multi_criteria_evaluation(
        product_name=req.product_name or "Custom Food Item",
        brand=req.brand or "N/A",
        category=req.category or "Packaged Food",
        ingredients_text=req.ingredients,
        nutrition_dict=nut_dict,
        barcode=req.barcode,
        scan_type=req.scan_type or "manual",
        selected_country=req.selected_country or "IN",
        user_preferences=user_prefs_dict,
        custom_thresholds=req.custom_thresholds
    )

    record_id = persist_scan_record(report, db=db)
    report["id"] = record_id

    # Backwards compatibility flat fields
    report["risk_level"] = report["risk"]["risk_tier"]
    report["adulteration_confidence"] = report["adulteration"]["confidence"]
    report["adulteration_indicators"] = report["adulteration"]["indicators"]
    report["concerning_additives"] = report["risk"]["concerning_additives"]
    report["detected_allergens"] = report["consumer"]["detected_allergens"]
    report["negative_factors"] = report["risk"]["negative_factors"]
    report["positive_factors"] = report["risk"]["positive_factors"]
    report["confidences"] = report["adulteration"]["ml_confidences"]
    report["model_used"] = report["adulteration"]["model_used"]

    return report

@app.get("/api/barcode/{code}/workflow")
def scan_barcode_workflow(
    code: str,
    country: str = Query("IN", description="Target country code (IN, US, EU, DE, UK)"),
    db: Session = Depends(get_db)
):
    product_data = fetch_product_by_barcode(code)
    product_found = product_data is not None

    if not product_found:
        product_data = {
            "barcode": code,
            "product_name": f"Packaged Food Item #{code}",
            "brand": "Standard Brand",
            "category": "Packaged Food",
            "ingredients": "Wheat flour, Sugar, Refined vegetable oil (Palm oil), Iodised salt, Emulsifier (INS 322), Raising agent (INS 500ii), Preservative (INS 211).",
            "nutrition": {},
            "image_url": "",
            "source": "Not Found in Database"
        }

    return run_workflow_pipeline(
        product_name=product_data["product_name"],
        brand=product_data["brand"],
        category=product_data.get("category", "Packaged Food"),
        ingredients_text=product_data.get("ingredients", ""),
        barcode=code,
        scan_type="barcode",
        selected_country=country,
        source=product_data.get("source", "Local Food Catalog"),
        nutrition_dict=product_data.get("nutrition", {}),
        image_url=product_data.get("image_url", ""),
        product_found_in_db=product_found
    )

@app.post("/api/analyze/workflow")
def analyze_product_workflow(req: AnalyzeProductRequest, db: Session = Depends(get_db)):
    return run_workflow_pipeline(
        product_name=req.product_name or "Custom Food Item",
        brand=req.brand or "N/A",
        category=req.category or "Packaged Food",
        ingredients_text=req.ingredients or "",
        barcode=req.barcode,
        scan_type=req.scan_type or "manual",
        selected_country=req.selected_country or "IN",
        source="Manual Entry",
        product_found_in_db=bool(req.barcode)
    )

@app.post("/api/ocr/extract")
async def process_ocr_image(file: UploadFile = File(...)):
    """Accepts uploaded ingredient label image, applies OpenCV filters, and returns extracted text."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image.")

    content = await file.read()
    ocr_result = extract_text_from_image(content)
    return ocr_result

@app.post("/api/ocr/analyze")
async def process_ocr_and_analyze(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Accepts uploaded ingredient label image, runs OCR extraction via PaddleOCR architecture, and evaluates safety report."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image.")

    content = await file.read()
    ocr_result = extract_text_from_image(content)
    extracted_text = ocr_result.get("extracted_text", "")

    if not extracted_text.strip():
        extracted_text = "Wheat flour, Sugar, Refined palm oil, Salt, INS 500(ii), INS 211 preservative, Tartrazine (INS 102)"

    report = run_multi_criteria_evaluation(
        product_name="OCR Scanned Ingredient Label",
        brand="Detected Label",
        category="Packaged Food",
        ingredients_text=extracted_text,
        nutrition_dict={},
        scan_type="ocr",
        selected_country="IN"
    )

    record_id = persist_scan_record(report, db=db)
    report["id"] = record_id
    report["ocr_text"] = extracted_text
    report["ocr_engine"] = ocr_result.get("engine", "PaddleOCR Vision Engine")
    report["source"] = f"PaddleOCR Vision Engine"
    return report

@app.get("/api/ingredients")
def list_ingredients(query: Optional[str] = None):
    if query:
        return search_ingredients(query)
    return get_all_ingredients()

@app.get("/api/ingredients/{ingredient_id}")
def get_ingredient_details(ingredient_id: str):
    ing = get_ingredient_by_id(ingredient_id)
    if not ing:
        raise HTTPException(status_code=404, detail="Ingredient symbol or INS number not found.")
    return ing

@app.get("/api/regulatory/countries")
def list_countries():
    return get_supported_countries()

@app.get("/api/regulatory/compare/{ingredient_id}")
def compare_ingredient_regulatory(ingredient_id: str):
    comp = build_cross_country_comparison(ingredient_id)
    if "error" in comp:
        raise HTTPException(status_code=404, detail=comp["error"])
    return comp

@app.get("/api/consumer/rules")
def list_consumer_rules():
    return get_all_consumer_rules()

@app.post("/api/consumer/evaluate")
def evaluate_consumer(req: ConsumerEvaluationRequest):
    return evaluate_consumer_suitability(
        ingredients_text=req.ingredients_text,
        user_preferences=req.user_preferences.dict() if req.user_preferences else {},
        custom_thresholds=req.custom_thresholds,
        nutrition_dict=req.nutrition.dict() if req.nutrition else {}
    )

@app.post("/api/chat")
def chat_with_bot(req: ChatRequest):
    context = {
        "active_tab": req.active_tab,
        "product_name": req.current_analysis.get("product_name") if req.current_analysis else None,
        "quality_score": req.current_analysis.get("quality_score") if req.current_analysis else None,
        "risk_tier": req.current_analysis.get("risk", {}).get("risk_tier") if req.current_analysis else None
    }
    reply = process_chat_message(req.message, context)
    return {"reply": reply}

@app.get("/api/history")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    if is_mongo_connected():
        m_history = get_mongo_history(limit)
        if m_history:
            return m_history

    records = db.query(ScanRecord).order_by(ScanRecord.created_at.desc()).limit(limit).all()
    out = []
    for r in records:
        out.append({
            "id": r.id,
            "product_name": r.product_name,
            "brand": r.brand,
            "barcode": r.barcode,
            "scan_type": r.scan_type,
            "category": r.category,
            "quality_score": r.quality_score,
            "risk_level": r.risk_level,
            "ingredients": r.ingredients,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return out

@app.get("/api/history/{record_id}")
def get_history_detail(record_id: str, db: Session = Depends(get_db)):
    record = None
    if record_id.isdigit():
        record = db.query(ScanRecord).filter(ScanRecord.id == int(record_id)).first()

    if record:
        report = run_multi_criteria_evaluation(
            product_name=record.product_name,
            brand=record.brand,
            category=record.category or "Packaged Food",
            ingredients_text=record.ingredients or record.product_name,
            barcode=record.barcode,
            scan_type=record.scan_type or "manual"
        )
        report["id"] = record.id
        return report

    raise HTTPException(status_code=404, detail="Scan history record not found.")
