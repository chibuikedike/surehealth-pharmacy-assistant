import pandas as pd
import random
from datetime import datetime, timedelta

medications = [
    "Paracetamol",
    "Ibuprofen",
    "Diclofenac",
    "Naproxen",
    "Meloxicam",
    "Celecoxib",
    "Aspirin",
    "Tramadol",
    "Codeine",
    "Morphine",
    "Amoxicillin",
    "Ampicillin",
    "Cloxacillin",
    "Flucloxacillin",
    "Azithromycin",
    "Erythromycin",
    "Clarithromycin",
    "Ciprofloxacin",
    "Levofloxacin",
    "Moxifloxacin",
    "Doxycycline",
    "Tetracycline",
    "Metronidazole",
    "Tinidazole",
    "Cefuroxime",
    "Cefixime",
    "Ceftriaxone",
    "Cefotaxime",
    "Gentamicin",
    "Nitrofurantoin",
    "Amlodipine",
    "Nifedipine",
    "Losartan",
    "Valsartan",
    "Telmisartan",
    "Lisinopril",
    "Enalapril",
    "Ramipril",
    "Hydrochlorothiazide",
    "Furosemide",
    "Spironolactone",
    "Bisoprolol",
    "Atenolol",
    "Carvedilol",
    "Propranolol",
    "Methyldopa",
    "Hydralazine",
    "Clopidogrel",
    "Warfarin",
    "Atorvastatin",
    "Rosuvastatin",
    "Simvastatin",
    "Metformin",
    "Gliclazide",
    "Glimepiride",
    "Pioglitazone",
    "Insulin Regular",
    "Insulin Glargine",
    "Insulin Aspart",
    "Empagliflozin",
    "Dapagliflozin",
    "Omeprazole",
    "Esomeprazole",
    "Pantoprazole",
    "Lansoprazole",
    "Famotidine",
    "Cimetidine",
    "Aluminium Hydroxide",
    "Magnesium Hydroxide",
    "Loperamide",
    "Ondansetron",
    "Domperidone",
    "Metoclopramide",
    "Salbutamol",
    "Terbutaline",
    "Ipratropium",
    "Budesonide",
    "Beclometasone",
    "Montelukast",
    "Cetirizine",
    "Loratadine",
    "Fexofenadine",
    "Chlorpheniramine",
    "Diphenhydramine",
    "Prednisolone",
    "Dexamethasone",
    "Hydrocortisone",
    "Methylprednisolone",
    "Betamethasone",
    "Levothyroxine",
    "Carbimazole",
    "Propylthiouracil",
    "Calcium Carbonate",
    "Vitamin C",
    "Vitamin D3",
    "Vitamin B Complex",
    "Folic Acid",
    "Ferrous Sulphate",
    "Zinc Sulphate",
    "Magnesium Sulphate",
    "Potassium Chloride",
    "Albendazole",
    "Mebendazole",
    "Praziquantel",
    "Artemether",
    "Lumefantrine",
    "Artesunate",
    "Quinine",
    "Chloroquine",
    "Sulfadoxine",
    "Pyrimethamine",
    "Acyclovir",
    "Valacyclovir",
    "Oseltamivir",
    "Fluconazole",
    "Itraconazole",
    "Ketoconazole",
    "Nystatin",
    "Clotrimazole",
    "Terbinafine",
    "Haloperidol",
    "Chlorpromazine",
    "Risperidone",
    "Olanzapine",
    "Quetiapine",
    "Sertraline",
    "Fluoxetine",
    "Paroxetine",
    "Escitalopram",
    "Amitriptyline",
    "Diazepam",
    "Lorazepam",
    "Clonazepam",
    "Alprazolam",
    "Carbamazepine",
    "Sodium Valproate",
    "Phenytoin",
    "Levetiracetam",
    "Lamotrigine",
    "Gabapentin",
    "Pregabalin",
    "Allopurinol",
    "Colchicine",
    "Methotrexate",
    "Sulfasalazine",
    "Hydroxychloroquine",
    "Azathioprine",
    "Cyclophosphamide",
    "Tacrolimus",
    "Cyclosporine",
    "Finasteride",
    "Tamsulosin",
    "Sildenafil",
    "Tadalafil",
    "Oxybutynin",
    "Duloxetine",
    "Venlafaxine",
    "Bupropion",
    "Mirtazapine",
    "Citalopram",
    "Topiramate",
    "Donepezil",
    "Memantine",
    "Rivastigmine",
    "Bromocriptine",
    "Levodopa",
    "Carbidopa",
    "Pramipexole",
    "Ropinirole",
    "Timolol",
    "Latanoprost",
    "Brimonidine",
    "Acetazolamide",
    "Pilocarpine",
    "Dorzolamide",
    "Amiodarone",
    "Digoxin",
    "Verapamil",
    "Diltiazem",
    "Isosorbide Mononitrate",
    "Nitroglycerin",
    "Heparin",
    "Enoxaparin",
    "Apixaban",
    "Rivaroxaban",
    "Dabigatran",
    "Tranexamic Acid",
    "Ethambutol",
    "Isoniazid",
    "Rifampicin",
    "Pyrazinamide",
    "Linezolid",
    "Meropenem",
    "Imipenem",
    "Piperacillin",
    "Tazobactam",
    "Vancomycin"
]

