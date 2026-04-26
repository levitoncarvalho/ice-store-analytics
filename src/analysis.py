import pandas as pd

def filter_relevant_period(df, start_year=2014):
    # Filter the data to keep only records from `start_year` onward.
    return df[df['year_of_release'] >= start_year].copy()

def get_top_platforms_by_region(df, region_col, top_n=5):
    # Return the top `top_n` platforms by total sales in a given region.
    return df.groupby('platform')[region_col].sum().sort_values(ascending=False).head(top_n)