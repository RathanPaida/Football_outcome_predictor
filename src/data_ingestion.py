import pandas as pd
import os

def load_and_clean_data(raw_dir='data/raw'):
    """Loads results.csv and formats core temporal and categorical parameters."""
    results_path = os.path.join(raw_dir, 'results.csv')
    if not os.path.exists(results_path):
        raise FileNotFoundError(f"Could not find results.csv in {raw_dir}")
        
    df = pd.read_csv(results_path)
    
    # Format date and sort chronologically to prevent data leakage
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    
    # Create our target variable: 2 = Home Win, 1 = Draw, 0 = Away Win
    def determine_outcome(row):
        if row['home_score'] > row['away_score']:
            return 2
        elif row['home_score'] == row['away_score']:
            return 1
        else:
            return 0
            
    df['outcome'] = df.apply(determine_outcome, axis=1)
    return df

if __name__ == "__main__":
    df = load_and_clean_data()
    print(f"Data ingested successfully. Shape: {df.shape}")