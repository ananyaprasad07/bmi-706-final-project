import pandas as pd
import re

neiss2022 = pd.read_csv('neiss2022.tsv', sep='\t')
neiss2023 = pd.read_csv('neiss2023.tsv', sep='\t')

#fixing column name disparities
neiss2023.rename(columns={'Gender': 'Sex'}, inplace=True)

# concatnating both years
neiss_pre = pd.concat([neiss2022, neiss2023], axis=0)

# keeping relevant columns
cols_to_keep = ['CPSC_Case_Number', 'Treatment_Date', 'Age', 'Sex', 'Race',
                'Body_Part', 'Disposition', 'Location', 'Product_1']

# dropping rows containing na values
neiss = neiss_pre[cols_to_keep]
neiss = neiss.dropna()

# droppingm non-head injuries (head code = 75)
neiss = neiss.loc[neiss['Body_Part'] == 75.0]

# change age over 200 (infants) to 0
neiss.loc[neiss['Age'] >= 200, 'Age'] = 0

# change sex from numeric to text (1=Male, 2=Female)
sex_codes = {1.0: 'Male', 2.0:'Female', 3.0:'Other', 0.0:'Unknown'} 
neiss['Sex'] = neiss['Sex'].replace(sex_codes)

# change race from numeric to text 
race_codes = {0.0: "Not Stated", 1.0: "White", 2.0: "Black/African American", 
              3.0: "Other", 4.0: "Asian", 5.0: "American Indian/Alaska Native", 
              6.0: "Native Hawaiian/Pacific Islander"}
neiss['Race'] = neiss['Race'].replace(race_codes)

# change location from numeric to text
location_codes = {1.0: 'Home', 0.0: 'Not recorded', 5.0: 'Public', 
                  9.0: 'Sports', 8.0: 'School', 4.0: 'Street', 2.0:'Farm', 
                  6.0:'Mobile Home', 7.0: 'Industrial'}
neiss['Location'] = neiss['Location'].replace(location_codes)

# change product from numeric to text using product codes
product_codes = {}
with open('neiss_product_codes.txt', 'r') as file:
    next(file)
    for line in file:
        number, name = re.split(r'\s+', line.strip(), maxsplit=1)
        product_codes[float(number)] = name

neiss['Product_1'] = neiss['Product_1'].replace(product_codes)

# add a year and month column
neiss['Treatment_Date'] = pd.to_datetime(neiss['Treatment_Date'], format='%m/%d/%Y')
neiss['Year'] = neiss['Treatment_Date'].dt.year
neiss['Month'] = neiss['Treatment_Date'].dt.month.apply(lambda x: calendar.month_abbr[x])


# naming the disposition
disposition_codes = {1.0: 'Treated, Released', 2.0: 'Treated, Tranferred', 4.0: 'Treated, Admitted', 
                     5.0: 'Held', 6.0: 'Left Against Medical Advice', 
                     8.0: 'Death', 9.0: 'Not recorded'}

neiss['Disposition_Expanded'] = neiss['Disposition'].map(disposition_codes)

# dropping unspecified disposition
neiss.drop(neiss[neiss['Disposition_Expanded'] == 'Not recorded'].index, inplace=True)

#quantifying the disposition
disposition_codes_2 = {1.0: 1, 2.0: 2, 4.0: 3, 
                     5.0: 4, 6.0: 5, 
                     8.0: 6}
neiss['Disposition'] = neiss['Disposition'].replace(disposition_codes_2)
neiss['Disposition'] = neiss['Disposition'].astype(int)

#create age group
age_bins = [0, 4, 14, 24, 34, 44, 54, 64, float('inf')]
age_labels = ["Age <5", "Age 5-14", "Age 15-24", "Age 25-34", "Age 35-44", "Age 45-54", "Age 55-64", "Age >64"]
neiss['Age_group'] = pd.cut(neiss['Age'], bins=age_bins, labels=age_labels, right=True)

# write to data file
neiss.to_csv('neiss_head_injuries.tsv', sep='\t', index=False)



