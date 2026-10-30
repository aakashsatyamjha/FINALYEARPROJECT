# FoodGuard — Packaged Food Safety & Regulatory Assessment System
## 300-Record Food Additive, Adulteration & Multi-Country Regulatory Dataset Specification

### Document Overview
- **Project Domain:** Food Safety, Regulatory Compliance & Computer Vision OCR
- **Dataset File:** `300_packaged_food_dataset.csv`
- **Total Records:** 300 Standardized Product/Additive Records
- **Governing Authorities:** India (FSSAI), USA (US FDA), European Union (EFSA), Australia/NZ (FSANZ)
- **Technical Architecture:** React 19 + FastAPI + Python Decision Engine + PaddleOCR Computer Vision

---

### 1. Executive Summary & Problem Definition
In contemporary packaged food manufacturing, formulations incorporate diverse chemical additives, synthetic colorants, preservatives, stabilizers, emulsifiers, and non-nutritive sweeteners. Crucially, legal permissions, maximum permissible exposure limits, and statutory labeling requirements diverge drastically between international regulatory bodies.

An additive authorized in one jurisdiction may be prohibited or revoked in another due to emerging clinical evidence regarding genotoxicity, endocrine disruption, or carcinogenicity:
- **Titanium Dioxide (INS 171):** Banned across the European Union under Regulation (EU) 2022/63 due to DNA strand-break concerns, yet permitted in the USA and India.
- **Erythrosine / Red No. 3 (INS 127):** Authorization revoked by the US FDA for food use under 21 CFR 74.303, while restricted only to cocktail cherries in Europe and permitted with limits in India.
- **Potassium Bromate (INS 924a):** Strictly banned in India (FSSAI 2016) and the European Union as an IARC Group 2B probable human carcinogen, yet permitted for certain baking uses in the USA.
- **Azodicarbonamide (INS 927a):** Banned in the European Union and the UK due to respiratory sensitization and semicarbazide thermal degradation products.
- **Brominated Vegetable Oil (BVO):** Explicitly revoked by the US FDA in 2024 following bioaccumulation and thyroid toxicity studies; long prohibited in Europe.

The **FoodGuard 300-Record Regulatory Dataset** provides a centralized, normalized benchmark that empowers automated scanning systems to cross-examine food items instantly against international legal baselines.

---

### 2. Standardized 15-Column Dataset Schema
The primary dataset file is stored at `dataset/300_packaged_food_dataset.csv` and adheres to the following 15-attribute schema:

| Column Name | Data Type | Description | Representative Values / Example |
| :--- | :--- | :--- | :--- |
| `record_id` | Integer | Unique primary key identifier | `1`, `2`, ..., `300` |
| `brand_or_manufacturer` | String | Target FMCG manufacturer or category brand | `Beverage Manufacturer`, `Parle`, `Britannia`, `Nestlé` |
| `product_category` | String | Standardized food category | `Soft Drink`, `Ice Cream`, `Extruded Snack`, `Bakery` |
| `product_name` | String | Specific packaged item or formulated additive | `Tartrazine`, `Titanium Dioxide / Colour`, `MSG` |
| `common_label_name` | String | Consumer-facing ingredient declaration name | `Tartrazine`, `Sodium Benzoate`, `Citric Acid` |
| `scientific_chemical_name` | String | Standard chemical nomenclature / IUPAC | `Disodium 2,4,5,7-tetraiodofluorescein`, `Citric acid` |
| `codex_ins_no` | String | Codex Alimentarius INS identification code | `102`, `110`, `127`, `171`, `211`, `621`, `924a` |
| `fssai_reference_status` | String | Statutory status under FSSAI regulations (India) | `Permitted`, `Permitted with limits`, `Not permitted` |
| `usa_reference_status` | String | Statutory status under US FDA 21 CFR | `Permitted`, `Authorization revoked; phase-out` |
| `eu_reference_status` | String | Statutory status under EFSA / Regulation 1333/2008 | `Permitted`, `Restricted uses`, `Not authorised` |
| `eu_e_number` | String | European Union authorized E-number | `E102`, `E110`, `E127`, `E171`, `E211`, `E621` |
| `us_identifier_reference` | String | US FDA regulatory citation code | `FD&C Yellow No. 5; 21 CFR 74.705`, `21 CFR 184.1733` |
| `australia_nz_code` | String | FSANZ Food Standards Code identifier | `102`, `110`, `127`, `171`, `211`, `621` |
| `screening_note` | String | Statutory limit, screening advice, or warning | `Verify maximum level in beverage`, `Mandatory warning` |
| `source` | String | Ground truth provenance citation | Official regulatory gazettes and dataset expansion |

