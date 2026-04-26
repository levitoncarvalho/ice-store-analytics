import pandas as pd
import numpy as np

def preprocess_data(df):
    """
    Clean and prepare the raw dataframe:
    - Lowercase column names
    - Convert 'user_score' from string (with 'tbd') to numeric
    - Convert 'year_of_release' to nullable integer
    - Create 'total_sales' by summing regional sales
    """
    df_clean = df.copy()
    
    # 1. Normalize column names to lowercase
    df_clean.columns = df_clean.columns.str.lower()
    
    # 2. Handle missing values and adjust data types
    if 'user_score' in df_clean.columns:
        # Replace 'tbd' (to be determined) with NaN
        df_clean['user_score'] = df_clean['user_score'].replace('tbd', np.nan)
        # Convert to numeric (float)
        df_clean['user_score'] = pd.to_numeric(df_clean['user_score'])
        
    if 'year_of_release' in df_clean.columns:
        # Use pandas nullable integer to preserve missing values
        df_clean['year_of_release'] = df_clean['year_of_release'].astype('Int64')
        
    # 3. Create total sales feature
    sales_cols = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales']
    if all(col in df_clean.columns for col in sales_cols):
        df_clean['total_sales'] = df_clean[sales_cols].sum(axis=1)
        
    return df_clean