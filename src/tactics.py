import os
import json
import random
import google.generativeai as genai

class TacticalEngine:
    """
    Recommends opponent-specific Starting XIs and formations based on historical
    data and opponent strengths/weaknesses. Uses Google Gemini API for ultimate dynamic squads.
    """
    def __init__(self, data_dir='data/raw'):
        api_key = os.environ.get("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-flash-latest')
        else:
            self.model = None

    def _generate_generic_fallback(self, team, formation):
        """Fallback if Gemini API Key is missing or fails."""
        base_names = ["Silva", "Santos", "Garcia", "Martinez", "Muller", "Rossi", "Kim", "Smith", "Johnson", "Ali", "Khan", "Alvarez"]
        layers = [int(x) for x in formation.split('-')]
        
        starting_xi = []
        starting_xi.append(f"{chr(65 + random.randint(0,25))}. {random.choice(base_names)} (GK)")
        
        positions = ["DEF", "MID", "ATT"]
        for i, count in enumerate([layers[0], sum(layers[1:-1]), layers[-1]]):
            for _ in range(count):
                starting_xi.append(f"{chr(65 + random.randint(0,25))}. {random.choice(base_names)} ({positions[i]})")
                
        return starting_xi

    def generate_starting_xi(self, team: str, opponent: str, team_stats: dict, opponent_stats: dict) -> dict:
        """
        Generates the tactical approach and Starting XI tailored specifically against the opponent.
        """
        # 1. Determine Tactical Formation Rules
        team_att = team_stats.get('attack', 1.0)
        team_def = team_stats.get('defense', 1.0)
        opp_att = opponent_stats.get('attack', 1.0)
        opp_def = opponent_stats.get('defense', 1.0)
        
        # 1. Ask Gemini for the Squad & Tactics!
        if self.model:
            prompt = f"""
            You are an elite football manager. You are managing {team} against {opponent}.
            
            Here are the statistics for this matchup:
            - {team} Attack Score: {team_att:.2f}, Defense Score: {team_def:.2f}, Form: {team_stats.get('form', 1.0):.2f}
            - {opponent} Attack Score: {opp_att:.2f}, Defense Score: {opp_def:.2f}, Form: {opponent_stats.get('form', 1.0):.2f}
            
            1. Analyze these stats and decide on the absolute optimal tactical formation (e.g., "4-3-3", "5-3-2", "4-2-3-1", "3-4-3") for {team} to counter {opponent}.
            2. Select the absolute best, most recent, active 11 players for {team} that fit this chosen formation perfectly.
            3. Provide a 2-sentence tactical explanation of why this formation and strategy beats {opponent}.
            
            IMPORTANT: You must return ONLY raw JSON matching this exact structure, with no markdown formatting or backticks:
            {{
                "formation": "4-3-3",
                "tactics": "Your 2 sentence explanation here...",
                "players": [
                    "Player Name (GK)",
                    "Player Name (DEF)",
                    "Player Name (DEF)",
                    "Player Name (MID)",
                    "Player Name (ATT)"
                    ... exactly 11 players formatted exactly like this with their broad position in parentheses
                ]
            }}
            """
            try:
                response = self.model.generate_content(prompt)
                raw_json = response.text.replace('```json', '').replace('```', '').strip()
                data = json.loads(raw_json)
                
                # Verify exactly 11 players
                if len(data.get("players", [])) == 11:
                    return {
                        "formation": data.get("formation", "4-3-3"),
                        "starting_xi": data["players"],
                        "tactical_explanation": {
                            "tactical_approach": data.get("tactics", "Balanced approach selected by AI."),
                            "strengths_exploited": "Dynamic based on stats",
                            "defensive_considerations": "Dynamic based on stats",
                            "key_player_instructions": "Focus on high intensity."
                        }
                    }
            except Exception as e:
                print(f"Gemini Tactical Engine failed: {e}")
                pass # Fallback below
                
        # 2. Fallback
        tactical_approach = f"Balanced control against {opponent}. Please set GEMINI_API_KEY environment variable for AI-generated dynamic squads."
        return {
            "formation": "4-3-3",
            "starting_xi": self._generate_generic_fallback(team, "4-3-3"),
            "tactical_explanation": {
                "tactical_approach": tactical_approach,
                "strengths_exploited": "N/A",
                "defensive_considerations": "N/A",
                "key_player_instructions": "Set GEMINI_API_KEY for dynamic tactical logic."
            }
        }
