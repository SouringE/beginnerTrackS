import pandas as pd
from collections import defaultdict
import operator
df = pd.read_csv("CAERS_ProductBased.csv")
df = df.dropna(axis=1, how="all")

print(df)

"""
Returns a new dataframe containing only the data containing a particular term in 
the given column
Inputs: df, the dataframe you want to create a sub-df of
        col_name, a String for the name of the column you're looking through
        terms, a list containing Strings for the keyword terms you're looking for
        equal, a boolean representing whether you want the terms to just be equal to the value in
            the column or just be contained within it
        include, a boolean representing whether you want to include values containing the
            terms or exclude them
Outputs: The new sub-dataframe fitting the criteria
"""
def df_subset(df, col_name, terms, equal, include, operator_fxn=operator.eq, contain_type=None):
    new_dfs = []
    for term in terms:
        new_df = df.copy()
        if equal:
            if include:
                new_df = new_df[operator_fxn(new_df[col_name], term)]
            else:
                operator_fxn = operator.ne
                #print(operator_fxn(new_df[col_name], term))
                new_df = new_df[operator_fxn(new_df[col_name], term)]
        elif include:
            if contain_type == "ends":
                new_df = new_df[new_df[col_name].str.endswith(term)]
            elif contain_type == "starts":
                new_df = new_df[new_df[col_name].str.startswith(term)]
            else:
                new_df = new_df[new_df[col_name].str.contains(term)]     
        else: 
            if contain_type == "ends":
                new_df = new_df[not new_df[col_name].str.endswith(term)]
            elif contain_type == "starts":
                new_df = new_df[not new_df[col_name].str.startswith(term)]
            else:
                new_df = new_df[not new_df[col_name].str.contains(term)]
        #print(new_df)
        new_dfs.append(new_df)
    final_df = pd.concat(new_dfs)
    final_df.reset_index(drop = True, inplace = True)
    return final_df

df = df_subset(df, "PRODUCT_TYPE", ["SUSPECT"], True, True)
#df = df_subset(df, "SEX", ["Female"], True, True)
df = df_subset(df, "PRODUCT", ["EXEMPTION 4"], True, False)
#df = df_subset(df, "DATE_FDA_FIRST_RECEIVED_REPORT", ["23"], False, True, contain_type="ends")
print(df)


"""
Creates a dictionary mapping each symptom present in the given dataframe to which indexes 
of the CSV experience those symptoms.
Inputs: Any dataframe you want to find symptom prevalence in
Outputs: The prevalence dictionary
"""
def symptom_prevalence(df, column="CASE_MEDDRA_PREFERRED_TERMS", split=True, delim=", "):
    symptom_df = df[column]
    symptom_prev = defaultdict(list)
    for case_idx in range(len(symptom_df)): 
        if split:
            sym_list = [x.lower() for x in symptom_df[case_idx].split(delim)]
            for symptom in sym_list:
                symptom_prev[symptom].append(case_idx)
        else: 
            sym = symptom_df[case_idx]
            symptom_prev[sym].append(case_idx)
        
    return dict(symptom_prev)

"""
Sorts the symptoms dictionary for the dataframe in decreasing order of symptom frequency.
Input: input_dict, the dictionary returned by calling symptom_prevalence on the dataframe
        of interest
        filename, name of the file you want to print the dictionary to
Outputs: Returns the sorted dictionary and writes it to filename
"""
def dict_sort(input_dict, filename=None, file=True, header=None):      
    freq_dict = {}
    for item in input_dict:
        freq_dict[item] = len(input_dict[item])
    sorted_freqs = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse = True))
    # writes the dictionary sorted in decreasing order of frequency to the given filename
    if file:
        with open(filename, 'w') as f:
            if header != None:
                f.write(header + "\n\n")
            for freq in sorted_freqs:
                line = freq + " : " + str(sorted_freqs[freq]) + "\n"
                f.write(line)
    return sorted_freqs

"""
Creates a separate dictionary mapping each symptom to another dictionary mapping each category to the list of 
cases experiencing that symptom in that category, and writes it to the file filename.
(The idea is more cases in the same category with a particular symptom indicate a trend with a certain type of product.)
Input: df, the dataframe to perform the categorization on
        symptom_p, the prevalence dictionary returned by symptom_prevalence()
        filename, the name of the file to write the dictionary to
Output: A dictionary mapping symptoms to a mapping of categories to prevalence.
"""
def symptom_categorizer(df, symptom_p, filename, col_name='PRODUCT_CODE'):
    symptom_cats = defaultdict(list) 

    for symp in symptom_p:
        cases = symptom_p[symp]
        cat_matches = defaultdict(list)
        for case in cases:
            cat = df[col_name][case]
            case_num = df['REPORT_ID'][case]
            #print(case_num)
            if case_num not in cat_matches[cat]:
                cat_matches[cat].append(case_num)
        cat_lengths = {}
        for cat in cat_matches:
            cat_lengths[cat] = len(cat_matches[cat])
        #symptom_cats[symp] = dict(cat_matches) --- For if you want a list of all case IDs instead of number of cases
        symptom_cats[symp] = dict(sorted(dict(cat_lengths).items(), key=lambda item: item[1], reverse = True))
   
    # prints out the contents of the symptoms dictionary to a file titled symptomlist.txt
    with open(filename, 'w') as f:
        for sympt in symptom_cats:
            sympt_dict = symptom_cats[sympt]
            #print(sympt_dict)
            line = str(sympt) + " : " + str(sympt_dict) + "\n"
            f.write(line)
    
    return symptom_cats


