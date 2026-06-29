import pandas as pd
import numpy as np

def get_tournament_weight(tournament):
    """Assigns an importance multiplier to a tournament type."""
    t_lower = tournament.lower()
    if 'fifa world cup' in t_lower and 'qualification' not in t_lower:
        return 60  # Highest weight for final tournaments
    elif 'qualification' in t_lower or 'uefa euro' in t_lower or 'copa américa' in t_lower or 'african cup of nations' in t_lower:
        return 40  # Continental championships and qualifiers
    elif 'friendly' in t_lower:
        return 16  # Low weight for friendlies
    return 25      # Standard baseline weight for minor tournaments

def compute_elo_and_history(df, initial_elo=1500):
    """
    Advanced engineering loop computing dynamic tournament-weighted Elos 
    and detailed offensive/defensive form signals.
    """
    elo_dict = {}
    team_history = {} # Maps team -> list of dicts {'points': x, 'gf': x, 'ga': x}
    
    # Feature columns array buffers
    home_elos, away_elos = [], []
    h_attack, a_attack = [], []
    h_defense, a_defense = [], []
    h_form, a_form = [], []
    
    for idx, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']
        h_score = row['home_score']
        a_score = row['away_score']
        
        # Fetch current Elo ratings
        h_elo = elo_dict.get(home, initial_elo)
        a_elo = elo_dict.get(away, initial_elo)
        home_elos.append(h_elo)
        away_elos.append(a_elo)
        
        # Extract advanced metrics from historical performance windows
        for team, att_list, def_list, form_list in [
            (home, h_attack, h_defense, h_form), 
            (away, a_attack, a_defense, a_form)
        ]:
            history = team_history.get(team, [])
            if not history:
                att_list.append(1.0)   # Default average baseline goals
                def_list.append(1.0)   # Default average baseline conceded
                form_list.append(0.33) # Balanced baseline form points
            else:
                recent = history[-5:]  # Lookback window of 5 matches
                att_list.append(np.mean([m['gf'] for m in recent]))
                def_list.append(np.mean([m['ga'] for m in recent]))
                form_list.append(np.mean([m['points'] for m in recent]))
                
        # Calculate matching outcomes and point weights
        if row['outcome'] == 2:
            s_h, s_a = 1.0, 0.0
        elif row['outcome'] == 1:
            s_h, s_a = 0.5, 0.5
        else:
            s_h, s_a = 0.0, 1.0
            
        exp_h = 1 / (1 + 10 ** ((a_elo - h_elo) / 400))
        exp_a = 1 / (1 + 10 ** ((h_elo - a_elo) / 400))
        
        # Calculate dynamic dynamic dynamic K factor based on tournament structure
        k = get_tournament_weight(row['tournament'])
        
        # Update state dictionary database
        elo_dict[home] = h_elo + k * (s_h - exp_h)
        elo_dict[away] = a_elo + k * (s_a - exp_a)
        
        # Cache updates back into individual running memory arrays
        if home not in team_history: team_history[home] = []
        if away not in team_history: team_history[away] = []
        
        team_history[home].append({'points': s_h, 'gf': h_score, 'ga': a_score})
        team_history[away].append({'points': s_a, 'gf': a_score, 'ga': h_score})
        
    df['home_elo'] = home_elos
    df['away_elo'] = away_elos
    df['elo_diff'] = df['home_elo'] - df['away_elo']
    df['home_attack_avg'] = h_attack
    df['home_defense_avg'] = h_defense
    df['away_attack_avg'] = a_attack
    df['away_defense_avg'] = a_defense
    df['home_recent_form'] = h_form
    df['away_recent_form'] = a_form
    df['is_neutral'] = df['neutral'].astype(int)
    
    return df