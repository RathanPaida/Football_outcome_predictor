import pandas as pd
import numpy as np

def compute_elo_and_history(df, k_factor=32, initial_elo=1500):
    """
    Computes chronological Elo ratings and rolling team statistics 
    without introducing temporal data leakage.
    """
    elo_dict = {}
    
    # Tracking variables for rolling metrics
    team_history = {} # Maps team -> list of outcomes, goals, etc.
    
    home_elos = []
    away_elos = []
    home_form = []
    away_form = []
    
    for idx, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']
        
        # 1. Fetch current Elo ratings or initialize them
        h_elo = elo_dict.get(home, initial_elo)
        a_elo = elo_dict.get(away, initial_elo)
        
        home_elos.append(h_elo)
        away_elos.append(a_elo)
        
        # 2. Extract recent rolling form (Win rate of last 5 games)
        for team, elo_list in [(home, home_form), (away, away_form)]:
            history = team_history.get(team, [])
            if len(history) == 0:
                elo_list.append(0.33) # Baseline default neutral form
            else:
                # Average score points from recent 5 matches
                elo_list.append(np.mean(history[-5:]))
        
        # 3. Calculate actual outcomes for updating Elo
        if row['outcome'] == 2:
            s_h, s_a = 1.0, 0.0
        elif row['outcome'] == 1:
            s_h, s_a = 0.5, 0.5
        else:
            s_h, s_a = 0.0, 1.0
            
        # 4. Compute Expected Outcomes via Elo formula
        exp_h = 1 / (1 + 10 ** ((a_elo - h_elo) / 400))
        exp_a = 1 / (1 + 10 ** ((h_elo - a_elo) / 400))
        
        # 5. Save updates back to database
        elo_dict[home] = h_elo + k_factor * (s_h - exp_h)
        elo_dict[away] = a_elo + k_factor * (s_a - exp_a)
        
        # 6. Push match result into individual team rolling memory histories
        if home not in team_history: team_history[home] = []
        if away not in team_history: team_history[away] = []
        team_history[home].append(s_h)
        team_history[away].append(s_a)
        
    df['home_elo'] = home_elos
    df['away_elo'] = away_elos
    df['elo_diff'] = df['home_elo'] - df['away_elo']
    df['home_recent_form'] = home_form
    df['away_recent_form'] = away_form
    
    # Binary code standard categoricals
    df['is_neutral'] = df['neutral'].astype(int)
    
    return df