# symptom frequency for the entire dataframe
symptom_p = symptom_prevalence(df)
dict_sort(symptom_p, "symptomfreq.txt")

symptom_categorizer(df, symptom_p, 'symptomlist.txt')

# symptom frequency for just cosmetic products
cosmetics = df_subset(df, "PRODUCT_CODE", ["53"], True, True)
symptoms_53 = symptom_prevalence(cosmetics)
dict_sort(symptoms_53, "cosmeticsymptoms.txt")
#print(cosmetics)

# symptom frequency for just vitamins
vitamins = df_subset(df, "PRODUCT_CODE", ["54"], True, True)
symptoms_54 = symptom_prevalence(vitamins)
dict_sort(symptoms_54, "vitaminsymptoms.txt")

# food dyes
dyes = df_subset(df, "PRODUCT_CODE", ["50"], True, True)
symptoms_50 = symptom_prevalence(dyes)
dict_sort(symptoms_50, "dyesymptoms.txt")

#symptom_types = ["cardiac" : ]

#word_freq = df.DESCRIPTION.str.split(expand = True).stack().value_counts()
#print(word_freq)
category_types = symptom_prevalence(df, "DESCRIPTION", False, None)
dict_sort(category_types, "categoryfreqs.txt")

category_codes = symptom_prevalence(df, "PRODUCT_CODE", False, None)

category_names = list(category_types.keys())
category_nums = list(category_codes.keys())

category_corr = defaultdict(list)
for name in category_names:
    cat_nums = []
    only_this_cat = df_subset(df, "DESCRIPTION", [name], True, True)
    for idx in range(len(only_this_cat)):
        category_name = only_this_cat["PRODUCT_CODE"][idx] 
        num = only_this_cat["PRODUCT_CODE"][idx]
        if num not in cat_nums:
            cat_nums.append(num)
    category_corr[name] = cat_nums

print(category_corr)

for category in category_names:
    print(category)
    filename = category_corr[category][0] + ".txt"
    data = df_subset(df, "DESCRIPTION", [category], True, True)
    symptoms_data = symptom_prevalence(data)
    dict_sort(symptoms_data, filename, header=str(category))
    
    # only_this_cat = df_subset(df, ["DESCRIPTION"], category, True, True)
    # print(only_this_cat)
    # num = only_this_cat.at[0, "PRODUCT_CODE"]
    # print(num)
    # category_nums[category] = num

# print(category_nums)
    
prod_types = symptom_prevalence(df, "PRODUCT", False, None)
prod_freq = dict_sort(prod_types, "productfreqs.txt")

symptom_categorizer(df, symptom_p, 'productsymptoms.txt', col_name="PRODUCT")

product_symptoms = {}

# with open("symptomtoproduct.txt", 'w') as f:
#     for product in prod_types:
#         #print(category)
#         #filename = category_corr[category][0] + ".txt"
#         data = df_subset(df, "PRODUCT", [product], True, True)
#         symptoms_data = symptom_prevalence(data)
#         symptoms = dict_sort(symptoms_data, file=False)
#         product_symptoms[product] = symptoms
#         #print(symptoms)
#         f.write(product + " : " + str(symptoms) + "\n")


for product in prod_types:
    #print(category)
    #filename = category_corr[category][0] + ".txt"
    data = df_subset(df, "PRODUCT", [product], True, True)
    symptoms_data = symptom_prevalence(data)
    symptoms = dict_sort(symptoms_data, file=False)
    product_symptoms[product] = symptoms
    #print(symptoms)
    
with open("symptomtoproduct.txt", 'w') as f:
    for product in prod_freq:
        symptoms = product_symptoms[product]
        f.write(product + " : " + str(symptoms) + "\n")

#symptom_categorizer(df, prod_types, 'productsymptoms.txt', col_name="PRODUCT")



#agefilter = df_subset(df, "AGE_UNITS", ["year", "decade"], False, True)
#agefilter = df_subset(df, "PATIENT_AGE", ["5"], True, False, operator_fxn=operator.gt)

#age = df[df[("PATIENT_AGE"].str.endswith(term)]