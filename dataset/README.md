# FoodGuard — Packaged Food Safety & Regulatory Dataset

## Dataset Specifications

This dedicated dataset directory contains the standardized food additive, regulatory compliance, and industrial adulterant screening catalog for **FoodGuardAI**.

- **File**: `300_packaged_food_dataset.csv`
- **Total Records**: 300 Records
- **Standardized Schema**:
  1. `record_id`: Sequential Unique Identifier (1 to 300)
  2. `company_or_manufacturer`: Target Brand or FMCG Manufacturer (Parle, Britannia, Nestlé, PepsiCo, Coca-Cola, Mondelez, Amul, etc.)
  3. `product_category`: Food Category Classification (Confectionery, Bakery, Noodles, Beverages, Dairy, Snacks)
  4. `product_name`: Standard Formulated Product Item / Additive
  5. `common_label_name`: Front-of-Package / Back-of-Package Label Ingredient Name
  6. `scientific_chemical_name`: IUPAC / Chemical Nomenclature
  7. `codex_ins_no`: International Numbering System (Codex Alimentarius INS No.)
  8. `india_fssai_status`: Regulatory Compliance Status under FSSAI (India)
  9. `usa_status`: Regulatory Compliance Status under US FDA (21 CFR)
  10. `eu_status`: Regulatory Compliance Status under European Food Safety Authority (EFSA / EC 1333/2008)
  11. `eu_e_number`: European Union Food Additive E-Number (e.g. E102, E171, E927a)
  12. `usa_regulatory_reference`: Code of Federal Regulations Reference (e.g. 21 CFR 74.705)
  13. `australia_nz_code`: Food Standards Australia New Zealand (FSANZ) Code
  14. `screening_note`: Safety Guidance, Maximum Permitted Limit, or Category Verification Instruction

## Matching & Regulatory Alert Logic
1. Every input (from 1D/2D Barcode Scan, Camera Photo Snapshot, or Image Upload) extracts ingredients and standardizes Codex INS numbers / common additive names.
2. Ingredients are cross-referenced directly against `300_packaged_food_dataset.csv`.
3. If permissions across all countries/unions (India, USA, European Union, Australia) are Permitted, the system confirms clean status (Low Risk).
4. If ANY authority revokes, restricts, or bans an ingredient:
   - System raises a clear alert identifying:
     - **Specific INS / E-Number** (e.g. INS 171, INS 924a, INS 127)
     - **Ingredient Name** (e.g. Titanium Dioxide, Potassium Bromate, Erythrosine)
     - **Country / Authority that issued the ban/restriction** (e.g. European Union - EFSA, USA - FDA, India - FSSAI)
     - **Transparent reason & regulatory reference** for the alert.
