"""
Builds the Restricted Substances Health Hazards & Toxicological Reference Dataset.
Generates:
1. dataset/restricted_substances_hazards_dataset.csv
2. dataset/restricted_substances_hazards_dataset.json
3. frontend/src/data/restricted_substances_hazards.json
"""

import os
import json
import pandas as pd

HAZARDS_DATA = [
    {
        "hazard_id": "HAZ-001",
        "ins_code": "INS 171",
        "eu_e_number": "E171",
        "common_name": "Titanium Dioxide",
        "scientific_chemical_name": "Titanium dioxide (TiO2 nanoparticles)",
        "food_applications": "White frosting, chewing gum, candies, bakery glazes, sauces, dairy whiteners",
        "restriction_status": "BANNED in European Union (2022); Permitted in USA & India with limitations",
        "primary_organ_affected": "Cellular DNA & Gastrointestinal Tract",
        "health_problems_faced": "Genotoxicity (DNA strand breaks, chromosomal aberration), systemic nanoparticle bioaccumulation in intestinal mucosa, liver, and spleen; unable to establish a safe Acceptable Daily Intake (ADI).",
        "toxicological_mechanism": "Induces reactive oxygen species (ROS) upon cellular uptake, leading to oxidative DNA damage and disruption of the intestinal epithelial barrier.",
        "governing_authority_actions": "EFSA concluded TiO2 can no longer be considered safe as a food additive (Regulation EU 2022/63). US FDA 21 CFR 73.575 currently permits up to 1% by weight.",
        "statutory_citation": "Regulation (EU) 2022/63; EFSA Journal 2021;19(5):6585; 21 CFR 73.575",
        "safer_permitted_alternatives": "Calcium Carbonate (INS 170i), Rice starch, Microcrystalline cellulose"
    },
    {
        "hazard_id": "HAZ-002",
        "ins_code": "INS 127",
        "eu_e_number": "E127",
        "common_name": "Erythrosine / FD&C Red No. 3",
        "scientific_chemical_name": "Disodium 2,4,5,7-tetraiodofluorescein",
        "food_applications": "Maraschino cherries, glazed confectionery, popsicles, cake decorating gels, strawberry milk powder",
        "restriction_status": "REVOKED by US FDA for ingested cosmetics/lakes; Banned in US for cosmetics; Under federal phase-out in food; RESTRICTED in EU solely to cocktail/candied cherries; Permitted with limits in India",
        "primary_organ_affected": "Endocrine System & Thyroid Gland",
        "health_problems_faced": "Thyroid follicular cell hypertrophy and adenomas/carcinogenesis; hyperthyroidism; pediatric neurobehavioral hyperactivity; iodine overload.",
        "toxicological_mechanism": "Inhibits peripheral conversion of thyroxine (T4) to triiodothyronine (T3), causing elevated thyroid-stimulating hormone (TSH) and chronic thyroid cell proliferation.",
        "governing_authority_actions": "US FDA revoked authorizations under Delaney Clause (21 CFR 74.303); California Food Safety Act enacted state-wide ban by 2027. EU restricted under Regulation (EC) 1333/2008.",
        "statutory_citation": "21 CFR 74.303; California AB 418 (2023); Regulation (EC) No 1333/2008 Annex II",
        "safer_permitted_alternatives": "Beetroot Red (INS 162), Anthocyanins (INS 163), Carmine/Cochineal (INS 120)"
    },
    {
        "hazard_id": "HAZ-003",
        "ins_code": "INS 927a",
        "eu_e_number": "E927a",
        "common_name": "Azodicarbonamide (ADA)",
        "scientific_chemical_name": "1,1'-Azobisformamide",
        "food_applications": "Commercial white bread, hamburger buns, pizza dough, flour conditioning agent",
        "restriction_status": "BANNED in European Union, United Kingdom, and Australia; Permitted up to 45 ppm in USA and India",
        "primary_organ_affected": "Respiratory System & Cellular Metabolism",
        "health_problems_faced": "Severe respiratory sensitization, occupational asthma, allergic rhinitis; thermal decomposition creates carcinogenic semicarbazide (SEM) and urethane (ethyl carbamate).",
        "toxicological_mechanism": "Thermal breakdown during baking yields semicarbazide (SEM), a known genotoxic carcinogen in animal models that induces DNA damage and vascular tumors.",
        "governing_authority_actions": "Banned in EU under Directive 2004/1/EC for food contact and prohibited as additive. US FDA allows under 21 CFR 172.806.",
        "statutory_citation": "Commission Directive 2004/1/EC; 21 CFR 172.806; WHO Food Additive Series 30",
        "safer_permitted_alternatives": "Ascorbic Acid (Vitamin C / INS 300), Fungal alpha-amylase, Proteases"
    },
    {
        "hazard_id": "HAZ-004",
        "ins_code": "INS 924a",
        "eu_e_number": "E924a",
        "common_name": "Potassium Bromate",
        "scientific_chemical_name": "Potassium bromate (KBrO3)",
        "food_applications": "Flour bleaching, bread dough strengthening and volume expansion",
        "restriction_status": "STRICTLY BANNED in India (FSSAI 2016), European Union, Canada, UK, China, and Brazil; Permitted in USA with advisory limit",
        "primary_organ_affected": "Renal (Kidneys), Thyroid & Auditory System",
        "health_problems_faced": "Classified as an IARC Group 2B probable human carcinogen; induces renal cell tumors, thyroid follicular adenocarcinomas, peritoneal mesotheliomas, and ototoxicity (hearing impairment).",
        "toxicological_mechanism": "Strong oxidizing agent that generates 8-hydroxydeoxyguanosine (8-OHdG) in renal cellular DNA, triggering irreversible lipid peroxidation and mutagenesis.",
        "governing_authority_actions": "FSSAI banned in 2016 following CSE study showing residues in commercial breads. Prohibited by Codex Alimentarius and European Union.",
        "statutory_citation": "FSSAI Notification No. 1-12/Standards/SP(L&C/A)/FSSAI-2015; IARC Monographs Vol 73 (1999)",
        "safer_permitted_alternatives": "Ascorbic Acid (INS 300), Glucose oxidase, Lecithin (INS 322)"
    },
    {
        "hazard_id": "HAZ-005",
        "ins_code": "BVO",
        "eu_e_number": "None",
        "common_name": "Brominated Vegetable Oil (BVO)",
        "scientific_chemical_name": "Brominated triglyceride fatty acids",
        "food_applications": "Citrus-flavored sodas, sports beverages, fruit drinks (emulsifier/clouding agent)",
        "restriction_status": "REVOKED / BANNED by US FDA (effective 2024); Banned in European Union, India, and Japan",
        "primary_organ_affected": "Thyroid Gland, Heart Muscle & Hepatic Tissues",
        "health_problems_faced": "Bioaccumulation of elemental bromine in adipose tissue and vital organs; myocardial degeneration; thyroid follicular cell hyperplasia; reproductive neurotoxicity; bromism symptoms (headache, fatigue, memory loss).",
        "toxicological_mechanism": "Competes with iodine in thyroid uptake; brominated fatty acids integrate into myocardial lipids, inhibiting cellular energy metabolism and normal organelle turnover.",
        "governing_authority_actions": "US FDA revoked food additive regulation (21 CFR 180.30) in July 2024 after NIH toxicology bioassays demonstrated cumulative systemic toxicity.",
        "statutory_citation": "US FDA Final Rule 89 FR 55040 (July 3, 2024); Regulation (EC) 1333/2008",
        "safer_permitted_alternatives": "Glycerol Ester of Wood Rosin (INS 445), Sucrose Acetate Isobutyrate (INS 444)"
    },
    {
        "hazard_id": "HAZ-006",
        "ins_code": "INS 102",
        "eu_e_number": "E102",
        "common_name": "Tartrazine / FD&C Yellow No. 5",
        "scientific_chemical_name": "Trisodium 5-hydroxy-1-(4-sulfonatophenyl)-4-(4-sulfonatophenylazo)pyrazole-3-carboxylate",
        "food_applications": "Flavored potato chips, instant noodles, sodas, energy drinks, confectionery, gelatin desserts",
        "restriction_status": "PERMITTED with strict limits in India & USA; MANDATORY WARNING LABEL in European Union ('May have an adverse effect on activity and attention in children')",
        "primary_organ_affected": "Central Nervous System & Immune/Respiratory System",
        "health_problems_faced": "Pediatric neurobehavioral hyperactivity, Attention Deficit Hyperactivity Disorder (ADHD) aggravation; cross-reactive hypersensitivity in aspirin-sensitive asthmatics (severe bronchoconstriction and urticaria).",
        "toxicological_mechanism": "Azo-dye metabolism releases sulfanilic acid which triggers histamine degranulation from mast cells and alters central neurochemical signaling.",
        "governing_authority_actions": "European Union Regulation (EC) No 1333/2008 Annex V mandates statutory warning label on retail packaging. FSSAI sets max level of 100 mg/kg in finished food.",
        "statutory_citation": "Regulation (EC) No 1333/2008 Annex V; Southampton Study (McCann et al., Lancet 2007)",
        "safer_permitted_alternatives": "Curcumin (INS 100), Beta-Carotene (INS 160a), Lutein (INS 161b)"
    },
    {
        "hazard_id": "HAZ-007",
        "ins_code": "INS 110",
        "eu_e_number": "E110",
        "common_name": "Sunset Yellow FCF / FD&C Yellow No. 6",
        "scientific_chemical_name": "Disodium 6-hydroxy-5-[(4-sulfophenyl)azo]-2-naphthalenesulfonate",
        "food_applications": "Cheese-flavored extruded snacks, orange sodas, biscuits, jams, confectionery, breakfast cereals",
        "restriction_status": "PERMITTED with quantitative limits in India & USA; EU MANDATORY WARNING LABEL regarding pediatric hyperactivity; ADI lowered by EFSA",
        "primary_organ_affected": "Neurological & Immune Systems",
        "health_problems_faced": "Increased motor restlessness and inattention in children; allergic rhinitis, angioedema, contact dermatitis; potential gastric irritation in sensitive individuals.",
        "toxicological_mechanism": "Azo linkage cleaved by intestinal microflora into aromatic amines that elicit immunoglobulin E-independent mast cell mediator release.",
        "governing_authority_actions": "EFSA reduced Acceptable Daily Intake (ADI) from 2.5 to 1.0 mg/kg bw/day. Statutory EU warning label required.",
        "statutory_citation": "EFSA Journal 2014;12(7):3765; 21 CFR 74.706; FSSAI Food Additives Regulations",
        "safer_permitted_alternatives": "Paprika Extract (INS 160c), Annatto (INS 160b), Beta-Carotene (INS 160a)"
    },
    {
        "hazard_id": "HAZ-008",
        "ins_code": "INS 122",
        "eu_e_number": "E122",
        "common_name": "Carmoisine / Azorubine",
        "scientific_chemical_name": "Disodium 4-hydroxy-3-[(4-sulfonato-1-naphthyl)azo]naphthalene-1-sulfonate",
        "food_applications": "Jellies, soft drinks, confectionery, cough drops, ice creams, flavored yogurts",
        "restriction_status": "BANNED / NOT AUTHORIZED in USA and Canada; Permitted with limits in India; Mandatory warning label in EU",
        "primary_organ_affected": "Respiratory & Dermatological Systems",
        "health_problems_faced": "Acute asthmatic episodes in aspirin-intolerant patients; generalized urticaria; pediatric behavioral disruption; potential genotoxic risk in in-vitro assays.",
        "toxicological_mechanism": "Reductive cleavage of the azo bond forms naphthionic acid metabolites that promote leukotriene synthesis and bronchospasm.",
        "governing_authority_actions": "Never approved by the US FDA for food use. EU mandates statutory warning under Regulation 1333/2008.",
        "statutory_citation": "US FDA 21 CFR Chapter I; EFSA Journal 2009; 7(11):1332; FSSAI Standards 2.11",
        "safer_permitted_alternatives": "Anthocyanins (INS 163), Beetroot Red (INS 162), Black Carrot Extract"
    },
    {
        "hazard_id": "HAZ-009",
        "ins_code": "INS 124",
        "eu_e_number": "E124",
        "common_name": "Ponceau 4R / Cochineal Red A",
        "scientific_chemical_name": "Trisodium 1-(4-sulfo-1-naphthylazo)-2-naphthol-6,8-disulfonate",
        "food_applications": "Fruit pie fillings, dessert mixes, sodas, cured sausages, confectionery, candied fruits",
        "restriction_status": "BANNED / NOT AUTHORIZED in USA; Permitted with limits in India; Mandatory hyperactivity warning label in EU; ADI significantly reduced by EFSA",
        "primary_organ_affected": "Hepatic & Immune Systems",
        "health_problems_faced": "Exacerbation of asthma, chronic urticaria, and angioedema; hyperactivity in preschool and school-age children; suspected renal DNA damage at high exposures.",
        "toxicological_mechanism": "Metabolized to 1-naphthylamine-4-sulfonic acid and 2-naphthol-6,8-disulfonic acid, provoking oxidative cellular stress.",
        "governing_authority_actions": "Prohibited in the United States by FDA. EU lowered ADI to 0.7 mg/kg bw/day.",
        "statutory_citation": "21 CFR (Unlisted / Prohibited); EFSA Journal 2009; 7(11):1328; FSSAI Color Regulations",
        "safer_permitted_alternatives": "Elderberry extract, Red Beet Juice (INS 162), Lycopene (INS 160d)"
    },
    {
        "hazard_id": "HAZ-010",
        "ins_code": "INS 104",
        "eu_e_number": "E104",
        "common_name": "Quinoline Yellow",
        "scientific_chemical_name": "Disodium 2-(1,3-dioxo-2,3-dihydro-1H-inden-2-yl)quinolinedisulfonate",
        "food_applications": "Energy drinks, hard candies, fruit ice pops, confectionery toppings, cough lozenges",
        "restriction_status": "BANNED / NOT AUTHORIZED in USA and Canada; Permitted with limits in India and European Union (with warning label)",
        "primary_organ_affected": "Neurological & Dermatological Systems",
        "health_problems_faced": "Contact sensitization, dermatitis, asthma exacerbation; behavioral restlessness and loss of concentration in pediatric cohorts.",
        "toxicological_mechanism": "Sulfonated quinophthalone derivative that interferes with trace metal homeostasis and promotes systemic histamine release.",
        "governing_authority_actions": "US FDA has not approved Quinoline Yellow for ingestion. EFSA reduced ADI to 0.5 mg/kg bw/day in 2014.",
        "statutory_citation": "EFSA Journal 2014;12(4):3670; US FDA 21 CFR; FSSAI Additive Rules",
        "safer_permitted_alternatives": "Safflower extract, Riboflavin (Vitamin B2 / INS 101), Turmeric oleoresin"
    },
    {
        "hazard_id": "HAZ-011",
        "ins_code": "INS 143",
        "eu_e_number": "E143",
        "common_name": "Fast Green FCF / FD&C Green No. 3",
        "scientific_chemical_name": "Disodium 2-{[4-[ethyl(3-sulfonatobenzyl)amino]phenyl][4-[ethyl(3-sulfonatobenzyl)iminio]cyclohexa-2,5-dien-1-ylidene]methyl}-5-hydroxybenzenesulfonate",
        "food_applications": "Mint jellies, beverage syrups, sherbets, confectionery fillings, canned peas",
        "restriction_status": "BANNED / NOT AUTHORIZED in European Union; Permitted with limits in USA and India",
        "primary_organ_affected": "Cellular Integrity & Gastrointestinal Tract",
        "health_problems_faced": "Poorly absorbed in intestine; associated with sarcomas at injection sites in animal studies; potential mutagenic responses in mammalian cell systems.",
        "toxicological_mechanism": "Triphenylmethane dye capable of inducing clastogenic alterations and chromosomal aberrations under elevated physiological exposure.",
        "governing_authority_actions": "Not approved under EU Regulation (EC) 1333/2008 Annex II for food use. US FDA permits under 21 CFR 74.1203.",
        "statutory_citation": "Regulation (EC) No 1333/2008; 21 CFR 74.1203; Joint FAO/WHO JECFA Evaluation",
        "safer_permitted_alternatives": "Chlorophyllin Copper Complexes (INS 141), Spirulina Extract, Spinach powder"
    },
    {
        "hazard_id": "HAZ-012",
        "ins_code": "INS 952",
        "eu_e_number": "E952",
        "common_name": "Sodium Cyclamate",
        "scientific_chemical_name": "Sodium cyclohexylsulfamate",
        "food_applications": "Diet beverages, tabletop sweeteners, sugar-free jams, diet confectionery",
        "restriction_status": "BANNED in USA since 1969; Permitted with quantitative limits in EU, Canada, and India",
        "primary_organ_affected": "Urinary Bladder & Male Reproductive System",
        "health_problems_faced": "Banned in USA following animal bioassays indicating bladder carcinogenesis when combined with saccharin; metabolite cyclohexylamine causes testicular atrophy in rodents.",
        "toxicological_mechanism": "Intestinal microflora partially convert cyclamate to cyclohexylamine, a potent sympathomimetic amine that induces vasoconstriction and reproductive tissue degeneration.",
        "governing_authority_actions": "US FDA banned all cyclamate use in foods (34 FR 17063). WHO JECFA maintains ADI of 0-11 mg/kg bw.",
        "statutory_citation": "21 CFR 189.135 (Explicitly Prohibited); EFSA Panel on Food Additives (2016)",
        "safer_permitted_alternatives": "Steviol Glycosides (INS 960), Erythritol (INS 968), Monk Fruit Extract (Luo Han Guo)"
    },
    {
        "hazard_id": "HAZ-013",
        "ins_code": "INS 320",
        "eu_e_number": "E320",
        "common_name": "Butylated Hydroxyanisole (BHA)",
        "scientific_chemical_name": "2-tert-butyl-4-methoxyphenol and 3-tert-butyl-4-methoxyphenol mixture",
        "food_applications": "Potato chips, fried snack pellets, edible vegetable oils, chewing gums, dehydrated potato flakes",
        "restriction_status": "RESTRICTED with strict maximum thresholds globally; Listed as suspected endocrine disruptor and reasonably anticipated human carcinogen in NTP Report",
        "primary_organ_affected": "Endocrine System & Gastrointestinal Mucosa",
        "health_problems_faced": "Induces forestomach papillomas and squamous cell carcinomas in rodent bioassays; disrupts thyroid and sex steroid hormone homeostasis; potential immune system alterations.",
        "toxicological_mechanism": "Bioactivated into reactive metabolites (tert-butylhydroquinone / BQ) that uncouple oxidative phosphorylation and induce microsomal lipid peroxidation.",
        "governing_authority_actions": "US National Toxicology Program (NTP) classifies BHA as reasonably anticipated to be a human carcinogen. FSSAI and FDA limit to 200 mg/kg fat content.",
        "statutory_citation": "NTP 15th Report on Carcinogens (2021); 21 CFR 172.110; FSSAI Regulation 2.4",
        "safer_permitted_alternatives": "Mixed Tocopherols (Vitamin E / INS 306), Rosemary Extract (INS 392), Ascorbyl Palmitate (INS 304)"
    },
    {
        "hazard_id": "HAZ-014",
        "ins_code": "INS 319",
        "eu_e_number": "E319",
        "common_name": "Tertiary Butylhydroquinone (TBHQ)",
        "scientific_chemical_name": "2-(1,1-Dimethylethyl)-1,4-benzenediol",
        "food_applications": "Instant ramen noodles, frozen processed foods, packaged cooking oils, microwave popcorn",
        "restriction_status": "RESTRICTED: Maximum permissible limit of 200 mg/kg globally; Prohibited or not approved in infant foods; High dosages cytotoxic",
        "primary_organ_affected": "Immune System, Cellular DNA & Liver",
        "health_problems_faced": "Suppresses T-cell and natural killer cell immune surveillance; precursor to DNA adduct formation at supra-nutritional doses; reported neurotoxic symptoms (vision disturbance, ringing in ears) during accidental acute exposure.",
        "toxicological_mechanism": "Induces microsomal cytochrome P450 enzymes and generates semiquinone free radical intermediates that deplete cellular glutathione (GSH).",
        "governing_authority_actions": "EFSA established an ADI of 0.7 mg/kg bw/day. US FDA mandates strict 0.02% (200 ppm) total fat limitation under 21 CFR 172.185.",
        "statutory_citation": "EFSA Journal 2004, 84, 1-50; 21 CFR 172.185; FSSAI Packaging & Labelling Standards",
        "safer_permitted_alternatives": "Rosemary Extract (INS 392), Ascorbic acid (INS 300), Nitrogen flushing in packaging"
    },
    {
        "hazard_id": "HAZ-015",
        "ins_code": "ADULT-SR",
        "eu_e_number": "None",
        "common_name": "Sudan Dyes (Sudan I, II, III, IV)",
        "scientific_chemical_name": "1-(Phenylazo)-2-naphthol and related alkylated derivatives",
        "food_applications": "Illegal chemical adulterant found in unbranded red chilli powder, turmeric, curry powder, and palm oil",
        "restriction_status": "STRICTLY ILLEGAL INDUSTRIAL ADULTERANT: Prohibited in all foodstuffs worldwide (Zero Tolerance)",
        "primary_organ_affected": "Liver (Hepatic), Bladder & Genomic DNA",
        "health_problems_faced": "Classified by IARC as potent genotoxic carcinogens; induce malignant hepatic carcinomas, urinary bladder tumors, and bone marrow chromosomal breakage.",
        "toxicological_mechanism": "Hepatic azo-reduction splits the molecule into aniline and 1-amino-2-naphthol, forming reactive arylamine intermediates that covalently bind to DNA guanine bases.",
        "governing_authority_actions": "European Rapid Alert System for Food and Feed (RASFF) and FSSAI operate zero-tolerance protocols with HPLC-MS confirmation for cross-border shipments.",
        "statutory_citation": "Commission Decision 2004/92/EC; FSSAI Prohibition of Sales Regulations; IARC Monograph Vol 8",
        "safer_permitted_alternatives": "Pure Paprika Oleoresin (INS 160c), Sun-dried natural red chilli powder"
    },
    {
        "hazard_id": "HAZ-016",
        "ins_code": "ADULT-MY",
        "eu_e_number": "None",
        "common_name": "Metanil Yellow",
        "scientific_chemical_name": "Sodium 3-[4-(phenylamino)phenylazo]benzenesulfonate",
        "food_applications": "Illegal textile colour used as adulterant in split pigeon peas (turmeric dal), laddu, jalebi, biryani rice",
        "restriction_status": "STRICTLY ILLEGAL INDUSTRIAL ADULTERANT: Banned from food consumption under the Food Safety and Standards Act",
        "primary_organ_affected": "Brain (Central Nervous System), Testes & Liver",
        "health_problems_faced": "Severe depletion of brain monoamine neurotransmitters (dopamine, serotonin, noradrenaline); testicular atrophy, reduced sperm motility; acute hepatocellular necrosis.",
        "toxicological_mechanism": "Crosses the blood-brain barrier, inhibiting acetylcholinesterase activity and causing severe oxidative lipid peroxidation in prefrontal and striatal brain regions.",
        "governing_authority_actions": "FSSAI Section 16(5) proactive inspection mandates penal action under the Indian Penal Code for unauthorized industrial dyeing of food grains.",
        "statutory_citation": "FSSAI Adulteration Act Schedule I; Indian Journal of Medical Research Toxicology Reports",
        "safer_permitted_alternatives": "Pure Haldi (Curcuma longa), Saffron (Kesar), Beta-Carotene (INS 160a)"
    },
    {
        "hazard_id": "HAZ-017",
        "ins_code": "ADULT-RB",
        "eu_e_number": "None",
        "common_name": "Rhodamine B",
        "scientific_chemical_name": "N-[9-(2-carboxyphenyl)-6-(diethylamino)-3H-xanthen-3-ylidene]-N-ethylethanaminium chloride",
        "food_applications": "Illegal chemical adulterant detected in pink cotton candy (Buddhi ke Baal), roadside confectionery, sauces",
        "restriction_status": "STRICTLY ILLEGAL INDUSTRIAL ADULTERANT: Industrial fluorescent dye prohibited in all food by FSSAI and WHO",
        "primary_organ_affected": "Cellular DNA, Liver, Kidneys & Thyroid",
        "health_problems_faced": "Proven genotoxicity, chromosomal aberrations in peripheral lymphocytes; liver enlargement; acute renal toxicity; potential carcinogenic transformation in long-term exposures.",
        "toxicological_mechanism": "Intercalates directly into double-stranded DNA helical structure, disrupting DNA polymerase replication and generating superoxides.",
        "governing_authority_actions": "Multiple Indian state food authorities (Tamil Nadu, Karnataka, Delhi) issued state-wide bans and raids on street vendors using Rhodamine B in 2024.",
        "statutory_citation": "State Food Safety Directives (2024); FSSAI Section 26 Non-Permitted Dyes; WHO Food Safety Notice",
        "safer_permitted_alternatives": "Natural Beetroot Extract (INS 162), Hibiscus flower extract"
    },
    {
        "hazard_id": "HAZ-018",
        "ins_code": "ADULT-MEL",
        "eu_e_number": "None",
        "common_name": "Melamine",
        "scientific_chemical_name": "1,3,5-Triazine-2,4,6-triamine",
        "food_applications": "Illegal economic adulterant added to fluid milk and milk powder to artificially inflate protein readings (Kjeldahl nitrogen test)",
        "restriction_status": "STRICTLY ILLEGAL ADULTERANT: Worldwide zero-tolerance threshold in fluid milk; max 1 mg/kg in infant formula",
        "primary_organ_affected": "Renal System (Kidneys)",
        "health_problems_faced": "Acute nephrotoxicity, renal tubular blockage, formation of insoluble kidney stones (melamine-cyanurate complexes), acute renal failure, and pediatric mortality.",
        "toxicological_mechanism": "Complexes with endogenous uric acid and cyanuric acid in collecting renal tubules, forming dense crystalline precipitates that obstruct urine flow and cause necrosis.",
        "governing_authority_actions": "Codex Alimentarius and FSSAI established maximum limit of 1.0 mg/kg in powdered infant formula and 2.5 mg/kg in other foods to catch fraudulent spiking.",
        "statutory_citation": "Codex Standard 193-1995; FSSAI Milk and Milk Products Adulteration Guidelines",
        "safer_permitted_alternatives": "Genuine raw cow/buffalo milk protein (Casein, Whey), no nitrogenous spiking"
    },
    {
        "hazard_id": "HAZ-019",
        "ins_code": "ADULT-FORM",
        "eu_e_number": "None",
        "common_name": "Formalin / Formaldehyde",
        "scientific_chemical_name": "Aqueous solution of formaldehyde (CH2O 37%)",
        "food_applications": "Illegal chemical preservative injected into fresh fish, crustaceans, and dairy to prevent spoilage during transport",
        "restriction_status": "STRICTLY ILLEGAL INDUSTRIAL CHEMICAL: IARC Group 1 known human carcinogen, completely prohibited in food",
        "primary_organ_affected": "Gastrointestinal Tract & Respiratory Epithelium",
        "health_problems_faced": "Corrosive ulcerations of the stomach and duodenum, severe vomiting and hematemesis; nasopharyngeal carcinoma, leukemia; irreversible protein cross-linking.",
        "toxicological_mechanism": "Rapidly forms covalent methylene bridges between biological proteins and nucleic acids, inactivating essential cellular enzymes and triggering cellular apoptosis.",
        "governing_authority_actions": "FSSAI and coastal state fisheries departments deploy rapid detection test strips (CIFT-Lab) at fish harbors to confiscate formalin-treated seafood.",
        "statutory_citation": "IARC Monograph Vol 100F (2012); FSSAI Guidance on Chemicals in Fresh Fish",
        "safer_permitted_alternatives": "Cold-chain refrigerated storage (0-4°C), Slurry ice packaging"
    },
    {
        "hazard_id": "HAZ-020",
        "ins_code": "ADULT-ARG",
        "eu_e_number": "None",
        "common_name": "Argemone Oil (Sanguinarine)",
        "scientific_chemical_name": "Argemone mexicana seed oil containing sanguinarine & dihydrosanguinarine",
        "food_applications": "Illegal toxic adulterant in edible mustard oil and sesame oil",
        "restriction_status": "STRICTLY PROHIBITED TOXIC ADULTERANT: Zero tolerance under FSSAI Regulations",
        "primary_organ_affected": "Cardiovascular System (Capillaries) & Eyes",
        "health_problems_faced": "Causes Epidemic Dropsy (severe bilateral lower-limb edema, cardiac failure, dyspnea), glaucoma, optic nerve degeneration leading to permanent blindness, and hepatomegaly.",
        "toxicological_mechanism": "Sanguinarine selectively inhibits vascular membrane Na+/K+-ATPase, leading to severe capillary hyperpermeability, widespread plasma leakage, and vasodilation.",
        "governing_authority_actions": "FSSAI mandates the Nitric Acid test and TLC screening for all commercial mustard oil batches under Section 2.2.1.",
        "statutory_citation": "FSSAI Edible Oils Quality Standards Section 2.2.1; Indian Council of Medical Research (ICMR) Protocol",
        "safer_permitted_alternatives": "Cold-pressed pure kachi ghani mustard oil, verified by gas chromatography"
    }
]

def main():
    os.makedirs("dataset", exist_ok=True)
    os.makedirs("frontend/src/data", exist_ok=True)

    df = pd.DataFrame(HAZARDS_DATA)
    
    # Save CSV
    csv_path = "dataset/restricted_substances_hazards_dataset.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Saved CSV dataset to {csv_path} ({len(df)} records)")

    # Save JSON in dataset folder
    json_path = "dataset/restricted_substances_hazards_dataset.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(HAZARDS_DATA, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON dataset to {json_path}")

    # Save JSON in frontend/src/data folder for seamless React rendering
    frontend_json_path = "frontend/src/data/restricted_substances_hazards.json"
    with open(frontend_json_path, "w", encoding="utf-8") as f:
        json.dump(HAZARDS_DATA, f, indent=2, ensure_ascii=False)
    print(f"Saved frontend data to {frontend_json_path}")

if __name__ == "__main__":
    main()
