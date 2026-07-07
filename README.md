# AI Football Outcome Predictor (World Cup 2026 Edition)

An advanced, production-ready web application that predicts international football match outcomes using XGBoost and the Google Gemini AI.

## Features

- **XGBoost Match Predictor:** Predicts Home Win, Draw, Away Win probabilities and exact scorelines using historical Elo ratings, form, and attack/defense metrics.
- **Dynamic Gemini AI Tactics Engine:** Replaces hardcoded databases by dynamically asking Google Gemini to calculate the absolute optimal tactical formation based on opponent stats, and then perfectly generating the 11-man squad for any country in the world.
- **Gemini AI Pundit Explanations:** Takes the mathematical SHAP feature impact values and feeds them into Gemini to generate human-readable, rich pundit analysis of the match.
- **Premium React Frontend:** A vibrant, highly responsive UI featuring a dynamic CSS visual football pitch that maps players exactly to their generated tactical formations.
- **Automated Web Scraping:** Integrates the Wikipedia Action API to automatically pull high-resolution photos of active players in real-time.

## Tech Stack
- **Backend**: FastAPI (Python), XGBoost, SHAP, Google Generative AI SDK, Pandas
- **Frontend**: Next.js, React, Tailwind CSS (Vibrant World Cup Theme)

## Setup & Run

### 1. Backend
Ensure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
uvicorn src.app:app --reload --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to interact with the application.

## System Architecture & Production Readiness

This application has been architected following modern enterprise and cloud-native standards:

- **Stateless Architecture:** The FastAPI backend (`app.py`), the XGBoost ML Engine, and the Gemini AI modules (`tactics.py`, `explainer.py`) are completely stateless. No session data is stored in memory, allowing for infinite horizontal scaling behind a load balancer.
- **API Rate Limiting:** Implemented `SlowAPI` to strictly rate-limit endpoints (e.g., `30 requests/minute` for predictions) to prevent malicious scraping, DDoS attacks, and uncontrolled LLM API billing spikes.
- **Structured Telemetry & Logging:** Replaced standard print statements with Python's `logging` module to output standardized timestamps, severities, and source modules, fully compatible with cloud monitoring solutions like Datadog or AWS CloudWatch.
- **Environment Isolation:** Secrets and API keys are securely decoupled from the source code via `python-dotenv` `.env` files.

### Future Scalability & Latency Optimization
- **Redis Caching**: To drastically reduce the ~2 second LLM generation latency, future implementations can cache identical Gemini JSON responses (e.g., "France vs Argentina tactics") in a Redis cluster, returning cached data to subsequent users in <20ms.
- **Containerization**: A `Dockerfile` is included for seamless containerization and deployment to Kubernetes (K8s) or Google Cloud Run.
