from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import xgboost as xgb
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Football Predictor API")

# --- CORS Configuration: Essential for React to talk to FastAPI ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

model = None
home_score_model = None
away_score_model = None
team_stats = {}
teams_list = []

@app.on_event("startup")
def load_assets():
    global model, home_score_model, away_score_model, team_stats, teams_list
    model = xgb.Booster()
    model.load_model(os.path.join("models", "football_model.json"))
    
    home_score_model = xgb.Booster()
    home_score_model.load_model(os.path.join("models", "home_score_model.json"))
    
    away_score_model = xgb.Booster()
    away_score_model.load_model(os.path.join("models", "away_score_model.json"))
    
    df = pd.read_csv(os.path.join("data", "processed", "engineered_matches.csv"))
    
    for team in pd.concat([df['home_team'], df['away_team']]).unique():
        last_match = df[(df['home_team'] == team) | (df['away_team'] == team)].iloc[-1]
        if last_match['home_team'] == team:
            team_stats[team] = {
                'elo': last_match['home_elo'],
                'attack': last_match['home_attack_avg'],
                'defense': last_match['home_defense_avg'],
                'form': last_match['home_recent_form'],
                'penalty_threat': last_match['home_penalty_threat']
            }
        else:
            team_stats[team] = {
                'elo': last_match['away_elo'],
                'attack': last_match['away_attack_avg'],
                'defense': last_match['away_defense_avg'],
                'form': last_match['away_recent_form'],
                'penalty_threat': last_match['away_penalty_threat']
            }
    teams_list = sorted(list(team_stats.keys()))

@app.get("/teams")
async def get_teams():
    return {"teams": teams_list}

@app.post("/predict")
async def predict_match(
    home_team: str = Form(...),
    away_team: str = Form(...),
    is_neutral: int = Form(0)
):
    if home_team not in team_stats or away_team not in team_stats:
        return {"error": "Team not found."}

    h = team_stats[home_team]
    a = team_stats[away_team]
    
    features = np.array([[
        h['elo'], a['elo'], h['elo'] - a['elo'],
        h['attack'], h['defense'], a['attack'], a['defense'],
        h['form'], a['form'], h['penalty_threat'], a['penalty_threat'], is_neutral
    ]])
    
    feature_names = [
        'home_elo', 'away_elo', 'elo_diff',
        'home_attack_avg', 'home_defense_avg', 'away_attack_avg', 'away_defense_avg',
        'home_recent_form', 'away_recent_form', 'home_penalty_threat', 'away_penalty_threat', 'is_neutral'
    ]
    dmatrix = xgb.DMatrix(features, feature_names=feature_names)
    probs = model.predict(dmatrix)[0]
    
    home_score_pred = home_score_model.predict(dmatrix)[0]
    away_score_pred = away_score_model.predict(dmatrix)[0]
    
    return {
        "home_team": home_team, "away_team": away_team,
        "home_win_prob": round(float(probs[2]) * 100, 2),
        "draw_prob": round(float(probs[1]) * 100, 2),
        "away_win_prob": round(float(probs[0]) * 100, 2),
        "predicted_home_score": int(round(float(home_score_pred))),
        "predicted_away_score": int(round(float(away_score_pred)))
    }