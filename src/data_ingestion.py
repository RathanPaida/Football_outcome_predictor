import pandas as pd
import os

def load_all_data(raw_dir='data/raw'):
    """Loads and formats results, shootouts, and goalscorers."""
    df_results = pd.read_csv(os.path.join(raw_dir, 'results.csv'))
    df_shootouts = pd.read_csv(os.path.join(raw_dir, 'shootouts.csv'))
    df_scorers = pd.read_csv(os.path.join(raw_dir, 'goalscorers.csv'))
    
    # Format dates
    for df in [df_results, df_shootouts, df_scorers]:
        df['date'] = pd.to_datetime(df['date'])
        
    # Sort chronological
    df_results = df_results.sort_values('date').reset_index(drop=True)
    
    # Target variable
    def determine_outcome(row):
        if row['home_score'] > row['away_score']: return 2
        elif row['home_score'] == row['away_score']: return 1
        else: return 0
            
    df_results['outcome'] = df_results.apply(determine_outcome, axis=1)
    
    return df_results, df_shootouts, df_scorers