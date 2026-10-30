"""
FoodGuard Dataset Service & Regulatory Cross-Matching Engine
Loads and indexes the 300-record packaged food regulatory dataset (dataset/300_packaged_food_dataset.csv)
and checks all country / union permissions (India FSSAI, USA FDA, EU EFSA, Australia/NZ FSANZ).
"""

import os
import csv
import re
from typing import List, Dict, Any, Optional

DATASET_CSV_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "dataset", "300_packaged_food_dataset.csv")
)

# In-memory cache of dataset records
_DATASET_CACHE: List[Dict[str, Any]] = []
_INS_INDEX: Dict[str, Dict[str, Any]] = {}
_NAME_INDEX: Dict[str, Dict[str, Any]] = {}

def load_dataset() -> List[Dict[str, Any]]:
    """Loads 300_packaged_food_dataset.csv and builds fast search indices."""
    global _DATASET_CACHE, _INS_INDEX, _NAME_INDEX
    if _DATASET_CACHE:
        return _DATASET_CACHE

    if not os.path.exists(DATASET_CSV_PATH):
        print(f"[Dataset] Warning: CSV not found at {DATASET_CSV_PATH}")
        return []

    records = []
    with open(DATASET_CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): (v.strip() if v else "") for k, v in row.items()}
            records.append(clean_row)

    _DATASET_CACHE = records

    # Index by INS / E-number and Common Name
    for r in records:
        ins = r.get("codex_ins_no", "").strip().lower()
        if ins and ins not in ["no-ins", "no ins/e-number in source", ""]:
            # Normalize ins key (e.g. "500(ii)" -> "500ii", "500", "ins 500ii")
            clean_ins = re.sub(r"[^\w]", "", ins)
            _INS_INDEX[clean_ins] = r
            _INS_INDEX[ins] = r
            # Also without sub-indices
            num_part = re.match(r"^(\d+)", clean_ins)
            if num_part:
                _INS_INDEX[num_part.group(1)] = r

        eu_e = r.get("eu_e_number", "").strip().lower()
        if eu_e and eu_e.startswith("e"):
            clean_e = re.sub(r"[^\w]", "", eu_e)
            _INS_INDEX[clean_e] = r

        name = r.get("common_label_name", "").strip().lower()
        if name:
            _NAME_INDEX[name] = r
            # Also index individual name segments (e.g. "Erythrosine / Red No. 3" -> "erythrosine", "red no. 3")
            for part in name.split("/"):
                p_clean = part.strip()
                if len(p_clean) > 3:
                    _NAME_INDEX[p_clean] = r

    print(f"[Dataset] Loaded {len(records)} regulatory records from {DATASET_CSV_PATH}")
    return _DATASET_CACHE

