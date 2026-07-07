import shap
import numpy as np
import xgboost as xgb
import os
import google.generativeai as genai

class PredictionExplainer:
    """
    Generates human-readable tactical explanations for match predictions 
    using SHAP (SHapley Additive exPlanations) values and Gemini API punditry.
    """
    def __init__(self, model: xgb.Booster, feature_names: list):
        self.model = model
        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(self.model)
        
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            self.gemini = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.gemini = None

    def generate_explanation(self, features_array: np.ndarray, home_team: str, away_team: str) -> dict:
        """
        Calculates SHAP values and feeds them into Gemini to generate a brilliant pundit explanation.
        """
        shap_values = self.explainer.shap_values(features_array)
        
        if isinstance(shap_values, list):
            home_win_shap = shap_values[2][0]
        else:
            if len(shap_values.shape) == 3:
                home_win_shap = shap_values[0, :, 2]
            else:
                home_win_shap = shap_values[0]

        home_win_shap = np.array(home_win_shap).flatten()

        feature_contributions = []
        for i, name in enumerate(self.feature_names):
            val = float(home_win_shap[i])
            feature_contributions.append({
                'feature': name,
                'shap_impact': val,
                'actual_value': features_array[0][i]
            })

        feature_contributions.sort(key=lambda x: abs(x['shap_impact']), reverse=True)
        top_factors = feature_contributions[:4]
        
        # Format factors for prompt
        factor_str = ", ".join([f"{f['feature']} (impact: {f['shap_impact']:.2f})" for f in top_factors])
        primary_team = home_team if top_factors[0]['shap_impact'] > 0 else away_team

        if self.gemini:
            prompt = f"""
            Act as an expert football pundit and data analyst.
            You are analyzing an upcoming match between {home_team} (Home) and {away_team} (Away).
            
            Our AI model has analyzed this match. The most heavily weighted factors driving this prediction are:
            {factor_str}. 
            (Note: A positive impact heavily favors the home team, negative favors the away team).
            
            Write a brilliant, exciting, 2-paragraph pundit analysis explaining exactly why the AI predicts that outcome, based on these metrics. 
            Do NOT mention 'SHAP values' or 'impact numbers' explicitly, just talk about the teams' strengths like Elo rankings, attack, defense, or form.
            Make it read like a premium sports article.
            """
            
            try:
                response = self.gemini.generate_content(prompt)
                return {
                    "top_features": [f['feature'] for f in top_factors],
                    "text_explanation": response.text.strip()
                }
            except Exception as e:
                print(f"Gemini Pundit failed: {e}")

        # Fallback
        return {
            "top_features": [f['feature'] for f in top_factors],
            "text_explanation": f"Based on our statistical analysis, the primary deciding factors in this match will be {top_factors[0]['feature']} and {top_factors[1]['feature']}, which largely favor {primary_team}. Set GEMINI_API_KEY to enable AI-powered pundit explanations."
        }
