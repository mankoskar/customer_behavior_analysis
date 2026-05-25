import pandas as pd # selecting library
df=pd.read_csv("customer_shopping_behavior.csv") # reading data from csv file
print(df.head()) # printing first 5 rows of data and showing structure of data
print(df.info()) # showing information about data types and non-null values
print(df.describe(include='all')) # showing statistical summary of numerical and categorical columns in the data    
print(df.isnull().sum()) # checking for missing values in each column of the data
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()) ) # filling missing values in 'Review Rating' column with median rating of each product category
print(df.isnull().sum()) # checking again for missing values after filling them
df.columns = df.columns.str.replace(' ', '_') # replacing spaces with underscores in column names
df.columns = df.columns.str.lower()
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
print(df.columns)
labels = ['Young Adults', 'Adults', 'Seniors','Middle-aged']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels) # creating age groups based on quartiles of 'Age' column
print(df[['age_group', 'age']].head(10)) # showing first 10 rows of 'age_group' and 'Age' columns to verify age groups
frequency_mapping ={'fortnightly': 14, 'weekly': 7, 'monthly': 30, 'quarterly': 90, 'annually': 365,'every 3 months': 90} # mapping purchase frequency to numerical values
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping) # creating new column with mapped values of purchase frequency
print(df[['purchase_frequency_days', 'frequency_of_purchases']].head(10)) # showing first 10 rows of 'purchase_frequency' and 'purchase_frequency_days' columns to verify mapping 
print(df[['discount_applied','promo_code_used']].head(10)) # showing first 10 rows of 'discount_applied' and 'promo_code_used' columns
(df['discount_applied']==df['promo_code_used']).all() # checking if 'discount_applied' and 'promo_code_used' columns have the same values for all rows 
df=df.drop('promo_code_used', axis=1) # dropping 'promo_code_used' column since it is redundant
df.columns
from sqlalchemy import create_engine
username = "postgres"
password = "kapil123"
host = "localhost"
port ="5432"
database = "customer_behavior"
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")
table_name = "customer"
df.to_sql(table_name,engine,if_exists="replace",index=False)
print(f"Data has been successfully inserted into the '{table_name}' table in the '{database}' database.")