import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import optuna
import os

def train_production_model(df, output_dir='models'):
    feature_cols = [
        'home_elo', 'away_elo', 'elo_diff', 
        'home_attack_avg', 'home_defense_avg',
        'away_attack_avg', 'away_defense_avg',
        'home_recent_form', 'away_recent_form',
        'home_penalty_threat', 'away_penalty_threat', # <-- The missing pieces!
        'is_neutral'
    ]
    
    train_df = df[df['date'].dt.year < 2021]
    test_df = df[df['date'].dt.year >= 2021]
    
    X_train, y_train = train_df[feature_cols], train_df['outcome']
    X_test, y_test = test_df[feature_cols], test_df['outcome']
    
    classes = np.unique(y_train)
    weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
    sample_weights = y_train.map(dict(zip(classes, weights)))

    print("Initiating Optuna Bayesian Hyperparameter Search...")

    def objective(trial):
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 100, 400),
            'max_depth': trial.suggest_int('max_depth', 3, 6),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.1, log=True),
            'subsample': trial.suggest_float('subsample', 0.6, 0.9),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 0.9),
            'objective': 'multi:softprob',
            'random_state': 42
        }
        
        opt_model = xgb.XGBClassifier(**params)
        opt_model.fit(X_train, y_train, sample_weight=sample_weights, verbose=False)
        preds = opt_model.predict(X_test)
        return accuracy_score(y_test, preds)

    # Run 20 search trials to find the optimum
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=20)
    
    print("\nBest Hyperparameters Found:", study.best_params)
    
    # Train final model with the absolute best parameters
    best_params = study.best_params
    best_params['objective'] = 'multi:softprob'
    best_params['random_state'] = 42
    
    final_model = xgb.XGBClassifier(**best_params)
    final_model.fit(X_train, y_train, sample_weight=sample_weights)
    
    # Evaluate
    final_preds = final_model.predict(X_test)
    print("\n--- Ultimate Model Evaluation ---")
    print(classification_report(y_test, final_preds, target_names=['Away Win', 'Draw', 'Home Win']))
    
    # Plot Feature Importances to understand model logic
    os.makedirs(output_dir, exist_ok=True)
    importances = pd.Series(final_model.feature_importances_, index=feature_cols).sort_values(ascending=True)
    plt.figure(figsize=(10, 6))
    importances.plot(kind='barh', color='#007bff')
    plt.title('XGBoost Feature Importances (What drives the predictions?)')
    plt.xlabel('F-Score / Weight')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_importance.png'))
    print(f"Feature importance chart saved to: {os.path.join(output_dir, 'feature_importance.png')}")

    # Save model
    model_path = os.path.join(output_dir, 'football_model.json')
    final_model.save_model(model_path)
    
    return final_model

def train_score_models(df, output_dir='models'):
    print("\nTraining Score Prediction Models (Poisson Regression)...")
    feature_cols = [
        'home_elo', 'away_elo', 'elo_diff', 
        'home_attack_avg', 'home_defense_avg',
        'away_attack_avg', 'away_defense_avg',
        'home_recent_form', 'away_recent_form',
        'home_penalty_threat', 'away_penalty_threat',
        'is_neutral'
    ]
    
    train_df = df[df['date'].dt.year < 2021]
    
    X_train = train_df[feature_cols]
    y_home = train_df['home_score']
    y_away = train_df['away_score']
    
    # We use count:poisson for predicting count variables like goals
    params = {
        'objective': 'count:poisson',
        'n_estimators': 150,
        'learning_rate': 0.05,
        'max_depth': 4,
        'random_state': 42
    }
    
    home_model = xgb.XGBRegressor(**params)
    home_model.fit(X_train, y_home)
    
    away_model = xgb.XGBRegressor(**params)
    away_model.fit(X_train, y_away)
    
    os.makedirs(output_dir, exist_ok=True)
    home_model.save_model(os.path.join(output_dir, 'home_score_model.json'))
    away_model.save_model(os.path.join(output_dir, 'away_score_model.json'))
    print(f"Score models saved to {output_dir}/home_score_model.json and away_score_model.json")
    
    return home_model, away_model