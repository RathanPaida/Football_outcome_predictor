# Football Outcome Predictor AI ⚽🤖

A full-stack, machine learning-powered application that predicts the outcome and exact score of international football (soccer) matches. It uses historical match data, dynamic Elo ratings, and advanced form metrics to train XGBoost models, serving predictions via a fast API and a premium, modern web interface.

## ✨ Features

- **Win Probability Predictions**: Calculates the exact percentage chance for a Home Win, Draw, or Away Win using a calibrated XGBoost Classifier.
- **Exact Score Predictions**: Estimates the exact final score (e.g., 2-1) using specialized XGBoost Poisson Regressors.
- **Advanced Feature Engineering**: Dynamically calculates Elo ratings, attacking/defensive form averages, and penalty threats over time for any international team.
- **Premium User Interface**: A beautifully crafted dark-mode frontend featuring glassmorphism, smooth animations, and glowing gradients built with Next.js and Tailwind CSS.
- **FastAPI Backend**: A lightweight, high-performance Python backend that serves model inferences instantly.
- **Automated ML Pipeline**: A complete end-to-end data pipeline (`src/pipeline.py`) that processes raw data, engineers features, tunes hyperparameters with Optuna, and trains the models.

## 🛠️ Technology Stack

- **Machine Learning**: XGBoost, Scikit-Learn, Optuna, Pandas, NumPy
- **Backend API**: FastAPI, Uvicorn
- **Frontend App**: Next.js, React, Tailwind CSS
- **Data**: Historical international football match datasets

## 📁 Project Structure

```text
football-outcome-predictor/
├── data/                   # Datasets (raw CSVs and processed features)
├── frontend/               # Next.js React frontend web application
├── models/                 # Serialized XGBoost models (.json)
├── notebooks/              # Jupyter notebooks for data exploration
├── src/                    # Backend API & ML Pipeline source code
│   ├── app.py              # FastAPI application & endpoints
│   ├── data_ingestion.py   # Scripts to load and clean raw datasets
│   ├── features.py         # Advanced feature engineering (Elo, form)
│   ├── pipeline.py         # Master script to run the full ML pipeline
│   └── train.py            # Model training and Optuna optimization logic
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.8+ and Node.js installed on your machine.

### 2. Setup the Machine Learning Backend

1. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Re-train the models using the latest data:
   ```bash
   python src/pipeline.py
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn src.app:app --reload --port 8000
   ```
   *The API will be available at `http://localhost:8000`*

### 3. Setup the Frontend UI

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the Node dependencies:
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
   *The web application will be available at `http://localhost:3000`*

## 🧠 How the AI Works

The AI relies heavily on engineered historical data rather than raw stats. Before a prediction is made, the pipeline simulates history chronologically to compute:
- **Elo Ratings**: Adjusting team strength based on the caliber of their opponents and match importance (e.g., World Cup vs. Friendlies).
- **Recent Form**: Tracking goals scored/conceded and match points over a trailing 5-match window.
- **Penalty Threat**: Factoring in a team's historical success rate in penalty shootouts.

These features are fed into three distinct XGBoost models:
1. `football_model.json`: An `XGBClassifier` (Softprob) predicting outcome likelihoods.
2. `home_score_model.json`: An `XGBRegressor` (Poisson) predicting the home team's goal count.
3. `away_score_model.json`: An `XGBRegressor` (Poisson) predicting the away team's goal count.