# ==========================
# CATEGORY RULES
# ==========================

category_rules = {
    "Antibiotic": {
        "keywords": [
            "cillin", "floxacin", "cycline", "cef", "mycin",
            "linezolid", "vancomycin", "meropenem", "imipenem",
            "rifampicin", "isoniazid", "ethambutol", "pyrazinamide",
            "tazobactam", "piperacillin"
        ],
        "strengths": ["125mg", "250mg", "500mg", "625mg", "1g"],
        "forms": ["Tablet", "Capsule", "Suspension", "Injection"]
    },

    "Antihypertensive": {
        "keywords": [
            "dipine", "sartan", "pril", "olol",
            "methyldopa", "hydralazine", "diltiazem",
            "verapamil"
        ],
        "strengths": ["2.5mg", "5mg", "10mg", "25mg", "50mg", "100mg"],
        "forms": ["Tablet"]
    },

    "Diuretic": {
        "keywords": [
            "furosemide",
            "spironolactone",
            "hydrochlorothiazide"
        ],
        "strengths": ["25mg", "40mg", "50mg", "100mg"],
        "forms": ["Tablet"]
    },

    "Antidiabetic": {
        "keywords": [
            "metformin",
            "gliclazide",
            "glimepiride",
            "pioglitazone",
            "insulin",
            "gliflozin"
        ],
        "strengths": ["500mg", "850mg", "1000mg", "10mg", "25mg"],
        "forms": ["Tablet", "Injection"]
    },

    "NSAID": {
        "keywords": [
            "ibuprofen",
            "diclofenac",
            "naproxen",
            "meloxicam",
            "celecoxib"
        ],
        "strengths": ["50mg", "100mg", "200mg", "400mg", "500mg"],
        "forms": ["Tablet", "Capsule", "Gel"]
    },

    "Analgesic": {
        "keywords": [
            "paracetamol",
            "tramadol",
            "codeine",
            "morphine"
        ],
        "strengths": ["500mg", "650mg", "1000mg"],
        "forms": ["Tablet", "Syrup", "Injection"]
    },

    "Statin": {
        "keywords": [
            "statin"
        ],
        "strengths": ["10mg", "20mg", "40mg", "80mg"],
        "forms": ["Tablet"]
    },

    "Respiratory": {
        "keywords": [
            "salbutamol",
            "terbutaline",
            "ipratropium",
            "budesonide",
            "montelukast",
            "beclometasone"
        ],
        "strengths": ["100mcg", "200mcg", "2mg", "4mg"],
        "forms": ["Inhaler", "Tablet", "Nebule"]
    },

    "Antihistamine": {
        "keywords": [
            "cetirizine",
            "loratadine",
            "fexofenadine",
            "chlorpheniramine",
            "diphenhydramine"
        ],
        "strengths": ["4mg", "10mg", "120mg", "180mg"],
        "forms": ["Tablet", "Syrup"]
    },

    "Corticosteroid": {
        "keywords": [
            "prednisolone",
            "dexamethasone",
            "hydrocortisone",
            "betamethasone",
            "methylprednisolone"
        ],
        "strengths": ["4mg", "5mg", "20mg", "40mg", "100mg"],
        "forms": ["Tablet", "Injection", "Cream"]
    },

    "Antimalarial": {
        "keywords": [
            "artemether",
            "lumefantrine",
            "artesunate",
            "quinine",
            "chloroquine",
            "sulfadoxine",
            "pyrimethamine"
        ],
        "strengths": ["20/120mg", "50mg", "100mg", "200mg"],
        "forms": ["Tablet", "Injection"]
    },

    "Antifungal": {
        "keywords": [
            "azole",
            "nystatin",
            "clotrimazole",
            "terbinafine"
        ],
        "strengths": ["100mg", "150mg", "200mg", "500mg"],
        "forms": ["Tablet", "Capsule", "Cream"]
    },

    "Antiviral": {
        "keywords": [
            "cyclovir",
            "oseltamivir"
        ],
        "strengths": ["200mg", "400mg", "500mg", "800mg"],
        "forms": ["Tablet", "Capsule"]
    },

    "Psychiatric": {
        "keywords": [
            "haloperidol",
            "chlorpromazine",
            "risperidone",
            "olanzapine",
            "quetiapine",
            "sertraline",
            "fluoxetine",
            "paroxetine",
            "escitalopram",
            "amitriptyline",
            "diazepam",
            "lorazepam",
            "clonazepam",
            "alprazolam",
            "venlafaxine",
            "duloxetine",
            "mirtazapine",
            "citalopram",
            "bupropion"
        ],
        "strengths": ["5mg", "10mg", "25mg", "50mg", "100mg"],
        "forms": ["Tablet"]
    },

    "Antiepileptic": {
        "keywords": [
            "carbamazepine",
            "valproate",
            "phenytoin",
            "levetiracetam",
            "lamotrigine",
            "gabapentin",
            "pregabalin",
            "topiramate"
        ],
        "strengths": ["100mg", "200mg", "300mg", "500mg"],
        "forms": ["Tablet", "Capsule"]
    },

    "Anticoagulant": {
        "keywords": [
            "warfarin",
            "heparin",
            "enoxaparin",
            "apixaban",
            "rivaroxaban",
            "dabigatran",
            "clopidogrel"
        ],
        "strengths": ["2.5mg", "5mg", "10mg", "20mg", "40mg"],
        "forms": ["Tablet", "Injection"]
    }
}

