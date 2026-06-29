from src.data_ingestion import load_and_clean_data
from src.features import compute_elo_and_history
from src.train import train_production_model
import os

def execute_full_pipeline():
    print("[1/3] Sourcing data entries & cleansing attributes...")
    raw_data = load_and_clean_data()
    
    print("[2/3] Transforming historical features and Elo metrics...")
    engineered_data = compute_elo_and_history(raw_data)
    
    # Save a checkpoint of the processed data
    processed_path = 'data/processed/engineered_matches.csv'
    engineered_data.to_csv(processed_path, index=False)
    print(f"Engineered data backed up at: {processed_path}")
    
    print("[3/3] Training model parameters...")
    model = train_production_model(engineered_data)
    print("\nPipeline Execution Cycle Complete.")

if __name__ == "__main__":
    execute_full_pipeline()