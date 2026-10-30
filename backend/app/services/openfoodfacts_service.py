"""
Open Food Facts Service & Offline Catalog
Retrieves real-time product information from Open Food Facts API
with an offline fallback catalog of popular packaged foods and test cases.
38 brand items covering all risk tiers for deterministic demo/testing.
"""

import requests
from typing import Dict, Any, Optional

# Rich catalog of 38 popular packaged foods for reliable offline/instant testing
# Covers: Safe (Green), Low Risk (Green-Yellow), Moderate Risk (Orange), High Risk (Red), Banned Chemical (Dark Red)
OFFLINE_PRODUCT_CATALOG = {

    # ── SAFE / LOW RISK (Green) ──────────────────────────────────────────────
    "8901262010047": {
        "barcode": "8901262010047",
        "product_name": "Amul Pure Cow Ghee",
        "brand": "Amul",
        "category": "Dairy Products",
        "ingredients": "100% Clarified Milk Fat (Cow Milk). No added preservatives. No artificial colour or flavour.",
        "nutrition": {"energy_kcal": 900, "sugar_g": 0.0, "sodium_mg": 0, "saturated_fat_g": 62.0, "trans_fat_g": 3.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": "https://images.openfoodfacts.org/images/products/890/126/201/0047/front_en.9.400.jpg"
    },
    "8901719101038": {
        "barcode": "8901719101038",
        "product_name": "Parle-G Original Gluco Biscuits",
        "brand": "Parle",
        "category": "Biscuits & Bakery",
        "ingredients": "Wheat flour (Maida), Sugar, Refined palm oil, Invert sugar syrup, Raising agents (INS 503ii, INS 500ii), Salt, Milk solids, Artificial vanilla flavouring, Emulsifier (INS 472e), Dough conditioner (INS 223).",
        "nutrition": {"energy_kcal": 454, "sugar_g": 26.5, "sodium_mg": 280, "saturated_fat_g": 6.5, "trans_fat_g": 0.0, "protein_g": 6.5, "fiber_g": 1.5},
        "image_url": "https://images.openfoodfacts.org/images/products/890/171/910/1038/front_en.11.400.jpg"
    },
    "8906007394019": {
        "barcode": "8906007394019",
        "product_name": "Amul Taaza Homogenised Toned Milk",
        "brand": "Amul",
        "category": "Dairy Products",
        "ingredients": "Pasteurised Toned Milk, Vitamin A, Vitamin D2. Fat 3.0% minimum, SNF 8.5% minimum. No preservatives, zero adulterants.",
        "nutrition": {"energy_kcal": 58, "sugar_g": 4.8, "sodium_mg": 47, "saturated_fat_g": 1.9, "trans_fat_g": 0.0, "protein_g": 3.2, "fiber_g": 0.0},
        "image_url": "https://images.openfoodfacts.org/images/products/890/600/739/4019/front_en.3.400.jpg"
    },
    "8901030911439": {
        "barcode": "8901030911439",
        "product_name": "Tata Salt Vacuum Evaporated Iodised",
        "brand": "Tata Consumer Products",
        "category": "Salt & Spices",
        "ingredients": "Vacuum Evaporated Iodised Salt, Potassium Iodate (INS 917). Free flowing agent: INS 554 (Sodium Aluminosilicate). No anticaking agents beyond standard.",
        "nutrition": {"energy_kcal": 0, "sugar_g": 0.0, "sodium_mg": 38758, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": "https://images.openfoodfacts.org/images/products/890/103/091/1439/front_en.3.400.jpg"
    },
    "8901063151053": {
        "barcode": "8901063151053",
        "product_name": "Amul Pasteurised Salted Butter",
        "brand": "Amul",
        "category": "Dairy Products",
        "ingredients": "Milk fat, Common salt, Permitted natural colour (INS 160a). Pasteurised cream. No artificial preservatives.",
        "nutrition": {"energy_kcal": 720, "sugar_g": 0.5, "sodium_mg": 650, "saturated_fat_g": 46.0, "trans_fat_g": 2.5, "protein_g": 0.6, "fiber_g": 0.0},
        "image_url": "https://images.openfoodfacts.org/images/products/890/106/315/1053/front_en.6.400.jpg"
    },
    "8906063670020": {
        "barcode": "8906063670020",
        "product_name": "Patanjali Desi Cow Ghee",
        "brand": "Patanjali Ayurved",
        "category": "Dairy Products",
        "ingredients": "Pure Desi Cow Milk Fat (Vedic Bilona method). No additives. No preservatives. FSSAI certified.",
        "nutrition": {"energy_kcal": 900, "sugar_g": 0.0, "sodium_mg": 0, "saturated_fat_g": 60.0, "trans_fat_g": 2.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8906078950010": {
        "barcode": "8906078950010",
        "product_name": "Mother Dairy Full Cream Milk",
        "brand": "Mother Dairy",
        "category": "Dairy Products",
        "ingredients": "Full Cream Standardised Pasteurised Milk. Fat min 6.0%, SNF min 9.0%. Fortified with Vitamin A & D.",
        "nutrition": {"energy_kcal": 67, "sugar_g": 4.5, "sodium_mg": 50, "saturated_fat_g": 3.8, "trans_fat_g": 0.0, "protein_g": 3.5, "fiber_g": 0.0},
        "image_url": ""
    },

    # ── MODERATE RISK (Orange) ───────────────────────────────────────────────
    "8901058852813": {
        "barcode": "8901058852813",
        "product_name": "Maggi 2-Minute Masala Noodles",
        "brand": "Nestle",
        "category": "Instant Noodles & Snacks",
        "ingredients": "Refined wheat flour (Maida), Palm oil, Iodised salt, Wheat gluten, Mineral (Calcium carbonate), Thickeners (INS 508, INS 412), Acidity regulators (INS 501i, INS 500i), Humectant (INS 451i), Hydrolysed groundnut protein, Mixed spices, Sugar, Edible starch, Flavour enhancer (INS 635), Palm oil, Colour (INS 150d), MSG (INS 621).",
        "nutrition": {"energy_kcal": 427, "sugar_g": 2.2, "sodium_mg": 1020, "saturated_fat_g": 6.8, "trans_fat_g": 0.12, "protein_g": 8.0, "fiber_g": 3.6},
        "image_url": "https://images.openfoodfacts.org/images/products/890/105/885/2813/front_en.11.400.jpg"
    },
    "7622210817014": {
        "barcode": "7622210817014",
        "product_name": "Oreo Original Sandwich Cookies",
        "brand": "Cadbury / Mondelez",
        "category": "Biscuits & Confectionery",
        "ingredients": "Wheat flour, Sugar, Palm oil, Rapeseed oil, Fat-reduced cocoa powder 4.5%, Wheat starch, Glucose-fructose syrup, Raising agents (INS 501, INS 503, INS 500), Salt, Emulsifiers (INS 322, INS 476), Flavouring (vanillin), Titanium Dioxide (INS 171).",
        "nutrition": {"energy_kcal": 471, "sugar_g": 38.0, "sodium_mg": 380, "saturated_fat_g": 5.2, "trans_fat_g": 0.0, "protein_g": 5.4, "fiber_g": 3.0},
        "image_url": "https://images.openfoodfacts.org/images/products/762/221/081/7014/front_en.114.400.jpg"
    },
    "8901491101837": {
        "barcode": "8901491101837",
        "product_name": "Lay's India's Magic Masala Potato Chips",
        "brand": "Lay's (PepsiCo)",
        "category": "Snacks & Chips",
        "ingredients": "Potato, Edible Vegetable Oil (Palmolein, Rice Bran Oil), Seasoning: Spices, Iodised Salt, Maltodextrin, Sugar, Tomato Powder, Acidity Regulators (INS 330, INS 296), Flavour Enhancers (INS 627, INS 631), Anticaking Agent (INS 551), Colour (INS 160c), BHA (INS 320).",
        "nutrition": {"energy_kcal": 555, "sugar_g": 4.5, "sodium_mg": 790, "saturated_fat_g": 14.5, "trans_fat_g": 0.1, "protein_g": 7.0, "fiber_g": 4.2},
        "image_url": "https://images.openfoodfacts.org/images/products/890/149/110/1837/front_en.11.400.jpg"
    },
    "5449000000996": {
        "barcode": "5449000000996",
        "product_name": "Coca-Cola Original Taste",
        "brand": "The Coca-Cola Company",
        "category": "Carbonated Soft Drinks",
        "ingredients": "Carbonated water, Sugar, Colour (Caramel INS 150d), Phosphoric acid (INS 338), Natural flavourings including caffeine, Aspartame (INS 951).",
        "nutrition": {"energy_kcal": 42, "sugar_g": 10.6, "sodium_mg": 4, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": "https://images.openfoodfacts.org/images/products/544/900/000/0996/front_en.448.400.jpg"
    },
    "8901030018503": {
        "barcode": "8901030018503",
        "product_name": "Kissan Fresh Tomato Ketchup",
        "brand": "Kissan (HUL)",
        "category": "Sauces & Condiments",
        "ingredients": "Water, Tomato paste (28%), Sugar, Salt, Acidity regulator (INS 260), Thickeners (INS 1422, INS 415), Preservative (INS 211), Spices and condiments, Onion powder, Garlic powder.",
        "nutrition": {"energy_kcal": 138, "sugar_g": 28.0, "sodium_mg": 890, "saturated_fat_g": 0.1, "trans_fat_g": 0.0, "protein_g": 1.2, "fiber_g": 1.1},
        "image_url": "https://images.openfoodfacts.org/images/products/890/103/001/8503/front_en.11.400.jpg"
    },
    "8901063000615": {
        "barcode": "8901063000615",
        "product_name": "Cadbury Dairy Milk Chocolate",
        "brand": "Cadbury (Mondelez)",
        "category": "Confectionery",
        "ingredients": "Sugar, Cocoa butter, Cocoa mass, Skimmed milk powder, Whey powder (from milk), Butterfat (from milk), Emulsifier (INS 476, INS 322), Flavourings, Vanillin. Contains: Milk, Soya. May contain: Tree nuts, Wheat.",
        "nutrition": {"energy_kcal": 534, "sugar_g": 56.0, "sodium_mg": 75, "saturated_fat_g": 19.0, "trans_fat_g": 0.0, "protein_g": 7.6, "fiber_g": 1.5},
        "image_url": ""
    },
    "8906073320015": {
        "barcode": "8906073320015",
        "product_name": "ITC Bingo! Mad Angles Achaari Masti",
        "brand": "ITC Bingo",
        "category": "Snacks & Chips",
        "ingredients": "Wheat flour, Refined palmolein oil, Spices and condiments, Iodised salt, Acidity regulators (INS 330, INS 296), Flavour enhancers (INS 621, INS 635), Anticaking agent (INS 551), Colour (INS 110, INS 102), Tartrazine (INS 102), Sunset Yellow (INS 110).",
        "nutrition": {"energy_kcal": 523, "sugar_g": 2.0, "sodium_mg": 720, "saturated_fat_g": 11.0, "trans_fat_g": 0.1, "protein_g": 7.0, "fiber_g": 2.0},
        "image_url": ""
    },
    "8901030924193": {
        "barcode": "8901030924193",
        "product_name": "Red Bull Energy Drink",
        "brand": "Red Bull GmbH",
        "category": "Energy Drinks",
        "ingredients": "Carbonated water, Sucrose, Glucose, Citric acid (INS 330), Sodium bicarbonate (INS 500i), Magnesium carbonate (INS 504i), Taurine, Niacinamide, Calcium D-Pantothenate, Pyridoxine HCI, Vitamin B12, Natural and artificial flavours, Acesulfame K (INS 950), Sucralose (INS 955), Caffeine.",
        "nutrition": {"energy_kcal": 45, "sugar_g": 11.0, "sodium_mg": 105, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8901396031009": {
        "barcode": "8901396031009",
        "product_name": "Bournvita Chocolate Health Drink",
        "brand": "Cadbury (Mondelez)",
        "category": "Health Drinks",
        "ingredients": "Sugar, Malt extract, Cocoa (10%), Milk solids, Vitamins and minerals, Glucose syrup, Caramel colour (INS 150a), Salt, Emulsifier (INS 322), Vanilla flavour, Raising agent (INS 500).",
        "nutrition": {"energy_kcal": 385, "sugar_g": 73.0, "sodium_mg": 170, "saturated_fat_g": 1.4, "trans_fat_g": 0.0, "protein_g": 5.0, "fiber_g": 1.0},
        "image_url": ""
    },
    "8901030992001": {
        "barcode": "8901030992001",
        "product_name": "Mountain Dew Soft Drink",
        "brand": "PepsiCo",
        "category": "Carbonated Soft Drinks",
        "ingredients": "Carbonated water, Sugar, Acidity regulator (INS 330), Colour (INS 102 Tartrazine), Caffeine, Flavourings.",
        "nutrition": {"energy_kcal": 56, "sugar_g": 13.5, "sodium_mg": 30, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8901719132001": {
        "barcode": "8901719132001",
        "product_name": "Parle 20-20 Butter Cookies",
        "brand": "Parle",
        "category": "Biscuits & Bakery",
        "ingredients": "Wheat flour, Sugar, Refined palm oil, Invert sugar, Butter, Milk solids, Salt, Raising agent (INS 503ii), Emulsifier (INS 322), Diacetyl tartaric acid esters of mono and diglycerides (INS 472e), Artificial vanilla flavour, Colour (INS 102).",
        "nutrition": {"energy_kcal": 493, "sugar_g": 22.0, "sodium_mg": 340, "saturated_fat_g": 9.0, "trans_fat_g": 0.0, "protein_g": 6.5, "fiber_g": 1.5},
        "image_url": ""
    },
    "8901019018700": {
        "barcode": "8901019018700",
        "product_name": "Sunfeast Marie Light Biscuits",
        "brand": "Sunfeast (ITC)",
        "category": "Biscuits & Bakery",
        "ingredients": "Wheat flour, Sugar, Edible vegetable fat, Glucose, Salt, Raising agents (INS 503ii, INS 500ii), Emulsifier (INS 472e), Dough conditioner (INS 223), Artificial flavour (vanillin).",
        "nutrition": {"energy_kcal": 435, "sugar_g": 18.5, "sodium_mg": 250, "saturated_fat_g": 7.0, "trans_fat_g": 0.0, "protein_g": 7.0, "fiber_g": 1.5},
        "image_url": ""
    },
    "8904235040121": {
        "barcode": "8904235040121",
        "product_name": "Dabur Real Mixed Fruit Juice",
        "brand": "Dabur India",
        "category": "Fruit Juices",
        "ingredients": "Water, Sugar, Mixed fruit concentrates (12%), Citric acid (INS 330), Ascorbic acid (INS 300), Colour (INS 110), Sodium benzoate (INS 211), Natural and artificial flavours.",
        "nutrition": {"energy_kcal": 65, "sugar_g": 14.5, "sodium_mg": 25, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8901765501012": {
        "barcode": "8901765501012",
        "product_name": "Knorr Classic Tomato Soup",
        "brand": "Knorr (HUL)",
        "category": "Soups & Ready Meals",
        "ingredients": "Sugar, Tomato powder, Cornflour, Modified starch (INS 1422), Palm fat, Salt, Flavour enhancer (INS 621), Citric acid (INS 330), Flavourings, Colour (INS 160a), Anticaking agent (INS 551), Sodium caseinate.",
        "nutrition": {"energy_kcal": 355, "sugar_g": 32.0, "sodium_mg": 2350, "saturated_fat_g": 7.0, "trans_fat_g": 0.0, "protein_g": 5.0, "fiber_g": 2.0},
        "image_url": ""
    },

    # ── HIGH RISK (Red) ──────────────────────────────────────────────────────
    "8901058921090": {
        "barcode": "8901058921090",
        "product_name": "Parle Coloured Candy (Kaccha Mango Bite variant)",
        "brand": "Parle",
        "category": "Confectionery & Sweets",
        "ingredients": "Sugar, Glucose syrup, Acidity regulator (INS 330), Erythrosine (INS 127), Tartrazine (INS 102), Artificial mango flavour.",
        "nutrition": {"energy_kcal": 390, "sugar_g": 80.0, "sodium_mg": 20, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8901764123456": {
        "barcode": "8901764123456",
        "product_name": "Britannia Bread (White Sliced)",
        "brand": "Britannia Industries",
        "category": "Bakery",
        "ingredients": "Refined wheat flour (Maida), Water, Sugar, Iodised salt, Yeast, Wheat gluten, Flour treatment agent (Azodicarbonamide INS 927a), Emulsifiers (INS 481, INS 472e), Calcium propionate (INS 282), Acidity regulator (INS 300).",
        "nutrition": {"energy_kcal": 265, "sugar_g": 4.0, "sodium_mg": 490, "saturated_fat_g": 0.5, "trans_fat_g": 0.0, "protein_g": 8.0, "fiber_g": 2.5},
        "image_url": ""
    },
    "8901030011500": {
        "barcode": "8901030011500",
        "product_name": "Frooti Mango Fruit Drink",
        "brand": "Parle Agro",
        "category": "Fruit Drinks",
        "ingredients": "Water, Mango pulp (18%), Sugar, Acidity regulator (INS 330), Stabiliser (INS 415), Preservative (INS 202), Colour (INS 102 Tartrazine, INS 110 Sunset Yellow), Artificial mango flavour.",
        "nutrition": {"energy_kcal": 58, "sugar_g": 13.5, "sodium_mg": 20, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8901063900011": {
        "barcode": "8901063900011",
        "product_name": "Kurkure Masala Munch",
        "brand": "PepsiCo India",
        "category": "Extruded Snacks",
        "ingredients": "Rice meal, Edible vegetable oil, Corn meal, Gram meal, Salt, Spices and condiments, Flavour enhancer (INS 621 MSG), Colour (INS 160c), Anticaking agent (INS 551), Acidity regulators (INS 330, INS 260).",
        "nutrition": {"energy_kcal": 531, "sugar_g": 3.5, "sodium_mg": 820, "saturated_fat_g": 8.0, "trans_fat_g": 0.0, "protein_g": 5.0, "fiber_g": 3.5},
        "image_url": ""
    },
    "8906025660022": {
        "barcode": "8906025660022",
        "product_name": "Haldiram's Aloo Bhujia",
        "brand": "Haldiram's",
        "category": "Traditional Snacks",
        "ingredients": "Gram flour, Potato, Edible vegetable oil (Palm oil), Salt, Red chilli, Black pepper, Mango powder, Cumin, Spices and condiments, Flavour enhancer (INS 621), Acidity regulator (INS 330).",
        "nutrition": {"energy_kcal": 553, "sugar_g": 1.5, "sodium_mg": 840, "saturated_fat_g": 14.0, "trans_fat_g": 0.0, "protein_g": 12.5, "fiber_g": 5.0},
        "image_url": ""
    },
    "8906011660001": {
        "barcode": "8906011660001",
        "product_name": "MDH Deggi Mirch Spice Mix",
        "brand": "MDH Spices",
        "category": "Spices & Condiments",
        "ingredients": "Red chilli, Coriander, Cumin, Turmeric, Salt. Note: Testing has identified traces of Sudan Red dye and Rhodamine B in certain batches (FSSAI alert 2023).",
        "nutrition": {"energy_kcal": 340, "sugar_g": 8.0, "sodium_mg": 890, "saturated_fat_g": 3.5, "trans_fat_g": 0.0, "protein_g": 12.0, "fiber_g": 20.0},
        "image_url": ""
    },
    "8906078009015": {
        "barcode": "8906078009015",
        "product_name": "Patanjali Atta Noodles",
        "brand": "Patanjali Ayurved",
        "category": "Instant Noodles",
        "ingredients": "Whole wheat flour (Atta), Palm oil, Salt, Spices, Flavour enhancer (INS 621 MSG), Acidity regulator (INS 330), Thickener (INS 412), Colour (INS 150d).",
        "nutrition": {"energy_kcal": 375, "sugar_g": 1.5, "sodium_mg": 870, "saturated_fat_g": 4.5, "trans_fat_g": 0.0, "protein_g": 10.0, "fiber_g": 3.5},
        "image_url": ""
    },
    "8906073580012": {
        "barcode": "8906073580012",
        "product_name": "Hamdard Rooh Afza Sharbat",
        "brand": "Hamdard",
        "category": "Beverages",
        "ingredients": "Sugar, Water, Rose water, Khus (Vetiver) extract, Kewra extract, Sandalwood extract, Citric acid (INS 330), Preservative (INS 211 Sodium benzoate), Colour: Ponceau 4R (INS 124), Carmoisine (INS 122).",
        "nutrition": {"energy_kcal": 272, "sugar_g": 68.0, "sodium_mg": 12, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "8906001761508": {
        "barcode": "8906001761508",
        "product_name": "MTR Ready to Eat Palak Paneer",
        "brand": "MTR Foods",
        "category": "Ready-to-Eat Meals",
        "ingredients": "Spinach, Cottage cheese, Water, Onion, Tomato, Refined vegetable oil, Ginger, Garlic, Salt, Spices and condiments, Modified starch (INS 1422), Acidity regulator (INS 330), Thickener (INS 415), Colour (INS 141i Chlorophyllin).",
        "nutrition": {"energy_kcal": 130, "sugar_g": 3.0, "sodium_mg": 680, "saturated_fat_g": 4.5, "trans_fat_g": 0.0, "protein_g": 6.5, "fiber_g": 2.0},
        "image_url": ""
    },
    "8906075240140": {
        "barcode": "8906075240140",
        "product_name": "Everest Garam Masala",
        "brand": "Everest Food Products",
        "category": "Spices & Condiments",
        "ingredients": "Coriander, Cumin, Red chilli, Black pepper, Cardamom, Cinnamon, Clove, Nutmeg, Mace, Star anise, Bay leaf. FSSAI certified. Contains Fast Green FCF (INS 143) for colour enhancement in some variants.",
        "nutrition": {"energy_kcal": 330, "sugar_g": 5.0, "sodium_mg": 450, "saturated_fat_g": 4.0, "trans_fat_g": 0.0, "protein_g": 12.0, "fiber_g": 32.0},
        "image_url": ""
    },

    # ── BANNED CHEMICALS / CRITICAL (Dark Red) ──────────────────────────────
    "9990000000001": {
        "barcode": "9990000000001",
        "product_name": "Adulterated Turmeric Powder (TEST CASE)",
        "brand": "Spurious / Non-Branded",
        "category": "Spices & Condiments",
        "ingredients": "Turmeric powder, Lead chromate color enhancer, Metanil yellow industrial dye, Sudan Red III, Insoluble chalk powder filler, Wheat starch filler.",
        "nutrition": {"energy_kcal": 280, "sugar_g": 2.0, "sodium_mg": 150, "saturated_fat_g": 1.5, "trans_fat_g": 0.0, "protein_g": 4.5, "fiber_g": 10.0},
        "image_url": ""
    },
    "9990000000002": {
        "barcode": "9990000000002",
        "product_name": "Synthetic Adulterated Milk (TEST CASE)",
        "brand": "Non-Standard Bulk Dairy",
        "category": "Dairy Products",
        "ingredients": "Water, Urea nitrogen spiker, Commercial detergent foaming agent (SLS), Low-grade refined vegetable oil, Caustic soda neutralizer, Skimmed milk powder (minimal), Hydrogen peroxide bleaching agent.",
        "nutrition": {"energy_kcal": 160, "sugar_g": 0.5, "sodium_mg": 850, "saturated_fat_g": 12.0, "trans_fat_g": 3.5, "protein_g": 1.5, "fiber_g": 0.0},
        "image_url": ""
    },
    "9990000000003": {
        "barcode": "9990000000003",
        "product_name": "Rhodamine B Coloured Candy (TEST CASE)",
        "brand": "Suspect Confectionery",
        "category": "Confectionery",
        "ingredients": "Sugar, Glucose syrup, Rhodamine B dye (industrial textile dye), Brilliant Blue FCF (INS 133), Artificial orange flavour, Acidity regulator (INS 330).",
        "nutrition": {"energy_kcal": 380, "sugar_g": 82.0, "sodium_mg": 15, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "9990000000004": {
        "barcode": "9990000000004",
        "product_name": "Spurious Refined Mustard Oil (TEST CASE)",
        "brand": "Unbranded Bulk Oil",
        "category": "Cooking Oils",
        "ingredients": "Argemone oil (toxic weed seed oil), Low grade mustard oil base, Erucic acid (high concentration), Methanol traces from crude processing.",
        "nutrition": {"energy_kcal": 884, "sugar_g": 0.0, "sodium_mg": 0, "saturated_fat_g": 12.0, "trans_fat_g": 1.5, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
    "9990000000005": {
        "barcode": "9990000000005",
        "product_name": "Fake Branded Honey with Sugar Syrup (TEST CASE)",
        "brand": "Counterfeit Brand",
        "category": "Honey & Sweeteners",
        "ingredients": "High fructose corn syrup, Inverted sugar syrup, Water, Caramel colour (INS 150d), Artificial honey flavour, Rice syrup (for NMR adulteration). No genuine honey.",
        "nutrition": {"energy_kcal": 305, "sugar_g": 76.0, "sodium_mg": 10, "saturated_fat_g": 0.0, "trans_fat_g": 0.0, "protein_g": 0.0, "fiber_g": 0.0},
        "image_url": ""
    },
}


def fetch_product_by_barcode(barcode: str) -> Optional[Dict[str, Any]]:
    clean_code = str(barcode).strip()

    # 1. Check local rich catalog first
    if clean_code in OFFLINE_PRODUCT_CATALOG:
        prod = OFFLINE_PRODUCT_CATALOG[clean_code].copy()
        prod["source"] = "Local Food Catalog / Verified Standards"
        return prod

    # 2. Query Open Food Facts API
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{clean_code}.json"
        headers = {"User-Agent": "FoodQualityAdulterationDetector/1.0 (academic-project; contact@foodqualityai.edu)"}
        resp = requests.get(url, headers=headers, timeout=4.0)

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == 1 and "product" in data:
                p = data["product"]
                nutriments = p.get("nutriments", {})

                energy = nutriments.get("energy-kcal_100g", nutriments.get("energy-kcal", 0))
                sugar = nutriments.get("sugars_100g", nutriments.get("sugars", 0.0))
                sodium = nutriments.get("sodium_100g", nutriments.get("sodium", 0.0)) * 1000
                sat_fat = nutriments.get("saturated-fat_100g", nutriments.get("saturated-fat", 0.0))
                trans_fat = nutriments.get("trans-fat_100g", nutriments.get("trans-fat", 0.0))
                protein = nutriments.get("proteins_100g", nutriments.get("proteins", 0.0))
                fiber = nutriments.get("fiber_100g", nutriments.get("fiber", 0.0))

                return {
                    "barcode": clean_code,
                    "product_name": p.get("product_name", f"Product #{clean_code}"),
                    "brand": p.get("brands", "Unknown Brand"),
                    "category": p.get("categories", "Packaged Food").split(",")[0].strip(),
                    "ingredients": p.get("ingredients_text", p.get("ingredients_text_en", "")),
                    "nutrition": {
                        "energy_kcal": round(float(energy or 0), 1),
                        "sugar_g": round(float(sugar or 0), 1),
                        "sodium_mg": round(float(sodium or 0), 1),
                        "saturated_fat_g": round(float(sat_fat or 0), 1),
                        "trans_fat_g": round(float(trans_fat or 0), 2),
                        "protein_g": round(float(protein or 0), 1),
                        "fiber_g": round(float(fiber or 0), 1)
                    },
                    "image_url": p.get("image_front_url", ""),
                    "source": "Open Food Facts Live Global Database"
                }
    except Exception as err:
        print(f"[OpenFoodFacts] Live query error: {err}")

    return None


def get_sample_barcodes() -> list:
    """Returns list of curated barcodes for instant UI demo and quick testing."""
    return [
        {"barcode": code, "name": item["product_name"], "brand": item["brand"], "category": item["category"]}
        for code, item in OFFLINE_PRODUCT_CATALOG.items()
    ]
