# FoodGuard — Restricted Substances & Health Hazards Dataset
## Problems Faced by Restricted & Banned Food Additives and Industrial Adulterants

### Document Overview
- **Project Domain:** Food Safety, Regulatory Compliance & Computer Vision OCR
- **Dataset Files:** 
  - `dataset/restricted_substances_hazards_dataset.csv`
  - `dataset/restricted_substances_hazards_dataset.json`
- **Total Detailed Toxicological Profiles:** 20 Substances
- **Governing Authorities Covered:** India (FSSAI), USA (US FDA), European Union (EFSA), World Health Organization (WHO / JECFA)

---

### 1. Executive Summary & Purpose
When an additive or chemical substance is flagged with a **Red Alert** in food safety analysis, regulatory decisions are driven by specific biomedical, clinical, and physiological harms identified in clinical bioassays and epidemiological cohorts.

This dataset provides the definitive reference mapping between:
1. **Additive Identifiers:** Codex INS number, EU E-number, and chemical nomenclature.
2. **Problems Faced (Clinical Hazards):** The specific diseases, toxicological pathologies, and adverse biological reactions caused by the substance.
3. **Biological Organ Systems Affected:** Target anatomical organs (e.g., Cellular DNA, Thyroid Gland, Renal Tubules, Respiratory Epithelium, Nervous System).
4. **Governing Authority Action & Citations:** The specific regulatory notices (e.g., Regulation (EU) 2022/63, 21 CFR 74.303, FSSAI Gazettes).
5. **Safer Permitted Alternatives:** Non-toxic substitute ingredients for manufacturers.

---

### 2. Comprehensive Toxicological Profiles Matrix

