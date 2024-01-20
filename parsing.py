import pandas as pd

fda_data = pd.read_csv(r"C:\Users\Leonardo\Documents\GitHub\beginnerTrackS\CAERS_ProductBased.csv")
fda_subUniversal = fda_data.drop(columns = ['AGE_UNITS', 'CASE_OUTCOME'])

fda_subUniversal['PRODUCT'] = fda_subUniversal['PRODUCT'].str.lower()
med_case = fda_subUniversal.dropna(subset=['PRODUCT'])
med_case = med_case.dropna(axis = 1, how = "all")
straw = med_case[med_case['PRODUCT'].str.contains('strawb', na = False)]

word_freq = med_case.PRODUCT.str.split(expand = True).stack().value_counts()
word_freq.to_csv('wordFreq.csv')
#straw = med_case['PRODUCT'].str.contains('strawb')
women_data = med_case[med_case['SEX'].str.startswith("Male") == False]
women_data = women_data[women_data['SEX'].str.startswith("Unknown") == False]
male_data = med_case[med_case['SEX'].str.startswith("Female") == False]
male_data = male_data[male_data['SEX'].str.startswith("Unknown") == False]
women_data.to_csv('female_data.csv')
male_data.to_csv('male_data.csv')
no5455_data = med_case[med_case['PRODUCT_CODE'] != '54']
no5455_data = no5455_data[no5455_data['PRODUCT_CODE'] != '53']
no5455_data.to_csv('excludeSupplementsCosmetics.csv')

#supplements and 
