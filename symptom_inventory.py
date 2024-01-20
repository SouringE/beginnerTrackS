import pandas as pd
from collections import defaultdict
df = pd.read_csv("CAERS_ProductBased.csv")
df = df.dropna(axis=1, how="all")
#df = df[df["PRODUCT_TYPE"] == "SUSPECT"]
#df = df[df["PRODUCT"] != "EXEMPTION 4"]

print(df)

vitamins = df['PRODUCT_CODE'].str.contains('54')
vitamin_data = df[vitamins]

cosmetics = df['PRODUCT_CODE'].str.contains('53')
cosmetic_data = df[cosmetics]

cosmetics = df['PRODUCT_CODE'].str.contains('53')
cosmetic_data = df[cosmetics]

symptoms = df['CASE_MEDDRA_PREFERRED_TERMS']

prod_types = df['PRODUCT_TYPE']
prods = df['PRODUCT']
print(symptoms)

symptom_prevalence = defaultdict(list)

# this creates a dictionary mapping each symptom to which *indexes* of the csv experience it
for case_idx in range(len(symptoms)): 
    #symptoms = df['CASE_MEDDRA_PREFERRED_TERMS']
    #print(case)
    #print(type(case))
    if prods[case_idx] != "EXEMPTION 4" and prod_types[case_idx] == "SUSPECT":
        sym_list = [x.lower() for x in symptoms[case_idx].split(", ")]
        for symptom in sym_list:
            #if()
            symptom_prevalence[symptom].append(case_idx)

#print(symptom_prevalence)

symptom_cats = defaultdict(list) 

#symptom_types = ["cardiac" : ]

# this creates a separate dictionary mapping each symptom to another dictionary mapping each category to the list of 
# cases experiencing that symptom in that category (the idea is more cases in the same category with a particular symptom
# indicate a trend with a certain type of product)
for symp in symptom_prevalence:
    cases = symptom_prevalence[symp]
    cat_matches = defaultdict(list)
    for case in cases:
        cat = df['PRODUCT_CODE'][case]
        case_num = df['REPORT_ID'][case]
        #print(case_num)
        if case_num not in cat_matches[cat]:
            cat_matches[cat].append(case_num)
    cat_lengths = {}
    for cat in cat_matches:
        cat_lengths[cat] = len(cat_matches[cat])
    #print(symp, dict(cat_matches))
    #symptom_cats[symp] = dict(cat_matches)
    symptom_cats[symp] = dict(cat_lengths)

#print(symptom_cats)
   
# prints out the contents of the symptoms dictionary to a file titled symptomlist.txt
with open('symptomlist.txt', 'w') as f:
    for sympt in symptom_cats:
        sympt_dict = symptom_cats[sympt]
        #print(sympt_dict)
        line = str(sympt) + " : " + str(sympt_dict) + "\n"
        f.write(line)

print(symptom_cats.keys(), len(symptom_cats.keys()))

#print(vitamin_data)