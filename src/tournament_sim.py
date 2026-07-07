import json
import os
import random
import numpy as np
import xgboost as xgb

class TournamentSimulator:
    def __init__(self, model, team_stats, data_dir='data/raw'):
        self.model = model
        self.team_stats = team_stats
        self.structure_path = os.path.join(data_dir, 'tournament_structure.json')
        
        # Load real structure if exists, else use default mock
        if os.path.exists(self.structure_path):
            try:
                with open(self.structure_path, 'r') as f:
                    self.structure = json.load(f)
            except Exception:
                self.structure = self._get_mock_structure()
        else:
            self.structure = self._get_mock_structure()

    def _get_mock_structure(self):
        """Mock knockout bracket for 16 teams"""
        return {
            "Round of 16": [
                ["Argentina", "Australia"], ["Netherlands", "USA"],
                ["France", "Poland"], ["England", "Senegal"],
                ["Japan", "Croatia"], ["Brazil", "South Korea"],
                ["Morocco", "Spain"], ["Portugal", "Switzerland"]
            ]
        }

    def _predict_match(self, home_team, away_team):
        if home_team not in self.team_stats or away_team not in self.team_stats:
            # Fallback if team not in our DB
            return 0.5, 0.5
            
        h = self.team_stats[home_team]
        a = self.team_stats[away_team]
        
        # We need the exact features format
        features = np.array([[
            h['elo'], a['elo'], h['elo'] - a['elo'],
            h['attack'], h['defense'], a['attack'], a['defense'],
            h['form'], a['form'], h['penalty_threat'], a['penalty_threat'], 1 # neutral ground
        ]])
        
        feature_names = [
            'home_elo', 'away_elo', 'elo_diff',
            'home_attack_avg', 'home_defense_avg', 'away_attack_avg', 'away_defense_avg',
            'home_recent_form', 'away_recent_form', 'home_penalty_threat', 'away_penalty_threat', 'is_neutral'
        ]
        
        dmatrix = xgb.DMatrix(features, feature_names=feature_names)
        probs = self.model.predict(dmatrix)[0]
        
        # XGBoost Softprob: [Away Win, Draw, Home Win]
        # In knockout, a draw goes to pens, split it 50/50
        home_win_prob = probs[2] + (probs[1] / 2)
        away_win_prob = probs[0] + (probs[1] / 2)
        
        return home_win_prob, away_win_prob

    def simulate_path(self, target_team, iterations=1000):
        """
        Runs Monte Carlo simulation of the target team's path through the tournament.
        """
        # Find which bracket the team is in
        start_match = None
        for match in self.structure.get("Round of 16", []):
            if target_team in match:
                start_match = match
                break
                
        if not start_match:
            return {"error": f"Team {target_team} not found in the tournament bracket."}

        # Initialize tracking
        path_results = {
            "Round of 16": {"reached": 0, "opponents": {}},
            "Quarter-finals": {"reached": 0, "opponents": {}},
            "Semi-finals": {"reached": 0, "opponents": {}},
            "Final": {"reached": 0, "opponents": {}},
            "Winner": {"reached": 0, "opponents": {}}
        }
        
        # Simulate 'iterations' times
        for _ in range(iterations):
            current_team = target_team
            
            # Simple bracket simulation logic
            # In a real app with full json, we traverse the exact tree.
            # Here we simulate sequential generic stages against random strong opponents 
            # to illustrate the Monte Carlo approach if the json is simple.
            
            stages = ["Round of 16", "Quarter-finals", "Semi-finals", "Final"]
            
            # Mock potential strong opponents
            pool = ["Brazil", "France", "Argentina", "England", "Spain", "Portugal", "Germany", "Netherlands"]
            if current_team in pool:
                pool.remove(current_team)
                
            for stage in stages:
                path_results[stage]["reached"] += 1
                
                # Pick opponent
                opponent = random.choice(pool)
                
                # Track likely opponent
                if opponent not in path_results[stage]["opponents"]:
                    path_results[stage]["opponents"][opponent] = 0
                path_results[stage]["opponents"][opponent] += 1
                
                home_p, away_p = self._predict_match(current_team, opponent)
                
                # Roll dice
                if random.random() < home_p:
                    # Win and progress
                    pass
                else:
                    # Lose and exit
                    break
            else:
                # If they survived all stages
                path_results["Winner"]["reached"] += 1

        # Format results
        final_path = {}
        for stage, data in path_results.items():
            prob = (data["reached"] / iterations) * 100
            if prob == 0:
                continue
                
            most_likely_opp = None
            if data["opponents"]:
                most_likely_opp = max(data["opponents"], key=data["opponents"].get)
                
            final_path[stage] = {
                "probability_to_reach_stage": round(prob, 2),
                "most_likely_opponent": most_likely_opp,
                "difficulty": "Extreme" if prob < 30 else "Moderate"
            }
            
        return {
            "team": target_team,
            "tournament_path": final_path,
            "simulations_run": iterations
        }
