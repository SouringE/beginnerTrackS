import pandas as pd

fda_data = pd.read_csv(r"C:\Users\Leonardo\Documents\GitHub\beginnerTrackS\CAERS_ProductBased.csv")
fda_subUniversal = fda_data.drop(columns = ['AGE_UNITS', 'CASE_OUTCOME'])

fda_subUniversal['PRODUCT'] = fda_subUniversal['PRODUCT'].str.lower()
med_case = fda_subUniversal.dropna(subset=['PRODUCT'])
straw = med_case[med_case['PRODUCT'].str.contains('strawb', na = False)]
print(straw)
word_freq = med_case.PRODUCT.str.split(expand = True).stack().value_counts()
word_freq.to_csv('wordFreq.csv')
#straw = med_case['PRODUCT'].str.contains('strawb')
print(med_case.columns)

print(fda_data.shape)