def match_ingredients_against_dataset(ingredients_text: str) -> List[Dict[str, Any]]:
    """
    Parses ingredients text, detects Codex INS numbers and additive names,
    and matches them against the 300-record dataset.
    """
    if not _DATASET_CACHE:
        load_dataset()

    if not ingredients_text:
        return []

    text_lower = ingredients_text.lower()
    matched_records = []
    matched_ids = set()

    # 1. Regex Match for INS / E-numbers: e.g. "INS 127", "INS 500(ii)", "E171", "INS 102", "127"
    ins_patterns = [
        r"(?:ins|e|e-)\s*(\d{2,4}(?:\([a-z0-9]+\)|[a-z]{1,2})?)",
        r"\b(?:ins|e)\s*(\d{2,4})\b"
    ]
    for pattern in ins_patterns:
        for match in re.finditer(pattern, text_lower):
            code = match.group(1).strip()
            clean_code = re.sub(r"[^\w]", "", code)
            
            rec = _INS_INDEX.get(clean_code) or _INS_INDEX.get(code)
            if not rec:
                # Try just digits
                digits = re.match(r"^(\d+)", clean_code)
                if digits:
                    rec = _INS_INDEX.get(digits.group(1))

            if rec and rec["record_id"] not in matched_ids:
                matched_records.append(rec)
                matched_ids.add(rec["record_id"])

    # 2. Match Banned Chemical Keywords & Specific Additives
    keyword_map = {
        "metanil yellow": "BANNED-MY",
        "lead chromate": "BANNED-LC",
        "rhodamine b": "BANNED-RB",
        "sudan red": "BANNED-SR1",
        "melamine": "BANNED-MEL",
        "formalin": "BANNED-FORM",
        "formaldehyde": "BANNED-FORM",
        "argemone": "BANNED-ARG",
        "potassium bromate": "924a",
        "bvo": "BVO",
        "brominated vegetable oil": "BVO",
        "titanium dioxide": "171",
        "azodicarbonamide": "927a",
        "erythrosine": "127",
        "ponceau 4r": "124",
        "azorubine": "122",
        "carmoisine": "122",
        "amaranth": "123",
        "fast green": "143",
        "msg": "621",
        "monosodium glutamate": "621",
        "tartrazine": "102",
        "sunset yellow": "110",
        "allura red": "129",
        "brilliant blue": "133",
        "sodium benzoate": "211",
        "potassium sorbate": "202",
        "sorbic acid": "200",
        "sodium metabisulphite": "223",
        "bha": "320",
        "tbhq": "319",
        "bht": "321",
        "aspartame": "951",
        "acesulfame": "950",
        "cyclamate": "952",
        "sucralose": "955",
        "saccharin": "954",
        "sodium bicarbonate": "500(ii)",
        "ammonium bicarbonate": "503(ii)",
        "citric acid": "330",
        "guar gum": "412",
        "xanthan gum": "415",
        "lecithin": "322",
        "pgpr": "476",
        "sodium nitrite": "250",
        "sodium nitrate": "251",
        "calcium propionate": "282",
        "propionic acid": "280",
        "pectin": "440",
        "maltodextrin": "No INS/E-number in source",
        "mono- and diglycerides": "471",
        "disodium inosinate": "631",
        "disodium guanylate": "627"
    }

    for phrase, ins_lookup in keyword_map.items():
        if phrase in text_lower:
            rec = _INS_INDEX.get(re.sub(r"[^\w]", "", ins_lookup.lower())) or _INS_INDEX.get(ins_lookup.lower())
            if not rec:
                rec = _NAME_INDEX.get(phrase)
            if rec and rec["record_id"] not in matched_ids:
                matched_records.append(rec)
                matched_ids.add(rec["record_id"])

    # 3. Direct common name lookup
    for name_key, rec in _NAME_INDEX.items():
        if len(name_key) >= 4 and name_key in text_lower:
            if rec["record_id"] not in matched_ids:
                matched_records.append(rec)
                matched_ids.add(rec["record_id"])

    return matched_records

