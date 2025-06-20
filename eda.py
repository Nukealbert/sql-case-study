import pandas as pd

try:
    sales_df=pd.read_csv('sales_transaction.csv')
    customers_df=pd.read_csv('customer_profiles.csv')
    product_df=pd.read_csv('product_inventory.csv')
except FileNotFoundError as e:
    print(f"Error loading files:{e}")
    exit()
#-----EDA start for sales data ------#

print("--- Sales Transactions Data Cleaning ---")
print('Original Sales DF info:')
sales_df.info()
print('\nOriginal Sales DF info:')

# dublicate transaction id removed
sales_df.drop_duplicates(inplace=True)
print(sales_df['TransactionID'])

# Check for null values in sales_df (this is fine for now)

print(sales_df.isnull().sum())

# TransactionID        0
# CustomerID           0
# ProductID            0
# QuantityPurchased    0
# TransactionDate      0
# Price                0
# dtype: int64

sales_df['TransactionDate']=pd.to_datetime(sales_df['TransactionDate'])
#change TransactionDate string to datetime

#sales_df.info()

# Data columns (total 6 columns):
#  #   Column             Non-Null Count  Dtype  
# ---  ------             --------------  -----  
#  0   TransactionID      5002 non-null   int64  
#  1   CustomerID         5002 non-null   int64  
#  2   ProductID          5002 non-null   int64  
#  3   QuantityPurchased  5002 non-null   int64  
#  4   TransactionDate    5002 non-null   object 
#  5   Price              5002 non-null   float64
# dtypes: float64(1), int64(4), object(1)




# ------ EDA done for sales data ------------ #


# 2 customers data 


# customers_df.info()

# Data columns (total 5 columns):
 #   Column      Non-Null Count  Dtype 
# ---  ------      --------------  ----- 
#  0   CustomerID  1000 non-null   int64 
#  1   Age         1000 non-null   int64 
#  2   Gender      1000 non-null   object
#  3   Location    987 non-null    object
#  4   JoinDate    1000 non-null   object

# 1. JoinDate is not date it is object
# 2. 13 Location is missing we can use ffill or bfill
customers_df['JoinDate']=pd.to_datetime(customers_df['JoinDate'])
customers_df['Location'].fillna('Unknown',inplace=True)
customers_df.info()

# ------ EDA done for customers data ------------ #

# 3. product data
product_df.info()
uniqueP=product_df['ProductID'].unique()
print(uniqueP)

# this data is look fine. we can proceed with this

# Data columns (total 5 columns):
#  #   Column       Non-Null Count  Dtype  
# ---  ------       --------------  -----  
#  0   ProductID    200 non-null    int64  
#  1   ProductName  200 non-null    object 
#  2   Category     200 non-null    object 
#  3   StockLevel   200 non-null    int64  
#  4   Price        200 non-null    float64
# dtypes: float64(1), int64(2), object(2)

# Correct discrepancies in product prices between sales transactions and product inventory
# Ensure 'ProductID' exists in both dataframes before merging

if 'ProductID' in sales_df.columns and 'ProductID' in product_df.columns:
    # Merge sales and products to compare prices, using a temporary merge to identify discrepancies
    # We will use the 'Price' column from product_df as the source of truth
    sales_df = pd.merge(sales_df, product_df[['ProductID', 'Price']], on='ProductID', suffixes=('_sale', '_inventory'))

    # Update the 'Price' column in sales_df with the correct prices from product_df
    # The 'Price_inventory' column contains the correct prices after the merge
    sales_df['Price'] = sales_df['Price_inventory']

    # Drop the temporary columns used for price comparison
    sales_df.drop(columns=['Price_sale', 'Price_inventory'], inplace=True)
    print("\nCorrected price discrepancies in sales_df using product_inventory prices and dropped temporary columns.")

    # Check for duplicates again after price correction
    initial_sales_rows_after_price_correction = sales_df.shape[0]
    sales_df.drop_duplicates(inplace=True)
    print(f"Removed {initial_sales_rows_after_price_correction - sales_df.shape[0]} duplicate transactions after price correction from sales_df.")

else:
    print("\nError: 'ProductID' not found in both sales_df and product_df. Please check column names.")
    exit()

# Display info and head of cleaned sales_df
print("\nCleaned Sales DF info:")
sales_df.info()

customers_df.to_csv('customer_profiles_cleaned.csv', index=False)
product_df.to_csv('product_inventory_cleaned.csv', index=False)
sales_df.to_csv('sales_transaction_cleaned.csv', index=False)