# ==========================
# HELPERS
# ==========================

def get_category(drug):
    name = drug.lower()

    for category, data in category_rules.items():
        for keyword in data["keywords"]:
            if keyword in name:
                return category

    return "General Medicine"

brands = [
    "Pfizer",
    "GSK",
    "Emzor",
    "Fidson",
    "May & Baker",
    "Juhel",
    "Evans",
    "Swiss Pharma",
    "Neimeth",
    "Drugfield"
]

suppliers = [
    "Emzor Pharmaceuticals",
    "Fidson Healthcare",
    "May & Baker Nigeria",
    "Drugfield Pharmaceuticals",
    "Evans Medical",
    "Swiss Pharma Nigeria"
]

locations = [
    "A1","A2","A3",
    "B1","B2","B3",
    "C1","C2","C3",
    "D1","D2","D3"
]

records = []

for i in range(2000):

    drug = random.choice(medications)

    category = get_category(drug)

    if category == "General Medicine":
        strengths = ["5mg", "10mg", "25mg", "50mg", "100mg"]
        forms = ["Tablet", "Capsule"]
    else:
        strengths = category_rules[category]["strengths"]
        forms = category_rules[category]["forms"]

    purchase_price = random.randint(100, 20000)

    expiry_date = (
        datetime.today() +
        timedelta(days=random.randint(90, 1460))
    ).strftime("%Y-%m-%d")

    records.append({
        "SKU": f"SKU{i+1:05d}",
        "Medication Name": drug,
        "Category": category,
        "Strength": random.choice(strengths),
        "Dosage Form": random.choice(forms),
        "Brand Name": random.choice(brands),
        "Purchase Price (₦)": purchase_price,
        "Selling Price (₦)": round(purchase_price * random.uniform(1.15, 1.60), 2),
        "Current Stock": random.randint(0, 1000),
        "Reorder Level": random.randint(20, 100),
        "Batch Number": f"BT{random.randint(100000,999999)}",
        "Supplier": random.choice(suppliers),
        "Warehouse Location": random.choice(locations),
        "Expiry Date": expiry_date
    })

df = pd.DataFrame(records)

df.to_csv("./documents/pharmacy_inventory_2000.csv", index=False)

print(df.head())
print(f"Generated {len(df)} records")
print(f"Unique drugs: {df['Medication Name'].nunique()}")