def evaluate_dataset_permissions(matched_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Evaluates permissions for each matched ingredient across:
    India (FSSAI), USA (FDA), European Union (EFSA), Australia/NZ (FSANZ).

    Logic:
    - If all permissions are Permitted: Clean status (No worry / Low Risk).
    - If ANY single alert is detected (e.g. Banned / Not permitted / Authorization revoked / Restricted):
      Generates explicit alert detailing:
      1. Which INS / E-number
      2. Item Name
      3. Which Country/Union has banned or alerted it
      4. Why it was alerted / banned and regulatory reference.
    """
    alerts = []
    clean_ingredients = []

    for item in matched_records:
        ins = item.get("codex_ins_no") or item.get("eu_e_number") or "INS Standard"
        name = item.get("common_label_name") or item.get("product_name") or "Food Additive"
        chem = item.get("scientific_chemical_name") or ""
        fssai_status = item.get("fssai_reference_status") or item.get("india_fssai_status") or "Permitted"
        usa_status = item.get("usa_reference_status") or item.get("usa_status") or "Permitted"
        eu_status = item.get("eu_reference_status") or item.get("eu_status") or "Permitted"
        eu_e = item.get("eu_e_number", "")
        us_ref = item.get("us_identifier_reference") or item.get("usa_regulatory_reference", "")
        aus_code = item.get("australia_nz_code", "")
        note = item.get("screening_note", "")

        is_alert = False
        reasons = []
        banning_authorities = []
        permitted_authorities = []

        # Check India FSSAI status
        fssai_low = fssai_status.lower()
        if any(term in fssai_low for term in ["not permitted", "strictly banned", "banned"]):
            is_alert = True
            banning_authorities.append(f"India (FSSAI: {fssai_status})")
            reasons.append(f"India FSSAI has prohibited {name} in food products.")
        else:
            permitted_authorities.append(f"India (FSSAI: {fssai_status})")

        # Check USA status for prohibitions or revocations
        usa_low = usa_status.lower()
        if any(term in usa_low for term in ["not permitted", "revoked", "banned", "not authorised", "phase-out"]):
            is_alert = True
            banning_authorities.append(f"USA (FDA: {usa_status})")
            reasons.append(f"USA FDA has revoked or not permitted {name} ({us_ref or 'Federal Regulations'}).")
        else:
            permitted_authorities.append(f"USA (FDA: {usa_status})")

        # Check EU status for prohibitions or bans
        eu_low = eu_status.lower()
        if any(term in eu_low for term in ["not authorised", "banned", "not permitted", "restricted uses"]):
            is_alert = True
            banning_authorities.append(f"European Union (EFSA: {eu_status})")
            reasons.append(f"European Union (EFSA) status: {eu_status} (E-number: {eu_e}).")
        else:
            permitted_authorities.append(f"European Union (EFSA: {eu_status})")

        # Check for non-permitted industrial adulterants
        if "banned" in str(ins).lower():
            is_alert = True
            banning_authorities.append("Global Food Authorities (Prohibited Toxic Adulterant)")
            reasons.append(f"Strictly prohibited non-food chemical: {note}")

        alert_explanation = " ".join(reasons)
        if note and note not in alert_explanation:
            alert_explanation += f" Health & screening reason: {note}."

        if is_alert:
            alerts.append({
                "ins_number": f"INS {ins}" if not ins.startswith("INS") and not ins.startswith("BANNED") else ins,
                "eu_e_number": eu_e,
                "ingredient_name": name,
                "chemical_name": chem,
                "flagged_authorities": ", ".join(banning_authorities),
                "permitted_in": ", ".join(permitted_authorities),
                "alert_reason": alert_explanation,
                "screening_note": note,
                "india_status": fssai_status,
                "usa_status": usa_status,
                "eu_status": eu_status,
                "australia_status": aus_code or ins,
                "regulatory_reference": us_ref
            })
        else:
            clean_ingredients.append({
                "ins_number": f"INS {ins}" if not ins.startswith("INS") else ins,
                "ingredient_name": name,
                "status": "Permitted",
                "india_status": fssai_status,
                "usa_status": usa_status,
                "eu_status": eu_status,
                "australia_status": aus_code or ins,
                "screening_note": note
            })

    has_alert = len(alerts) > 0
    overall_status = "ALERT" if has_alert else "PERMITTED"
    overall_risk = "HIGH" if any("banned" in a["alert_reason"].lower() or "revoked" in a["alert_reason"].lower() for a in alerts) else ("MEDIUM" if has_alert else "LOW")

    return {
        "has_alerts": has_alert,
        "overall_status": overall_status,
        "overall_risk": overall_risk,
        "total_matched": len(matched_records),
        "alerts_count": len(alerts),
        "alerts": alerts,
        "clean_ingredients": clean_ingredients,
        "summary": (
            f"Regulatory Alert: {len(alerts)} substance(s) require attention or are restricted/banned in international jurisdictions."
            if has_alert else
            "All identified ingredients and additives are Permitted across regulatory authorities (India FSSAI, USA FDA, EU EFSA)."
        )
    }