---

### 3. Country-Wise Regulatory Comparison Matrix
The table below illustrates representative regulatory divergences captured in the dataset:

| INS Code | Substance Name | India (FSSAI) | USA (US FDA) | European Union (EFSA) | Australia / NZ | Regulatory Alert Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **INS 171** | Titanium Dioxide | Specified uses | Permitted (21 CFR 73.575) | **Not authorised / Banned** | 171 | Banned in EU under Regulation (EU) 2022/63 due to genotoxicity concerns. |
| **INS 127** | Erythrosine (Red 3) | Permitted with limits | **Authorization revoked** | **Restricted to cherries** | 127 | FDA revoked authorization under 21 CFR 74.303; restricted in EU. |
| **INS 924a** | Potassium Bromate | **Not permitted / Banned** | Certain baking uses | **Not authorised / Banned** | 924a | Banned in India and EU as an IARC Group 2B probable carcinogen. |
| **INS 927a** | Azodicarbonamide | Specified uses | Permitted (21 CFR 172.806) | **Not authorised / Banned** | 927a | Banned in Europe & UK due to respiratory sensitization and semicarbazide. |
| **BVO** | Brominated Vegetable Oil | Category verification | **Revoked / Banned (2024)** | **Not authorised / Banned** | No code | Banned due to bioaccumulation and thyroid toxicity. |
| **INS 143** | Fast Green FCF | Specified uses | Permitted | **Not authorised in EU** | 143 | Unapproved under EU food additive registry. |
| **INS 952** | Cyclamate | Verification required | **Not permitted / Banned** | Permitted with limits | 952 | Banned in US as food additive; permitted in EU and UK. |
| **INS 102** | Tartrazine (Yellow 5) | Permitted with limits | Permitted | Mandatory warning label | 102 | Mandatory EU warning regarding attention and hyperactivity in children. |

---

### 4. Verification & Algorithmic Audit Pipeline
1. **Input Ingestion:** 
   - 1D/2D Barcode (Camera scanner or manual entry) queries Open Food Facts and the local catalog.
   - Ingredient packaging photos (Camera snapshot or file upload) are processed via **PaddleOCR** with OpenCV CLAHE contrast enhancement and adaptive thresholding.
2. **Standardization & Token Matching:**
   - Extracts all additive names, Codex INS codes, and E-numbers.
   - Searches indexed records in `300_packaged_food_dataset.csv`.
3. **Multi-Jurisdiction Permission Audit:**
   - Cross-checks status across India, USA, European Union, and Australia.
   - **All Permitted:** System reports `✓ All Regulatory Permissions OK — Low Risk`.
   - **Single Restriction or Ban:** System raises immediate alert specifying:
     - **INS / E-Number**
     - **Item Name**
     - **Authority that flagged it**
     - **Exact Reason and Legal Reference**

---

### 5. Dataset Distribution by Substance Category
| Food Additive / Ingredient Class | Record Count | Representative Substance Examples |
| :--- | :---: | :--- |
| **Food Colours & Synthetic Dyes** | 68 | Tartrazine, Sunset Yellow, Allura Red, Brilliant Blue, Erythrosine, Titanium Dioxide |
| **Preservatives & Antioxidants** | 74 | Sodium Benzoate, Potassium Sorbate, Sorbic Acid, BHA, BHT, TBHQ, Sodium Metabisulphite |
| **Emulsifiers, Stabilizers & Gums** | 52 | Lecithin, PGPR, Guar Gum, Xanthan Gum, DATEM, Mono- and Diglycerides |
| **Artificial & Natural Sweeteners** | 38 | Aspartame, Acesulfame-K, Sucralose, Saccharin, Cyclamate, Stevia, Xylitol |
| **Flavour Enhancers & Acidulants** | 36 | MSG (INS 621), Disodium Inosinate (INS 631), Guanylate (INS 627), Citric Acid |
| **Banned Toxic Chemical Adulterants** | 32 | Metanil Yellow, Lead Chromate, Rhodamine B, Sudan Dyes, Melamine, Formalin |
| **Total Standardized Records** | **300** | **Comprehensive coverage of packaged food formulations** |

---

### 6. Mentor Sign-Off & Verification
- **Dataset Location:** `dataset/300_packaged_food_dataset.csv`
- **PDF Report Location:** `dataset/FOOD_REGULATORY_DATASET_DOCUMENTATION.pdf`
- **Evaluation Status:** Fully verified and operational in live application.
