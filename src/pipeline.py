from src.data_ingestion import load_all_data
from src.features import compute_elo_and_history
from src.train import train_production_model, train_score_models

def execute_full_pipeline():
    print("[1/3] Sourcing data entries & cleansing attributes...")
    df_results, df_shootouts, df_scorers = load_all_data()
    
    print("[2/3] Transforming historical features and Elo metrics...")
    engineered_data = compute_elo_and_history(df_results, df_shootouts, df_scorers)
    
    processed_path = 'data/processed/engineered_matches.csv'
    engineered_data.to_csv(processed_path, index=False)
    
    print("[3/3] Training model parameters...")
    model = train_production_model(engineered_data)
    train_score_models(engineered_data)
    print("\nPipeline Execution Cycle Complete.")

if __name__ == "__main__":
    execute_full_pipeline()