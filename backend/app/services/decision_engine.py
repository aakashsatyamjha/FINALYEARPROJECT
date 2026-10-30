"""
Multi-Criteria Food Safety Decision Engine & Decision Trace Service
Synthesizes Adulteration Screening, Health Risk Assessment, Global Regulatory Compliance,
and Consumer Intelligence into an explainable, multi-dimensional Food Safety Report.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from .adulteration_service import analyze_ingredients_text, DISCLAIMER_TEXT
from .ingredient_intelligence import match_ingredient_text, get_supported_countries
from .regulatory_service import evaluate_country_compliance, build_cross_country_comparison
from .consumer_service import evaluate_consumer_suitability
from .dataset_service import match_ingredients_against_dataset, evaluate_dataset_permissions
from ...ml.predict import predictor

def run_multi_criteria_evaluation(
    product_name: str,
    brand: str,
    category: str,
    ingredients_text: str,
    nutrition_dict: Optional[Dict[str, float]] = None,
    barcode: Optional[str] = None,
    scan_type: str = "manual",
    selected_country: str = "IN",
    user_preferences: Optional[Dict[str, bool]] = None,
    custom_thresholds: Optional[Dict[str, float]] = None,
    image_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Executes all 4 FoodGuard pillars sequentially and generates an explainable Decision Trace.
    Never short-circuits on first failure; evaluates every applicable criterion.
    """
    if nutrition_dict is None:
        nutrition_dict = {
            "energy_kcal": 0.0,
            "sugar_g": 0.0,
            "sodium_mg": 0.0,
            "saturated_fat_g": 0.0,
            "trans_fat_g": 0.0,
            "protein_g": 0.0,
            "fiber_g": 0.0
        }

    decision_steps = []

    # ── STEP 1: Ingredient Identification & Normalization ──
    matched_ingredients = match_ingredient_text(ingredients_text)
    
    # ── 300-Item Regulatory Dataset Matching & Permissions Audit ──
    dataset_matches = match_ingredients_against_dataset(ingredients_text)
    dataset_eval = evaluate_dataset_permissions(dataset_matches)

    decision_steps.append({
        "step_num": 1,
        "title": "Ingredient Identification & Entity Normalization",
        "status": "PASS" if matched_ingredients or dataset_matches else "INFO",
        "detail": f"Matched {len(matched_ingredients)} standardized ingredients and {len(dataset_matches)} regulatory substances against the 300-item dataset.",
        "icon": "ListChecks"
    })

    # ── PILLAR 1: Adulteration Screening (AI & Chemical Rules) ──
    adulteration_res = analyze_ingredients_text(ingredients_text, category)
    has_critical_adulterant = adulteration_res.get("has_critical_flags", False)
    adulteration_indicators = adulteration_res.get("adulteration_indicators", [])

    if has_critical_adulterant:
        adulteration_status = "HIGH CONCERN"
        adulteration_badge = "✕ High Concern / Adulterant Flagged"
        adulteration_summary = f"Detected {len(adulteration_indicators)} indicator(s) associated with banned or hazardous adulteration patterns."
        step_status = "FAIL"
    elif adulteration_indicators:
        adulteration_status = "MEDIUM CONCERN"
        adulteration_badge = "⚠ Medium Concern"
        adulteration_summary = f"Flagged {len(adulteration_indicators)} suspicious formulation marker(s)."
        step_status = "CONDITIONAL"
    else:
        adulteration_status = "LOW CONCERN"
        adulteration_badge = "✓ Low Concern"
        adulteration_summary = "No known industrial chemical adulterants or non-permitted dye signatures detected."
        step_status = "PASS"

    decision_steps.append({
        "step_num": 2,
        "title": "Pillar 1: Adulteration Screening",
        "status": step_status,
        "detail": adulteration_summary,
        "icon": "ShieldAlert" if has_critical_adulterant else "ShieldCheck"
    })

    # If nutrition was not explicitly provided (e.g. from OCR label text), estimate baseline from ingredients keywords
    if not nutrition_dict or (nutrition_dict.get("energy_kcal", 0.0) == 0.0 and nutrition_dict.get("sugar_g", 0.0) == 0.0 and nutrition_dict.get("sodium_mg", 0.0) == 0.0):
        ing_lower = ingredients_text.lower()
        est_sugar = 0.0
        est_sodium = 45.0
        est_sat_fat = 0.5
        est_trans_fat = 0.0
        est_protein = 2.0
        est_fiber = 1.0
        est_energy = 120.0

        if any(w in ing_lower for w in ["sugar", "sucrose", "glucose", "corn syrup", "fructose", "maltose", "dextrose", "jaggery", "tastemaker"]):
            est_sugar += 16.5
        if any(w in ing_lower for w in ["salt", "sodium", "ins 621", "msg", "monosodium glutamate", "ins 635", "baking powder", "soda"]):
            est_sodium += 620.0
        if any(w in ing_lower for w in ["palm oil", "hydrogenated", "shortening", "vanaspati", "butter", "lard", "tallow", "fat"]):
            est_sat_fat += 9.5
            if "hydrogenated" in ing_lower or "vanaspati" in ing_lower:
                est_trans_fat += 0.8
        if any(w in ing_lower for w in ["milk", "dairy", "whey", "protein", "soya", "egg", "peanut", "cashew", "almond"]):
            est_protein += 8.0
        if any(w in ing_lower for w in ["whole wheat", "oats", "fiber", "bran", "psyllium", "flaxseed"]):
            est_fiber += 6.0

        nutrition_dict = {
            "energy_kcal": est_energy,
            "sugar_g": est_sugar,
            "sodium_mg": est_sodium,
            "saturated_fat_g": est_sat_fat,
            "trans_fat_g": est_trans_fat,
            "protein_g": est_protein,
            "fiber_g": est_fiber
        }

    # ── ML Model Inference for Quality Scoring & Explanations ──
    concerning_additives = list(adulteration_res.get("concerning_additives", []))
    for ing in matched_ingredients:
        concerning_additives.append({
            "name": ing.get("common_name", "Additive"),
            "matched_text": ing.get("common_name", ""),
            "type": ing.get("function", "Food Additive"),
            "risk_level": ing.get("risk_classification", "Moderate"),
            "concern": ing.get("cross_country_reason", "")
        })

    n_additives = len(concerning_additives)
    n_colors = sum(1 for a in concerning_additives if any(k in a.get("type", "").lower() for k in ["dye", "color", "colour", "pigment"]))
    n_sweeteners = sum(1 for a in concerning_additives if any(k in a.get("type", "").lower() for k in ["sweetener", "sugar substitute"]))
    n_preservatives = sum(1 for a in concerning_additives if any(k in a.get("type", "").lower() for k in ["preservative", "antioxidant", "conditioner", "agent"]))
    is_adulterated_flag = 1 if has_critical_adulterant else 0

    ml_input = {
        "energy_kcal": nutrition_dict.get("energy_kcal", 0.0),
        "sugar_g": nutrition_dict.get("sugar_g", 0.0),
        "sodium_mg": nutrition_dict.get("sodium_mg", 0.0),
        "saturated_fat_g": nutrition_dict.get("saturated_fat_g", 0.0),
        "trans_fat_g": nutrition_dict.get("trans_fat_g", 0.0),
        "protein_g": nutrition_dict.get("protein_g", 0.0),
        "fiber_g": nutrition_dict.get("fiber_g", 0.0),
        "additives_count": n_additives,
        "artificial_colors_count": n_colors,
        "artificial_sweeteners_count": n_sweeteners,
        "preservatives_count": n_preservatives,
        "is_suspected_adulterant": is_adulterated_flag
    }

    ml_res = predictor.predict(ml_input)

    # ── PILLAR 2: Health & Risk Assessment ──
    # Compute multi-dimensional risk scores (0% to 100%)
    # 1. Ingredient Risk (based on severity of additives and toxicity markers)
    ing_risk_points = 0
    for ing in matched_ingredients:
        r = ing.get("risk_classification", "Low").lower()
        if r == "critical":
            ing_risk_points += 45
        elif r == "high":
            ing_risk_points += 25
        elif r == "moderate":
            ing_risk_points += 15
        elif r == "low-to-moderate":
            ing_risk_points += 8
    if has_critical_adulterant:
        ing_risk_points += 60
    if n_additives > 3:
        ing_risk_points += (n_additives - 3) * 5
    ingredient_risk_pct = min(100, max(5, ing_risk_points))

    # 2. Regulatory Risk & Multi-Country Pre-Evaluation (IN, US, EU, DE, UK)
    cross_country_data = build_cross_country_comparison(ingredients_text)
    
    all_country_codes = ["IN", "US", "EU", "DE", "UK"]
    all_country_evaluations = {}
    country_summaries = {}
    for c_code in all_country_codes:
        eval_res = evaluate_country_compliance(ingredients_text, country_code=c_code, category=category)
        all_country_evaluations[c_code] = eval_res
        country_summaries[c_code] = {
            "country_code": c_code,
            "country_name": eval_res["country_name"],
            "authority": eval_res["authority"],
            "full_authority": eval_res.get("full_authority", eval_res["authority"]),
            "flag": eval_res["flag"],
            "verdict": eval_res["verdict"],
            "verdict_text": eval_res["verdict_text"],
            "summary": eval_res["summary"],
            "passed_criteria": eval_res["passed_criteria"],
            "conditional_criteria": eval_res["conditional_criteria"],
            "failed_criteria": eval_res["failed_criteria"],
            "total_criteria_evaluated": eval_res.get("total_criteria_evaluated", 0)
        }
        
    selected_country_eval = all_country_evaluations.get(selected_country, all_country_evaluations["IN"])
    
    reg_risk_points = 0
    if selected_country_eval["verdict"] == "FAIL":
        reg_risk_points += 75
    elif selected_country_eval["verdict"] == "CONDITIONAL":
        reg_risk_points += 40
    if cross_country_data["divergence_count"] > 0:
        reg_risk_points += cross_country_data["divergence_count"] * 12
    regulatory_risk_pct = min(100, max(5, reg_risk_points))

    # 3. Consumer Risk (based on nutritional extremes and user profile conflicts)
    consumer_eval = evaluate_consumer_suitability(
        ingredients_text=ingredients_text,
        nutrition=nutrition_dict,
        preferences=user_preferences,
        custom_thresholds=custom_thresholds
    )
    
    sugar_val = float(nutrition_dict.get("sugar_g", 0.0))
    sodium_val = float(nutrition_dict.get("sodium_mg", 0.0))
    sat_val = float(nutrition_dict.get("saturated_fat_g", 0.0))
    trans_val = float(nutrition_dict.get("trans_fat_g", 0.0))

    consumer_risk_points = 0
    if sugar_val > 22.5: consumer_risk_points += 30
    elif sugar_val > 10.0: consumer_risk_points += 15
    if sodium_val > 800.0: consumer_risk_points += 30
    elif sodium_val > 400.0: consumer_risk_points += 15
    if sat_val > 8.0: consumer_risk_points += 20
    if trans_val > 0.2: consumer_risk_points += 40
    if len(consumer_eval.get("concerns", [])) > 0:
        consumer_risk_points += len(consumer_eval["concerns"]) * 15
    consumer_risk_pct = min(100, max(5, consumer_risk_points))

    # 4. Overall Holistic Risk Calculation
    overall_risk_pct = min(100, max(5, round(
        (ingredient_risk_pct * 0.40) + 
        (regulatory_risk_pct * 0.35) + 
        (consumer_risk_pct * 0.25)
    )))

    if overall_risk_pct >= 65 or has_critical_adulterant:
        risk_tier = "High Risk"
    elif overall_risk_pct >= 30:
        risk_tier = "Moderate Risk"
    else:
        risk_tier = "Low Risk"

    if dataset_eval.get("overall_risk") == "HIGH":
        overall_risk_pct = max(overall_risk_pct, 75)
        risk_tier = "High Risk"
    elif dataset_eval.get("overall_risk") == "MEDIUM" and risk_tier == "Low Risk":
        overall_risk_pct = max(overall_risk_pct, 45)
        risk_tier = "Moderate Risk"

    # ── Holistic Multi-Pillar Quality & Safety Score (0-100) ──
    base_ml_score = ml_res["quality_score"]
    safety_score = max(5, 100 - overall_risk_pct)

    if has_critical_adulterant or dataset_eval.get("overall_risk") == "HIGH":
        quality_score = max(5, min(28, safety_score))
    elif selected_country_eval["verdict"] == "FAIL":
        quality_score = max(10, min(38, round(safety_score * 0.7 + base_ml_score * 0.3)))
    elif selected_country_eval["verdict"] == "CONDITIONAL" or cross_country_data["divergence_count"] > 0 or dataset_eval.get("has_alerts"):
        quality_score = max(25, min(65, round(safety_score * 0.6 + base_ml_score * 0.4)))
    elif risk_tier == "Moderate Risk" or consumer_eval["verdict"] == "CONCERN":
        quality_score = max(40, min(72, round(safety_score * 0.5 + base_ml_score * 0.5)))
    else:
        quality_score = max(75, min(98, round(safety_score * 0.4 + base_ml_score * 0.6)))

    # ── Why This Product is Not 100/100 (Score Deduction Audit) ──
    score_deductions = []

    # ── 300-Item Dataset Score Deductions & Alerts ──
    if dataset_eval.get("has_alerts"):
        for alert_item in dataset_eval.get("alerts", []):
            is_banned = "banned" in alert_item.get("alert_reason", "").lower() or "revoked" in alert_item.get("alert_reason", "").lower()
            pts = 40 if is_banned else 20
            score_deductions.append({
                "factor": f"{alert_item['ingredient_name']} ({alert_item['ins_number']})",
                "category": "Regulatory Alert / International Restriction",
                "impact": f"-{pts} pts",
                "points_deducted": pts,
                "reason": alert_item["alert_reason"],
                "prohibited_in": alert_item["flagged_authorities"]
            })
    
    if has_critical_adulterant:
        for ind in adulteration_indicators:
            score_deductions.append({
                "factor": ind.get("substance", "Adulterant Marker"),
                "category": "Adulteration / Toxic Marker",
                "impact": "-45 to -60 pts",
                "points_deducted": 50,
                "reason": f"Prohibited industrial chemical marker: {ind.get('reason', 'Strictly banned adulterant')}.",
                "prohibited_in": "India (FSSAI), USA (FDA), EU (EFSA), Germany (BVL), UK (FSA)"
            })
            
    for ing in matched_ingredients:
        ing_name = ing.get("common_name", "Additive")
        ins_code = ing.get("ins_e_number", "INS Additive")
        risk_cls = ing.get("risk_classification", "Moderate")
        
        in_code = ing.get("india_status", {}).get("code", "")
        us_code = ing.get("usa_status", {}).get("code", "")
        eu_code = ing.get("eu_status", {}).get("code", "")
        de_code = ing.get("germany_status", {}).get("code", "")
        uk_code = ing.get("uk_status", {}).get("code", "")
        
        prohibited_countries = []
        if in_code == "NOT_PERMITTED": prohibited_countries.append("India (FSSAI)")
        if us_code == "NOT_PERMITTED": prohibited_countries.append("USA (FDA)")
        if eu_code == "NOT_PERMITTED": prohibited_countries.append("EU (EFSA)")
        if de_code == "NOT_PERMITTED": prohibited_countries.append("Germany (BVL)")
        if uk_code == "NOT_PERMITTED": prohibited_countries.append("UK (FSA)")
        
        if prohibited_countries:
            pts = 35 if risk_cls.lower() in ["critical", "high"] else 20
            score_deductions.append({
                "factor": f"{ing_name} ({ins_code})",
                "category": "Statutory Regulatory Prohibition",
                "impact": f"-{pts} pts",
                "points_deducted": pts,
                "reason": f"Banned or unapproved in {', '.join(prohibited_countries)}. {ing.get('cross_country_reason', '')}",
                "prohibited_in": ", ".join(prohibited_countries)
            })
        elif risk_cls.lower() in ["high", "moderate", "low-to-moderate"]:
            pts = 15 if risk_cls.lower() == "high" else (10 if risk_cls.lower() == "moderate" else 5)
            score_deductions.append({
                "factor": f"{ing_name} ({ins_code})",
                "category": "Food Additive / Formulation Limit",
                "impact": f"-{pts} pts",
                "points_deducted": pts,
                "reason": f"Subject to regulatory exposure caps and statutory warning labels. {ing.get('cross_country_reason', '')}",
                "prohibited_in": "Permitted with limits"
            })
            
    if sugar_val > 22.5:
        score_deductions.append({
            "factor": f"High Sugar Content ({sugar_val}g/100g)",
            "category": "Nutritional Risk",
            "impact": "-18 pts",
            "points_deducted": 18,
            "reason": "Exceeds WHO/FSSAI high sugar threshold (15g/100g).",
            "prohibited_in": "None (Nutritional Guideline)"
        })
    elif sugar_val > 10.0:
        score_deductions.append({
            "factor": f"Moderate Sugar Level ({sugar_val}g/100g)",
            "category": "Nutritional Risk",
            "impact": "-8 pts",
            "points_deducted": 8,
            "reason": "Elevated added sugar content.",
            "prohibited_in": "None (Nutritional Guideline)"
        })
        
    if sodium_val > 800.0:
        score_deductions.append({
            "factor": f"High Sodium ({sodium_val}mg/100g)",
            "category": "Cardiovascular Risk",
            "impact": "-18 pts",
            "points_deducted": 18,
            "reason": "Exceeds daily baseline sodium recommendations.",
            "prohibited_in": "None (Nutritional Guideline)"
        })
    elif sodium_val > 400.0:
        score_deductions.append({
            "factor": f"Elevated Sodium ({sodium_val}mg/100g)",
            "category": "Cardiovascular Risk",
            "impact": "-8 pts",
            "points_deducted": 8,
            "reason": "Moderate-to-high sodium content.",
            "prohibited_in": "None (Nutritional Guideline)"
        })
        
    if sat_val > 8.0:
        score_deductions.append({
            "factor": f"High Saturated Fat ({sat_val}g/100g)",
            "category": "Lipid Profile Risk",
            "impact": "-12 pts",
            "points_deducted": 12,
            "reason": "Rich in saturated fats (e.g. palm oil / hydrogenated fats).",
            "prohibited_in": "None (Nutritional Guideline)"
        })
        
    if trans_val > 0.2:
        score_deductions.append({
            "factor": f"Industrial Trans Fat ({trans_val}g/100g)",
            "category": "Strict Legal Cap",
            "impact": "-25 pts",
            "points_deducted": 25,
            "reason": "Exceeds WHO & FSSAI mandatory 2% trans-fat cap in fats/oils.",
            "prohibited_in": "Restricted globally"
        })

    decision_steps.append({
        "step_num": 3,
        "title": "Pillar 2: Health & Risk Assessment",
        "status": "FAIL" if risk_tier == "High Risk" else ("CONDITIONAL" if risk_tier == "Moderate Risk" else "PASS"),
        "detail": f"Overall Risk Score: {overall_risk_pct}% (Ingredient Risk: {ingredient_risk_pct}%, Regulatory Risk: {regulatory_risk_pct}%, Consumer Risk: {consumer_risk_pct}%).",
        "icon": "Activity"
    })

    # ── PILLAR 3: Global Regulatory Compliance ──
    decision_steps.append({
        "step_num": 4,
        "title": f"Pillar 3: Regulatory Compliance ({selected_country_eval['country_name']})",
        "status": selected_country_eval["verdict"],
        "detail": selected_country_eval["summary"],
        "icon": "Scale"
    })

    if cross_country_data["divergence_count"] > 0:
        decision_steps.append({
            "step_num": 5,
            "title": "Cross-Country Regulatory Divergence",
            "status": "CONDITIONAL",
            "detail": f"Identified {cross_country_data['divergence_count']} ingredient(s) with divergent regulatory statuses between India, USA, EU, Germany, and the UK.",
            "icon": "Globe"
        })

    # ── PILLAR 4: Consumer Intelligence ──
    if consumer_eval["verdict"] == "CONCERN":
        consumer_step_status = "CONDITIONAL"
    elif consumer_eval["verdict"] == "SUITABLE":
        consumer_step_status = "PASS"
    else:
        consumer_step_status = "INFO"

    decision_steps.append({
        "step_num": 6,
        "title": "Pillar 4: Consumer Suitability & Preference Matching",
        "status": consumer_step_status,
        "detail": consumer_eval["summary"],
        "icon": "UserCheck"
    })

    # ── FINAL DECISION ENGINE SYNTHESIS ──
    if has_critical_adulterant:
        overall_assessment = "HIGH CONCERN: BANNED / ADULTERANT SIGNATURE DETECTED"
        final_verdict_badge = "High Concern"
        final_explanation = "Product failed critical adulteration screening due to presence of hazardous or non-permitted industrial markers."
    elif selected_country_eval["verdict"] == "FAIL":
        overall_assessment = "REGULATORY CONCERN: NON-COMPLIANT IN SELECTED REGION"
        final_verdict_badge = "Regulatory Concern"
        final_explanation = f"Product contains substances not authorized or prohibited under {selected_country_eval['country_name']} ({selected_country_eval['authority']}) regulations."
    elif cross_country_data["divergence_count"] > 0:
        overall_assessment = "CONDITIONAL / COUNTRY-DEPENDENT REGULATORY STATUS"
        final_verdict_badge = "Country Dependent"
        final_explanation = f"Product legality and permissible additive levels vary across international jurisdictions ({cross_country_data['divergence_count']} ingredient divergence(s))."
    elif risk_tier == "Moderate Risk" or consumer_eval["verdict"] == "CONCERN":
        overall_assessment = "MODERATE CONCERN: FORMULATION & DIETARY LIMITS APPLY"
        final_verdict_badge = "Moderate Concern"
        final_explanation = "Product is legally compliant but carries elevated nutritional or consumer preference concerns."
    else:
        overall_assessment = "SAFE / LOW CONCERN: MEETS GLOBAL SCREENING BASELINE"
        final_verdict_badge = "Low Concern"
        final_explanation = "All ingredients pass adulteration screening, comply with regulatory standards in the selected region, and align with health baselines."

    return {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "category": category,
        "scan_type": scan_type,
        "quality_score": quality_score,
        "overall_assessment": overall_assessment,
        "final_verdict_badge": final_verdict_badge,
        "final_explanation": final_explanation,
        "safety_disclaimer": DISCLAIMER_TEXT,
        
        # Pillar 1: Adulteration Screening
        "adulteration": {
            "status": adulteration_status,
            "badge": adulteration_badge,
            "summary": adulteration_summary,
            "has_critical_flags": has_critical_adulterant,
            "confidence": adulteration_res.get("adulteration_confidence", 0.0),
            "indicators": adulteration_indicators,
            "model_used": ml_res["model_used"],
            "ml_confidences": ml_res["confidences"],
            "disclaimer": "AI-based screening is a preliminary algorithmic check and not a laboratory chemical confirmation of adulteration."
        },

        # Pillar 2: Health & Risk Assessment
        "risk": {
            "risk_tier": risk_tier,
            "overall_risk_pct": overall_risk_pct,
            "ingredient_risk_pct": ingredient_risk_pct,
            "regulatory_risk_pct": regulatory_risk_pct,
            "consumer_risk_pct": consumer_risk_pct,
            "negative_factors": ml_res["negative_factors"],
            "positive_factors": ml_res["positive_factors"],
            "concerning_additives": concerning_additives
        },

        # Pillar 3: Global Regulatory Compliance
        "regulatory": {
            "selected_country": selected_country_eval,
            "country_summaries": country_summaries,
            "country_evaluations": all_country_evaluations,
            "cross_country_comparison": cross_country_data,
            "divergent_ingredients": cross_country_data["divergent_ingredients"],
            "divergence_count": cross_country_data["divergence_count"]
        },

        # Pillar 4: Consumer Intelligence
        "consumer": consumer_eval,

        # Why Not 100/100 Detailed Point Deductions
        "score_deductions": score_deductions,

        # Decision Trace & Criteria Audit Trail
        "decision_trace": {
            "steps": decision_steps,
            "total_steps": len(decision_steps),
            "matched_ingredients_count": len(matched_ingredients),
            "passed_criteria_count": len(selected_country_eval["passed_criteria"]),
            "conditional_criteria_count": len(selected_country_eval["conditional_criteria"]),
            "failed_criteria_count": len(selected_country_eval["failed_criteria"])
        },

        # Ingredients & Nutrition Raw Context
        "matched_ingredients": matched_ingredients,
        "parsed_ingredients": adulteration_res.get("parsed_ingredients", []),
        "nutrition": nutrition_dict,
        "image_url": image_url,
        "created_at": datetime.utcnow(),

        # 300-Item Dataset & International Regulatory Permissions
        "dataset_eval": dataset_eval,
        "regulatory_alerts": dataset_eval.get("alerts", []),
        "has_regulatory_alerts": dataset_eval.get("has_alerts", False),
        "clean_ingredients": dataset_eval.get("clean_ingredients", []),
        "dataset_matches": dataset_matches
    }



