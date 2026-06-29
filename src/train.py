import xgboost as xgb
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os

def train_production_model(df, output_dir='models'):
    """Trains an optimized XGBoost classifier using class weights and advanced features."""
    
    # Expanded high-fidelity predictive feature space
    feature_cols = [
        'home_elo', 'away_elo', 'elo_diff', 
        'home_attack_avg', 'home_defense_avg',
        'away_attack_avg', 'away_defense_avg',
        'home_recent_form', 'away_recent_form', 
        'is_neutral'
    ]
    
    # Chronological timeline split
    train_df = df[df['date'].dt.year < 2021]
    test_df = df[df['date'].dt.year >= 2021]
    
    X_train, y_train = train_df[feature_cols], train_df['outcome']
    X_test, y_test = test_df[feature_cols], test_df['outcome']
    
    # Compute class weights to address the Draw classification drop
    classes = np.unique(y_train)
    weights = compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
    class_weights_map = dict(zip(classes, weights))
    
    # Map raw training arrays to sample weights
    sample_weights = y_train.map(class_weights_map)
    
    print(f"Training on optimized dataset: {X_train.shape[0]} samples. Weight Map: {class_weights_map}")
    
    # Optimized Hyperparameters
    model = xgb.XGBClassifier(
        n_estimators=300,        # Increased trees for deeper exploration
        max_depth=4,             # Shallower trees limit overfitting
        learning_rate=0.02,      # Slower learning step minimizes variance
        subsample=0.8,           # Row sub-sampling introduces stochastic regularization
        colsample_bytree=0.8,    # Feature sub-sampling reduces tree cross-correlation
        objective='multi:softprob',
        random_state=42
    )
    
    # Fit model applying calculated sample weights
    model.fit(X_train, y_train, sample_weight=sample_weights)
    
    # Verify predictions
    preds = model.predict(X_test)
    print("\n--- Optimized Production Model Evaluation ---")
    print(classification_report(y_test, preds, target_names=['Away Win', 'Draw', 'Home Win']))
    
    # Serialize model artifact
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, 'football_model.json')
    model.save_model(model_path)
    print(f"Optimized model binary saved to: {model_path}")
    
    return model