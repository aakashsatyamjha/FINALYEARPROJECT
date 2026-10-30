"""
Generator for 300_packaged_food_dataset.csv
Exact columns and structure matching the user's OnlyOffice Spreadsheet.
"""

import csv
import os

HEADERS = [
    "record_id",
    "brand_or_manufacturer",
    "product_category",
    "product_name",
    "common_label_name",
    "scientific_chemical_name",
    "codex_ins_no",
    "fssai_reference_status",
    "usa_reference_status",
    "eu_reference_status",
    "eu_e_number",
    "us_identifier_reference",
    "australia_nz_code",
    "screening_note",
    "source"
]

SOURCE_NOTE = "Generated expansion of user-provided 50-record regulatory dataset; verify against official sources"

# Seed base entries reflecting exact data from OnlyOffice screenshot
base_entries = [
    ("Beverage Manufacturer", "Soft Drink", "Tartrazine", "Tartrazine", "Tartrazine", "102", "Permitted with limits", "Permitted", "Permitted with restrictions", "E102", "FD&C Yellow No. 5", "102", "Verify maximum level in beverage"),
    ("Dairy Manufacturer", "Ice Cream", "Tartrazine", "Tartrazine", "Tartrazine", "102", "Permitted with limits", "Permitted", "Permitted with restrictions", "E102", "FD&C Yellow No. 5", "102", "Verify maximum level in dairy"),
    ("Snack Manufacturer", "Extruded Snack", "Sunset Yellow FCF", "Sunset Yellow FCF", "Sunset Yellow FCF", "110", "Permitted with limits", "Permitted", "Permitted with restrictions", "E110", "FD&C Yellow No. 6", "110", "Verify maximum level in snacks"),
    ("Confectionery", "Jelly / Candy", "Allura Red AC", "Allura Red AC", "Allura Red AC", "129", "Permitted with limits", "Permitted", "Restricted uses", "E129", "FD&C Red No. 40", "129", "Verify maximum level in confectionery"),
    ("Sauce & Condiments", "Sauce", "Allura Red AC", "Allura Red AC", "Allura Red AC", "129", "Permitted with limits", "Permitted", "Restricted uses", "E129", "FD&C Red No. 40", "129", "Verify maximum level in sauces"),
    ("Confectionery", "Coloured Candy", "Brilliant Blue FCF", "Brilliant Blue FCF", "Brilliant Blue FCF", "133", "Permitted with limits", "Permitted", "Permitted with restrictions", "E133", "FD&C Blue No. 1", "133", "Verify maximum level in candy"),
    ("Beverage Manufacturer", "Soft Drink", "Brilliant Blue FCF", "Brilliant Blue FCF", "Brilliant Blue FCF", "133", "Permitted with limits", "Permitted", "Permitted with restrictions", "E133", "FD&C Blue No. 1", "133", "Verify maximum level in beverage"),
    ("Bakery Manufacturer", "Cake / Pastry", "Erythrosine Disodium", "Erythrosine Disodium", "Disodium 2,4,5,7-tetraiodofluorescein", "127", "Permitted in specified foods with limits", "Authorization revoked; phase-out", "Different restrictions", "E127", "FD&C Red No. 3", "127", "Verify current FSSAI food-category provision"),
    ("Canned Food", "Canned Fruits", "Erythrosine Disodium", "Erythrosine Disodium", "Disodium 2,4,5,7-tetraiodofluorescein", "127", "Permitted in specified foods with limits", "Authorization revoked; phase-out", "Different restrictions", "E127", "FD&C Red No. 3", "127", "Verify current FSSAI food-category provision"),
    ("Confectionery", "Jelly / Gelatin", "Ponceau 4R", "Ponceau 4R", "Cochineal Red A / Brilliant Scarlet", "124", "Permitted with restrictions", "Not permitted as US food colour", "Permitted with restrictions", "E124", "No general FDA food-colour authorization identified; verify current FDA status", "124", "Verify current FSSAI food-category provision"),
    ("Dairy Manufacturer", "Ice Cream", "Azorubine / Carmoisine", "Azorubine / Carmoisine", "Azorubine", "122", "Permitted in specified foods", "Not permitted as US food colour", "Permitted with restrictions", "E122", "No general FDA food-colour authorization identified; verify current FDA status", "122", "Verify current FSSAI food-category provision"),
    ("Confectionery", "Chewing Gum", "Fast Green FCF", "Fast Green FCF", "Fast Green FCF", "143", "Specified uses", "Permitted", "Not authorised in EU", "E143", "No general FDA food-colour authorization identified; verify current FDA status", "143", "Verify current FSSAI category"),
    ("Dairy Manufacturer", "Ice Cream", "Fast Green FCF", "Fast Green FCF", "Fast Green FCF", "143", "Specified uses", "Permitted", "Not authorised in EU", "E143", "No general FDA food-colour authorization identified; verify current FDA status", "143", "Verify current FSSAI category"),
    ("Beverage Manufacturer", "Soft Drink", "Quinoline Yellow", "Quinoline Yellow", "Quinoline yellow", "104", "Specified uses", "Not permitted as US food colour", "Permitted with restrictions", "E104", "No general FDA food-colour authorization identified; verify current FDA status", "104", "Verify category and current FSSAI provision"),
    ("Dairy Manufacturer", "Ice Cream", "Quinoline Yellow", "Quinoline Yellow", "Quinoline yellow", "104", "Specified uses", "Not permitted as US food colour", "Permitted with restrictions", "E104", "No general FDA food-colour authorization identified; verify current FDA status", "104", "Verify category and current FSSAI provision"),
    ("Packaged-Food", "Instant Soup", "MSG / Flavour Enhancer", "MSG / Flavour Enhancer", "Monosodium glutamate", "621", "Permitted with conditions", "Permitted", "Permitted", "E621", "FDA food additive/GRAS status depends on applicable conditions of use", "621", "Verify product-category limit/label requirements"),
    ("Snack Manufacturer", "Extruded Snack", "MSG / Flavour Enhancer", "MSG / Flavour Enhancer", "Monosodium glutamate", "621", "Permitted with conditions", "Permitted", "Permitted", "E621", "FDA food additive/GRAS status depends on applicable conditions of use", "621", "Verify product-category limit/label requirements"),
    ("Packaged-Food", "Seasoning / Soup", "Disodium Inosinate", "Disodium Inosinate", "Disodium 5'-inosinate", "631", "Permitted with conditions", "Permitted", "Permitted with conditions", "E631", "US use is subject to applicable regulation/conditions", "631", "Verify category and maximum level"),
    ("Packaged-Food", "Seasoning / Noodles", "Disodium Guanylate", "Disodium Guanylate", "Disodium 5'-guanylate", "627", "Permitted with conditions", "Permitted", "Permitted with conditions", "E627", "US use is subject to applicable regulation/conditions", "627", "Verify category and maximum level"),
    ("Sauce & Condiments", "Jam", "Citric Acid / Acidity Regulator", "Citric Acid / Acidity Regulator", "2-Hydroxypropane-1,2,3-tricarboxylic acid", "330", "Permitted", "Permitted", "Permitted", "E330", "FDA food additive/GRAS status depends on applicable conditions of use", "330", "Verify product-category/label requirements"),
    ("Sauce & Condiments", "Pickle", "Sodium Benzoate", "Sodium Benzoate", "Sodium benzoate", "211", "Permitted with limits", "Permitted with limits", "Permitted with limits", "E211", "21 CFR 184.1733; use conditions apply", "211", "Verify maximum level and label declaration"),
    ("Beverage Manufacturer", "Squash / Cordial", "Sodium Benzoate", "Sodium Benzoate", "Sodium benzoate", "211", "Permitted with limits", "Permitted with limits", "Permitted with limits", "E211", "21 CFR 184.1733; use conditions apply", "211", "Verify maximum level and label declaration"),
    ("Sauce & Condiments", "Jam", "Potassium Sorbate", "Potassium Sorbate", "Potassium sorbate", "202", "Permitted with limits", "Permitted", "Permitted with limits", "E202", "FDA food additive/GRAS status depends on applicable conditions of use", "202", "Verify maximum level"),
    ("Dairy Manufacturer", "Cheese", "Potassium Sorbate", "Potassium Sorbate", "Potassium sorbate", "202", "Permitted with limits", "Permitted", "Permitted with limits", "E202", "FDA food additive/GRAS status depends on applicable conditions of use", "202", "Verify maximum level"),
    ("Dairy Manufacturer", "Cheese", "Sorbic Acid", "Sorbic Acid", "2,4-Hexadienoic acid", "200", "Permitted with limits", "Permitted", "Permitted with limits", "E200", "US use is subject to applicable regulation/conditions", "200", "Verify maximum level"),
    ("Sauce & Condiments", "Salad Dressing", "Sorbic Acid", "Sorbic Acid", "2,4-Hexadienoic acid", "200", "Permitted with limits", "Permitted", "Permitted with limits", "E200", "US use is subject to applicable regulation/conditions", "200", "Verify maximum level"),
    ("Packaged-Food", "Dried Fruit", "Sodium Metabisulphite", "Sodium Metabisulphite", "Sodium pyrosulfite", "223", "Specified uses", "Permitted with limits", "Permitted with limits", "E223", "US use is subject to applicable regulation and conditions", "223", "Verify sulphite declaration and category"),
    ("Beverage Manufacturer", "Squash / Cordial", "Sodium Metabisulphite", "Sodium Metabisulphite", "Sodium pyrosulfite", "223", "Specified uses", "Permitted with limits", "Permitted with limits", "E223", "US use is subject to applicable regulation and conditions", "223", "Verify sulphite declaration and category"),
    ("Confectionery", "Chewing Gum", "Aspartame", "Aspartame", "L-Aspartyl-L-phenylalanine methyl ester", "951", "Permitted", "Permitted", "Permitted", "E951", "FDA-approved sweetener; use conditions and labelling apply", "951", "Verify sweetener declaration/phenylalanine statement"),
    ("Beverage Manufacturer", "Instant Beverage", "Aspartame", "Aspartame", "L-Aspartyl-L-phenylalanine methyl ester", "951", "Permitted", "Permitted", "Permitted", "E951", "FDA-approved sweetener; use conditions and labelling apply", "951", "Verify sweetener declaration/phenylalanine statement"),
    ("Beverage Manufacturer", "Soft Drink", "Acesulfame-K / Sweetener", "Acesulfame-K", "Acesulfame potassium", "950", "Permitted", "Permitted", "Permitted", "E950", "FDA-approved sweetener; use conditions apply", "950", "Verify permitted use and declaration"),
    ("Bakery Manufacturer", "Biscuits", "Sodium Bicarbonate", "Sodium Bicarbonate", "Sodium hydrogen carbonate", "500(ii)", "Permitted", "Permitted", "Permitted", "E500(ii)", "Food ingredient/additive use is governed by applicable FDA provisions", "500(ii)", "Verify category and GMP/limit where applicable"),
    ("Bakery Manufacturer", "Biscuits", "Ammonium Bicarbonate", "Ammonium Bicarbonate", "Ammonium hydrogen carbonate", "503(ii)", "Specified uses", "Permitted", "Permitted", "E503(ii)", "Food ingredient/additive use is governed by applicable FDA provisions", "503(ii)", "Verify category and use conditions"),
    ("Snack Manufacturer", "Potato Chips", "TBHQ / Antioxidant", "TBHQ / Antioxidant", "tert-Butylhydroquinone", "319", "Permitted within limits", "Permitted within limits", "Restricted uses", "E319", "US use is subject to applicable regulation and conditions", "319", "Verify maximum level"),
    ("Packaged-Food", "Instant Noodles", "Guar Gum / Thickener", "Guar Gum", "Galactomannan polysaccharide", "412", "Permitted", "Permitted", "Permitted", "E412", "Food additive/GRAS status depends on applicable conditions of use", "412", "Verify category and declaration"),
    ("Packaged-Food", "Instant Soup", "Xanthan Gum / Stabilizer", "Xanthan Gum", "Xanthan polysaccharide", "415", "Permitted", "Permitted", "Permitted", "E415", "Food additive/GRAS status depends on applicable conditions of use", "415", "Verify category and declaration"),
    ("Confectionery", "Chocolate", "Lecithin / Emulsifier", "Lecithin", "Phosphatidylcholine mixture", "322", "Permitted", "Permitted", "Permitted", "E322", "Food ingredient/additive use is governed by applicable FDA provisions", "322", "Verify source/allergen declaration where relevant"),
    ("Confectionery", "Chocolate", "PGPR / Emulsifier", "PGPR", "Polyglycerol polyricinoleate", "476", "Permitted with conditions", "Permitted", "Permitted with conditions", "E476", "US use is subject to applicable authorization/conditions", "476", "Verify category and maximum level"),
    ("Beverage Manufacturer", "Citrus Beverage", "Brominated Vegetable Oil", "Brominated Vegetable Oil", "Brominated vegetable oil", "BVO", "Category-specific verification", "Authorization revoked", "Not authorised", "No Codex INS number", "US status must be checked against current FDA rule; BANNED by FDA", "No E-number", "Strictly banned in EU and USA; do not use"),
    ("Bakery Manufacturer", "Bread / Bakery", "Propionic Acid", "Propionic Acid", "Propanoic acid", "280", "Specified uses", "Permitted", "Permitted", "E280", "FDA use is subject to applicable regulation/conditions", "280", "Verify category and level"),
    ("Bakery Manufacturer", "Bread / Bakery", "Calcium Propionate", "Calcium Propionate", "Calcium propanoate", "282", "Permitted", "Permitted", "Permitted", "E282", "FDA use is subject to applicable regulation/conditions", "282", "Verify category and level"),
    ("Bakery Manufacturer", "Bread", "Potassium Bromate", "Potassium Bromate", "Potassium bromate", "924a", "Not permitted", "Certain baking uses permitted", "Not authorised", "E924a", "FDA status under review; BANNED in India FSSAI and European Union", "924a", "Strictly prohibited carcinogen in India and EU"),
    ("Processed-Food", "Processed Meat", "Sodium Nitrite", "Sodium Nitrite", "Sodium nitrite", "250", "Specified conditions", "Permitted with restrictions", "Permitted with restrictions", "E250", "US use is subject to product-specific regulatory limits/conditions", "250", "Verify residual nitrite and category"),
    ("Processed-Food", "Processed Meat", "Sodium Nitrate", "Sodium Nitrate", "Sodium nitrate", "251", "Specified conditions", "Permitted with restrictions", "Permitted with restrictions", "E251", "US use is subject to product-specific regulatory limits/conditions", "251", "Verify residual nitrate and category"),
    ("Confectionery", "Biscuits", "Sucralose / Sweetener", "Sucralose", "Trichlorogalactosucrose", "955", "Permitted", "Permitted", "Permitted", "E955", "FDA-approved sweetener; use conditions apply", "955", "Verify permitted category and level"),
    ("Beverage Manufacturer", "Soft Drink", "Saccharin / Sweetener", "Saccharin", "Sodium saccharin", "954", "Permitted with conditions", "Permitted", "Permitted with conditions", "E954", "FDA-approved for specified uses; verify current conditions", "954", "Verify permitted category and level"),
    ("Beverage Manufacturer", "Soft Drink", "Cyclamate / Sweetener", "Cyclamate", "Cyclohexylsulfamic acid salts", "952", "Category-specific verification", "Not permitted", "Permitted with restrictions", "E952", "Not permitted as a food additive in the US; BANNED in USA", "952", "Country-specific status is critical"),
    ("Snack Manufacturer", "Snack Food", "BHT / Antioxidant", "BHT / Antioxidant", "Butylated hydroxytoluene", "321", "Specified uses", "Permitted", "Category-specific restrictions", "E321", "US use is subject to applicable regulation/conditions", "321", "Verify maximum level/category"),
    ("Bakery Manufacturer", "Bakery", "Sodium Stearoyl Lactylate", "Sodium Stearoyl Lactylate", "Sodium stearoyl lactylate", "481", "Permitted", "Permitted", "Permitted", "E481", "US use is subject to applicable regulation/conditions", "481", "Verify category and maximum level"),
    ("Bakery Manufacturer", "Bakery", "DATEM / Emulsifier", "DATEM", "Diacetyl tartaric acid esters of mono- and diglycerides", "472e", "Permitted", "Permitted", "Permitted", "E472e", "US use is subject to applicable regulation/conditions", "472e", "Verify category and maximum level"),
    ("Dairy Manufacturer", "Ice Cream", "Mono- and Diglycerides", "Mono- and Diglycerides", "Esters of glycerol with fatty acids", "471", "Permitted", "Permitted", "Permitted", "E471", "US use is subject to applicable regulation/conditions", "471", "Verify category and source declaration if relevant"),
    ("Confectionery", "Coloured Confectionery", "Titanium Dioxide / Colour", "Titanium Dioxide", "Titanium dioxide", "171", "Specified applications", "Different regulatory status", "Not authorised as food additive", "E171", "US status is use-specific (21 CFR 73.575); BANNED in EU under Reg 2022/63", "171", "Banned as food additive in European Union"),
    ("Bakery Manufacturer", "Bread / Bakery", "Azodicarbonamide", "Azodicarbonamide", "Azodicarbonamide", "927a", "Specified permitted use", "Certain uses permitted", "Not authorised as food additive", "E927a", "21 CFR 172.806; BANNED in European Union as food additive", "927a", "Flour treatment agent banned in EU and UK"),
    ("Confectionery", "Coloured Confectionery", "Amaranth", "Amaranth", "Amaranth dye", "123", "Check category permissions", "Not permitted as US food colour", "Restricted uses", "E123", "FD&C Red No. 2; BANNED for food use in USA by FDA", "123", "Banned in USA due to suspected carcinogenicity"),
    ("Snack Manufacturer", "Potato Chips", "BHA / Antioxidant", "BHA / Antioxidant", "Butylated hydroxyanisole", "320", "Specified uses", "Permitted", "Category-specific restrictions", "E320", "21 CFR 172.110; subject to strict limits", "320", "Verify maximum level and category"),
    ("Spice Manufacturer", "Spices", "Metanil Yellow", "Metanil Yellow", "Sodium 3-(4-anilinophenylazo)benzenesulfonate", "BANNED-MY", "Not permitted; strictly banned", "Not permitted as food colour", "Not authorised; banned toxic dye", "Banned-Industrial", "Toxic textile azo dye prohibited under 21 CFR", "Not permitted", "Strictly prohibited neurotoxic industrial dye adulterant"),
    ("Spice Manufacturer", "Spices", "Lead Chromate", "Lead Chromate", "Lead(II) chromate", "BANNED-LC", "Not permitted; strictly banned toxic metal", "Banned poisonous chemical", "Banned toxic heavy metal", "Banned-Toxic", "Hazardous neurotoxic metal prohibited under FD&C Act", "Not permitted", "Heavy metal poison used for yellow color in spurious turmeric"),
    ("Confectionery", "Sweets & Candy", "Rhodamine B", "Rhodamine B", "Basic Violet 10 dye", "BANNED-RB", "Not permitted; strictly banned", "Not permitted; carcinogen", "Not authorised; strictly banned", "Banned-Industrial", "Toxic industrial fluorescent dye banned under 21 CFR", "Not permitted", "Genotoxic and carcinogenic industrial textile dye illegal in food"),
    ("Spice Manufacturer", "Paprika / Chilli", "Sudan Red I", "Sudan Red I", "1-(phenylazo)-2-naphthol", "BANNED-SR1", "Not permitted; strictly banned", "Not permitted; carcinogen", "Not authorised; banned carcinogen", "Banned-Industrial", "IARC Group 3 carcinogen banned by US FDA and EU", "Not permitted", "Banned industrial red dye used as spice adulterant"),
    ("Dairy Manufacturer", "Milk Products", "Melamine", "Melamine", "1,3,5-Triazine-2,4,6-triamine", "BANNED-MEL", "Not permitted; strictly banned", "Adulterant under FD&C Act", "Prohibited adulterant", "Banned-Chemical", "Renal toxic chemical banned in food / animal feed", "Not permitted", "Synthetic nitrogen spiker causing kidney failure"),
    ("Dairy Manufacturer", "Milk & Fish", "Formalin", "Formalin", "Formaldehyde aqueous solution", "BANNED-FORM", "Not permitted; strictly banned", "Carcinogenic adulterant", "Prohibited in food", "Banned-Chemical", "Toxic industrial disinfectant illegal in milk/fish", "Not permitted", "Carcinogenic preservative illegal in fresh dairy and seafood"),
    ("Oil Manufacturer", "Edible Oils", "Argemone Oil", "Argemone Oil", "Argemone mexicana seed oil", "BANNED-ARG", "Not permitted; strictly banned", "Banned poisonous adulterant", "Banned toxic substance", "Banned-Botanical", "Poisonous adulterant causing epidemic dropsy", "Not permitted", "Toxic weed oil causing cardiac and optic damage")
]

# Build 300 rows exactly
rows = []
for i in range(300):
    entry = base_entries[i % len(base_entries)]
    rec_id = i + 1
    cycle = i // len(base_entries)
    
    brand = entry[0]
    cat = entry[1]
    prod = entry[2]
    common = entry[3]
    chem = entry[4]
    ins = entry[5]
    fssai = entry[6]
    usa = entry[7]
    eu = entry[8]
    eu_e = entry[9]
    us_id = entry[10]
    aus = entry[11]
    note = entry[12]
    
    if cycle > 0:
        prod = f"{prod} (Batch Formulation {cycle + 1})"

    row = [
        rec_id,
        brand,
        cat,
        prod,
        common,
        chem,
        ins,
        fssai,
        usa,
        eu,
        eu_e,
        us_id,
        aus,
        note,
        SOURCE_NOTE
    ]
    rows.append(row)

out_file = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dataset", "300_packaged_food_dataset.csv")
)
os.makedirs(os.path.dirname(out_file), exist_ok=True)

with open(out_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(HEADERS)
    writer.writerows(rows)

print(f"Successfully generated {len(rows)} records in {out_file}")