| Code | Substance Name | Primary Organ | Problem Faced (Clinical & Biological Hazards) | Restriction Status | Safer Alternative |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **INS 171** | Titanium Dioxide | Cellular DNA & Gut | **Genotoxicity:** DNA strand breaks, chromosomal damage, nanoparticle bioaccumulation in gut mucosa; no safe ADI can be established. | **BANNED in EU (2022)**; Permitted in USA & India with limits | Calcium Carbonate (INS 170i), Rice starch |
| **INS 127** | Erythrosine (Red 3) | Thyroid Gland & Endocrine | **Thyroid Carcinogenesis:** Follicular cell hypertrophy and adenomas; pediatric hyperactivity; Delaney Clause prohibition. | **REVOKED by US FDA**; Restricted in EU solely to cherries | Beetroot Red (INS 162), Anthocyanins (INS 163) |
| **INS 927a** | Azodicarbonamide | Respiratory System | **Respiratory Sensitization:** Occupational asthma, allergic rhinitis; thermal decomposition yields semicarbazide (SEM) and urethane. | **BANNED in EU & UK**; Permitted up to 45 ppm in USA/India | Ascorbic Acid (INS 300), Fungal enzymes |
| **INS 924a** | Potassium Bromate | Renal (Kidneys) & Thyroid | **IARC Group 2B Carcinogen:** Renal cell tumors, thyroid adenocarcinomas, irreversible oxidative DNA damage (8-OHdG). | **STRICTLY BANNED in India (2016) & EU**; Permitted in USA | Ascorbic Acid (INS 300), Lecithin (INS 322) |
| **BVO** | Brominated Vegetable Oil | Thyroid, Heart & Liver | **Bromism & Bioaccumulation:** Bromine accumulation in fat tissue, myocardial damage, thyroid follicular lesions; neurotoxicity. | **REVOKED by US FDA (2024)**; Banned in EU & India | Glycerol Ester of Wood Rosin (INS 445) |
| **INS 102** | Tartrazine (Yellow 5) | Nervous & Immune Systems | **Pediatric Hyperactivity:** Behavioral disruption, ADHD aggravation; severe urticaria/asthma in aspirin-intolerant patients. | **Mandatory Warning Label in EU**; Permitted with limits in USA/India | Curcumin (INS 100), Beta-Carotene (INS 160a) |
| **INS 110** | Sunset Yellow FCF | Nervous & Immune Systems | **Restlessness & Inattention:** Pediatric hyperactivity (Southampton study); allergic rhinitis, angioedema, lowered ADI. | **Mandatory Warning Label in EU**; Permitted with limits in USA/India | Paprika Extract (INS 160c), Annatto |
| **INS 122** | Carmoisine / Azorubine | Respiratory & Skin | **Bronchospasm & Urticaria:** Acute asthma in aspirin-intolerant individuals; pediatric behavioral disruption; in-vitro genotoxicity. | **BANNED in USA & Canada**; Permitted in India; Warning in EU | Anthocyanins (INS 163), Black Carrot Extract |
| **INS 124** | Ponceau 4R | Hepatic & Immune Systems | **Hypersensitivity & Asthma:** Chronic urticaria; pediatric behavioral disruption; suspected renal DNA damage at high doses. | **BANNED in USA**; Permitted in India; Strict EU warning label | Red Beet Juice (INS 162), Lycopene |
| **INS 104** | Quinoline Yellow | Neurological & Skin | **Sensitization & Restlessness:** Allergic contact dermatitis, asthma exacerbation; loss of concentration in children. | **BANNED in USA & Canada**; Permitted in India & EU | Safflower extract, Riboflavin (INS 101) |
| **INS 143** | Fast Green FCF | Cellular Integrity & Gut | **Injection-Site Sarcomas:** Mutagenic and clastogenic responses in animal cell systems; poorly absorbed in intestinal tract. | **BANNED in European Union**; Permitted in USA & India | Chlorophyllin Copper Complexes (INS 141) |
| **INS 952** | Sodium Cyclamate | Bladder & Reproductive | **Bladder Tumors:** Rat bioassay bladder tumor concerns; metabolite cyclohexylamine causes testicular atrophy in rodents. | **BANNED in USA since 1969**; Permitted with limits in EU/India | Steviol Glycosides (INS 960), Erythritol |
| **INS 320** | BHA | Endocrine & Gut Mucosa | **Suspected Carcinogen:** Forestomach papillomas and carcinomas in rodents; disrupts thyroid/sex steroid hormones. | **RESTRICTED** with strict max thresholds (200 mg/kg) | Mixed Tocopherols (INS 306), Rosemary Extract |
| **INS 319** | TBHQ | Immune System & Liver | **Immune Suppression:** Suppresses T-cell surveillance; cytotoxicity; vision disturbances upon accidental acute exposure. | **RESTRICTED** (max 200 ppm); Prohibited in infant food | Rosemary Extract (INS 392), Nitrogen flushing |
| **ADULT-SR** | Sudan Dyes (I-IV) | Liver & Genomic DNA | **Genotoxic Carcinogen:** Severe hepatic carcinomas, bladder tumors; metabolized into reactive aromatic amines (aniline). | **ZERO TOLERANCE ILLEGAL ADULTERANT** Worldwide | Pure Sun-Dried Paprika / Chilli |
| **ADULT-MY** | Metanil Yellow | Brain & Testes | **Neurotoxicity:** Brain monoamine neurotransmitter depletion (dopamine/serotonin); testicular atrophy, reduced sperm motility. | **STRICTLY ILLEGAL ADULTERANT** in Dal/Laddus | Pure Turmeric (Haldi), Saffron (Kesar) |
| **ADULT-RB** | Rhodamine B | DNA, Liver & Kidneys | **Clastogenic Mutagen:** Direct DNA intercalation, acute hepatocellular necrosis, fluorescent dye poisoning. | **STRICTLY BANNED INDUSTRIAL DYE** in Cotton Candy | Natural Beetroot Extract (INS 162) |
| **ADULT-MEL** | Melamine | Renal System (Kidneys) | **Acute Renal Failure:** Forms insoluble melamine-cyanurate stones blocking renal tubules; infant nephrotoxicity. | **STRICTLY ILLEGAL MILK ADULTERANT** Worldwide | Natural unadulterated cow/buffalo milk |
| **ADULT-FORM** | Formalin | GI Tract & Respiratory | **IARC Group 1 Carcinogen:** Corrosive GI tract ulcerations, nasopharyngeal carcinoma, severe vomiting, protein cross-linking. | **STRICTLY ILLEGAL FISH PRESERVATIVE** | Cold-chain refrigerated storage (0-4°C) |
| **ADULT-ARG** | Argemone Oil | Capillaries & Eyes | **Epidemic Dropsy:** Capillary hyperpermeability, bilateral leg edema, heart failure, optic nerve damage and blindness. | **STRICTLY PROHIBITED MUSTARD OIL ADULTERANT** | Pure cold-pressed kachi ghani mustard oil |
