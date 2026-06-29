import pandas as pd
import numpy as np

def get_tournament_weight(tournament):
    t_lower = tournament.lower()
    if 'fifa world cup' in t_lower and 'qualification' not in t_lower: return 60
    elif 'qualification' in t_lower or 'euro' in t_lower or 'copa américa' in t_lower: return 40
    elif 'friendly' in t_lower: return 16
    return 25

def compute_elo_and_history(df, df_shootouts, df_scorers, initial_elo=1500):
    
    # --- 1. Pre-compute O(1) Hash Maps for Performance ---
    print("Pre-computing shootout and goalscorer hash maps...")
    
    # Shootout Map: (date, home, away) -> winner_name
    shootout_map = {}
    for _, row in df_shootouts.iterrows():
        key = (row['date'], row['home_team'], row['away_team'])
        shootout_map[key] = row['winner']
        
    # Penalty Map: (date, home, away) -> {'home_pens': int, 'away_pens': int}
    # We only care about goals marked as penalties
    pens_only = df_scorers[df_scorers['penalty'] == True]
    penalty_map = {}
    for name, group in pens_only.groupby(['date', 'home_team', 'away_team']):
        home_pens = len(group[group['team'] == name[1]])
        away_pens = len(group[group['team'] == name[2]])
        penalty_map[name] = {'home_pens': home_pens, 'away_pens': away_pens}

    # --- 2. Initialize Tracking Variables ---
    elo_dict = {}
    team_history = {} 
    
    home_elos, away_elos = [], []
    h_attack, a_attack = [], []
    h_defense, a_defense = [], []
    h_form, a_form = [], []
    h_pen_threat, a_pen_threat = [], []
    
    # --- 3. The Main Historical Loop ---
    for idx, row in df.iterrows():
        home = row['home_team']
        away = row['away_team']
        date = row['date']
        match_key = (date, home, away)
        
        h_elo = elo_dict.get(home, initial_elo)
        a_elo = elo_dict.get(away, initial_elo)
        home_elos.append(h_elo)
        away_elos.append(a_elo)
        
        # Extract rolling forms (including new penalty threat)
        for team, att_list, def_list, form_list, pen_list in [
            (home, h_attack, h_defense, h_form, h_pen_threat), 
            (away, a_attack, a_defense, a_form, a_pen_threat)
        ]:
            history = team_history.get(team, [])
            if not history:
                att_list.append(1.0); def_list.append(1.0); form_list.append(0.33); pen_list.append(0.0)
            else:
                recent = history[-5:]
                att_list.append(np.mean([m['gf'] for m in recent]))
                def_list.append(np.mean([m['ga'] for m in recent]))
                form_list.append(np.mean([m['points'] for m in recent]))
                pen_list.append(np.mean([m['pens'] for m in recent]))
                
        # Base Points
        if row['outcome'] == 2: s_h, s_a = 1.0, 0.0
        elif row['outcome'] == 1: s_h, s_a = 0.5, 0.5
        else: s_h, s_a = 0.0, 1.0
            
        # SHOOTOUT OVERRIDE: If it was a draw, check if a shootout occurred
        if row['outcome'] == 1 and match_key in shootout_map:
            winner = shootout_map[match_key]
            if winner == home:
                s_h, s_a = 0.75, 0.25  # Home won on penalties
            elif winner == away:
                s_h, s_a = 0.25, 0.75  # Away won on penalties
                
        # Check penalties scored in this match
        match_pens = penalty_map.get(match_key, {'home_pens': 0, 'away_pens': 0})
            
        # Update Elos
        exp_h = 1 / (1 + 10 ** ((a_elo - h_elo) / 400))
        exp_a = 1 / (1 + 10 ** ((h_elo - a_elo) / 400))
        k = get_tournament_weight(row['tournament'])
        
        elo_dict[home] = h_elo + k * (s_h - exp_h)
        elo_dict[away] = a_elo + k * (s_a - exp_a)
        
        # Save to memory buffer
        if home not in team_history: team_history[home] = []
        if away not in team_history: team_history[away] = []
        
        team_history[home].append({'points': s_h, 'gf': row['home_score'], 'ga': row['away_score'], 'pens': match_pens['home_pens']})
        team_history[away].append({'points': s_a, 'gf': row['away_score'], 'ga': row['home_score'], 'pens': match_pens['away_pens']})
        
    # Append to DataFrame
    df['home_elo'] = home_elos
    df['away_elo'] = away_elos
    df['elo_diff'] = df['home_elo'] - df['away_elo']
    df['home_attack_avg'] = h_attack
    df['home_defense_avg'] = h_defense
    df['away_attack_avg'] = a_attack
    df['away_defense_avg'] = a_defense
    df['home_recent_form'] = h_form
    df['away_recent_form'] = a_form
    df['home_penalty_threat'] = h_pen_threat
    df['away_penalty_threat'] = a_pen_threat
    df['is_neutral'] = df['neutral'].astype(int)
    
    return df