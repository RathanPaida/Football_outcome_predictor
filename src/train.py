import xgboost as xgb
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_production_model(df, output_dir='models'):
    """Splits data cleanly by timeline, trains XGBoost, and exports weights."""
    # Features selected for predicting outcome before kickoff
    feature_cols = ['home_elo', 'away_elo', 'elo_diff', 'home_recent_form', 'away_recent_form', 'is_neutral']
    
    # Time-based train/test splits
    train_df = df[df['date'].dt.year < 2021]
    test_df = df[df['date'].dt.year >= 2021]
    
    X_train, y_train = train_df[feature_cols], train_df['outcome']
    X_test, y_test = test_df[feature_cols], test_df['outcome']
    
    print(f"Training size: {X_train.shape[0]} matches | Test size: {X_test.shape[0]} matches")
    
    # Initialize multi-class XGBoost model architecture
    model = xgb.XGBClassifier(
        n_estimators=150,
        max_depth=5,
        learning_rate=0.05,
        objective='multi:softprob',
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate performance
    preds = model.predict(X_test)
    print("\n--- Production Model Evaluation (Post-2021 Matches) ---")
    print(classification_report(y_test, preds, target_names=['Away Win', 'Draw', 'Home Win']))
    
    # Save model artifacts safely
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'football_model.json')
    model.save_model(model_path)
    print(f"Production model successfully compiled and written to: {model_path}")
    
    return model