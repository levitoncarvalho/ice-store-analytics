import pandas as pd
import os

# Get the absolute path to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'games.csv')

def load_data():
    # Load the raw dataset from the CSV file.
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {DATA_PATH}")
        return pd.DataFrame()