# ─────────────────────────────────────────────────────────────────────────────
# WORKFLOW PIPELINE ENGINE — Sequential 5-Step Analysis
# ─────────────────────────────────────────────────────────────────────────────

def run_workflow_pipeline(
    product_name: str,
    brand: str,
    category: str,
    ingredients_text: str,
    barcode=None,
    scan_type: str = "barcode",
    selected_country: str = "IN",
    source: str = "Local Food Catalog",
    nutrition_dict=None,
    image_url=None,
    product_found_in_db: bool = True
) -> dict:
    """
    Executes the explicit 5-step workflow pipeline:
      Step 1 -> Dataset Lookup: Was the product found?
      Step 2 -> Ingredient Extraction: All detected ingredients/additives
      Step 3 -> Dataset Pass/Fail Check: Per-ingredient regulatory check
      Step 4 -> INS Alert Report: Deep-dive for flagged ingredients
      Step 5 -> Final Verdict: Overall risk classification
    """
    from .regulatory_service import STATUS_BADGES, get_country_status_key
    import re as _re

    if nutrition_dict is None:
        nutrition_dict = {}

    pipeline_steps = []

    # ── STEP 1: Dataset Lookup ──
    step1 = {
        "step_num": 1,
        "name": "Dataset Lookup",
        "icon": "Database",
        "status": "PASS" if product_found_in_db else "INFO",
        "status_label": "Found in Database" if product_found_in_db else "Live API / Manual Entry",
        "color": "green" if product_found_in_db else "blue",
        "detail": (
            f"Product '{product_name}' by {brand} found in local verified catalog."
            if product_found_in_db
            else "Product not in local catalog. Data from Open Food Facts API or manual entry."
        ),
        "data": {
            "product_name": product_name,
            "brand": brand,
            "category": category,
            "barcode": barcode,
            "source": source
        }
    }
    pipeline_steps.append(step1)

    # ── STEP 2: Ingredient Extraction ──
    matched_ingredients = match_ingredient_text(ingredients_text)
    raw_tokens = [t.strip() for t in _re.split(r"[,;:\n\r]+", ingredients_text) if len(t.strip()) > 2]
    known_ins = [
        {
            "name": i["common_name"],
            "ins_e_number": i["ins_e_number"],
            "function": i["function"],
            "risk": i["risk_classification"],
            "matched_text": i["matched_text"]
        }
        for i in matched_ingredients
    ]

    step2 = {
        "step_num": 2,
        "name": "Ingredient Extraction",
        "icon": "ListChecks",
        "status": "PASS",
        "status_label": f"{len(raw_tokens)} ingredients · {len(matched_ingredients)} additives matched to DB",
        "color": "blue",
        "detail": (
            f"Extracted {len(raw_tokens)} ingredients from label. "
            f"Matched {len(matched_ingredients)} against INS/E-number regulatory database."
        ),
        "data": {
            "raw_tokens": raw_tokens[:25],
            "matched_additives": known_ins,
            "total_raw": len(raw_tokens),
            "total_matched": len(matched_ingredients)
        }
    }
    pipeline_steps.append(step2)

    # ── STEP 3: Dataset Pass/Fail Check ──
    country_key = get_country_status_key(selected_country)
    country_meta = next(
        (c for c in get_supported_countries() if c["code"] == selected_country.upper()),
        {"code": "IN", "name": "India", "authority": "FSSAI", "flag": "\U0001f1ee\U0001f1f3"}
    )

    pass_items = []
    alert_items = []
    banned_items = []

    for ing in matched_ingredients:
        c_status = ing.get(country_key, {})
        sc = c_status.get("code", "INSUFFICIENT_DATA")
        check_item = {
            "name": ing["common_name"],
            "ins_e_number": ing["ins_e_number"],
            "function": ing["function"],
            "risk_classification": ing["risk_classification"],
            "status_code": sc,
            "status_text": c_status.get("status", "Unknown"),
            "condition": c_status.get("condition", ""),
            "max_limit": c_status.get("max_limit", ""),
            "source": c_status.get("source", ""),
            "country": country_meta["name"],
            "authority": country_meta["authority"],
            "flag": country_meta["flag"],
            "cross_country_reason": ing.get("cross_country_reason", "")
        }
        if sc == "NOT_PERMITTED":
            banned_items.append(check_item)
            alert_items.append(check_item)
        elif sc in ["PERMITTED_WITH_LIMITS", "PERMITTED_WITH_CONDITIONS", "RESTRICTED"]:
            alert_items.append(check_item)
        else:
            pass_items.append(check_item)

    has_banned = len(banned_items) > 0
    has_alerts = len(alert_items) > 0

    if has_banned:
        s3s, s3c = "FAIL", "red"
        s3l = f"{len(banned_items)} BANNED/NOT PERMITTED · {len(alert_items) - len(banned_items)} conditional"
    elif has_alerts:
        s3s, s3c = "CONDITIONAL", "orange"
        s3l = f"All pass · {len(alert_items)} ingredient(s) with conditions/limits"
    else:
        s3s, s3c = "PASS", "green"
        s3l = f"All {len(pass_items)} recognized ingredients PASS regulatory check"

    step3 = {
        "step_num": 3,
        "name": f"Dataset Check ({country_meta['flag']} {country_meta['name']} / {country_meta['authority']})",
        "icon": "ShieldAlert" if has_banned else "ShieldCheck",
        "status": s3s,
        "status_label": s3l,
        "color": s3c,
        "detail": (
            f"Each ingredient cross-referenced against {country_meta['name']} "
            f"({country_meta['authority']}) regulatory database."
        ),
        "data": {
            "country": country_meta["name"],
            "authority": country_meta["authority"],
            "flag": country_meta["flag"],
            "passed": pass_items,
            "alerts": alert_items,
            "banned": banned_items,
            "pass_count": len(pass_items),
            "alert_count": len(alert_items),
            "banned_count": len(banned_items)
        }
    }
    pipeline_steps.append(step3)

    # ── STEP 4: INS Alert Report ──
    all_cc = {
        "IN": {"name": "India", "authority": "FSSAI", "flag": "\U0001f1ee\U0001f1f3"},
        "US": {"name": "USA", "authority": "FDA", "flag": "\U0001f1fa\U0001f1f8"},
        "EU": {"name": "European Union", "authority": "EFSA", "flag": "\U0001f1ea\U0001f1fa"},
        "DE": {"name": "Germany", "authority": "BVL", "flag": "\U0001f1e9\U0001f1ea"},
        "UK": {"name": "United Kingdom", "authority": "FSA", "flag": "\U0001f1ec\U0001f1e7"},
    }

    ins_reports = []
    for ing in matched_ingredients:
        c_status = ing.get(country_key, {})
        sc = c_status.get("code", "INSUFFICIENT_DATA")
        if sc in ["NOT_PERMITTED", "PERMITTED_WITH_LIMITS", "PERMITTED_WITH_CONDITIONS", "RESTRICTED"]:
            matrix = []
            for cc, cl in all_cc.items():
                ck2 = get_country_status_key(cc)
                cs2 = ing.get(ck2, {})
                sc2 = cs2.get("code", "INSUFFICIENT_DATA")
                badge = STATUS_BADGES.get(sc2, STATUS_BADGES["INSUFFICIENT_DATA"])
                matrix.append({
                    "country_code": cc,
                    "country_name": cl["name"],
                    "authority": cl["authority"],
                    "flag": cl["flag"],
                    "status": cs2.get("status", "Unknown"),
                    "status_code": sc2,
                    "badge_label": badge["label"],
                    "badge_symbol": badge["symbol"],
                    "badge_category": badge["category"],
                    "max_limit": cs2.get("max_limit", "Not specified"),
                    "condition": cs2.get("condition", ""),
                    "source": cs2.get("source", "")
                })
            ins_reports.append({
                "ingredient_name": ing["common_name"],
                "scientific_name": ing.get("scientific_name", ""),
                "ins_e_number": ing["ins_e_number"],
                "function": ing["function"],
                "risk_classification": ing["risk_classification"],
                "consumer_concerns": ing.get("consumer_concerns", []),
                "cross_country_reason": ing.get("cross_country_reason", ""),
                "evidence_source": ing.get("evidence_source", ""),
                "is_banned_in_selected": sc == "NOT_PERMITTED",
                "selected_country_status": c_status,
                "country_matrix": matrix
            })

    bis = sum(1 for r in ins_reports if r["is_banned_in_selected"]) if ins_reports else 0
    s4s = ("FAIL" if bis > 0 else "CONDITIONAL") if ins_reports else "PASS"
    s4c = ("red" if bis > 0 else "orange") if ins_reports else "green"
    s4l = (
        f"{len(ins_reports)} investigated · {bis} banned in {country_meta['name']}"
        if ins_reports
        else "No alerts triggered — all ingredients clear"
    )
    step4 = {
        "step_num": 4,
        "name": "INS Alert & Country Report",
        "icon": "Globe",
        "status": s4s,
        "status_label": s4l,
        "color": s4c,
        "detail": f"Cross-country INS report for {len(ins_reports)} flagged ingredient(s) across 5 jurisdictions.",
        "data": {
            "ins_reports": ins_reports,
            "total_investigated": len(ins_reports),
            "banned_in_selected_country": bis
        }
    }
    pipeline_steps.append(step4)

    # ── STEP 5: Final Verdict ──
    from .adulteration_service import analyze_ingredients_text as _ait
    adres = _ait(ingredients_text, category)
    has_crit = adres.get("has_critical_flags", False)

    if has_crit or banned_items:
        v, vc, vi, rp, rt = "Banned Chemical Detected", "red", "ShieldOff", 90, "High Risk"
        rec = (
            "STOP CONSUMING immediately. Contains PROHIBITED or hazardous adulterant ingredients. "
            "Report to FSSAI/local food authority."
        )
    elif len(alert_items) >= 4:
        v, vc, vi, rp, rt = "High Risk", "red", "AlertOctagon", 72, "High Risk"
        rec = "Multiple restricted ingredients detected. Avoid or consume with extreme caution."
    elif len(alert_items) >= 2:
        v, vc, vi, rp, rt = "Moderate Risk", "orange", "AlertTriangle", 45, "Moderate Risk"
        rec = (
            f"Ingredients permitted under {country_meta['name']} regulations but with usage limits. "
            "Read label warnings. Limit consumption especially for children."
        )
    elif len(alert_items) == 1:
        v, vc, vi, rp, rt = "Low Risk", "yellow", "Info", 22, "Low Risk"
        rec = "Minor condition detected. Generally safe for adults following label directions."
    else:
        v, vc, vi, rp, rt = "Not Compromised", "green", "ShieldCheck", 8, "Low Risk"
        rec = (
            f"All ingredients pass {country_meta['name']} ({country_meta['authority']}) check. "
            "Product appears safe based on ingredient profile."
        )

    qs = max(10, min(98, 100 - rp))
    step5 = {
        "step_num": 5,
        "name": "Final Verdict",
        "icon": vi,
        "status": "FAIL" if rt == "High Risk" else ("CONDITIONAL" if rt == "Moderate Risk" else "PASS"),
        "status_label": v,
        "color": vc,
        "detail": rec,
        "data": {
            "verdict": v,
            "verdict_color": vc,
            "risk_tier": rt,
            "risk_pct": rp,
            "quality_score": qs,
            "selected_country": selected_country,
            "country_name": country_meta["name"],
            "authority": country_meta["authority"],
            "flag": country_meta["flag"],
            "recommendation": rec,
            "summary": {
                "pass_count": len(pass_items),
                "alert_count": len(alert_items),
                "banned_count": len(banned_items),
                "total_matched": len(matched_ingredients),
                "has_critical_adulterant": has_crit
            }
        }
    }
    pipeline_steps.append(step5)

    return {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "category": category,
        "scan_type": scan_type,
        "selected_country": selected_country,
        "country_name": country_meta["name"],
        "country_flag": country_meta["flag"],
        "authority": country_meta["authority"],
        "ingredients_text": ingredients_text,
        "image_url": image_url,
        "source": source,
        "pipeline_steps": pipeline_steps,
        "total_steps": len(pipeline_steps),
        "final_verdict": v,
        "final_verdict_color": vc,
        "risk_tier": rt,
        "risk_pct": rp,
        "quality_score": qs,
        "matched_ingredients_count": len(matched_ingredients),
        "pass_count": len(pass_items),
        "alert_count": len(alert_items),
        "banned_count": len(banned_items),
        "has_critical_adulterant": has_crit,
        "recommendation": rec,
        "created_at": datetime.utcnow().isoformat()
    }
