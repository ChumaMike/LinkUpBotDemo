import os
import google.generativeai as genai
import json
from src.services.ai_service import ai_brain

class AIService:
    def __init__(self):
        # Configure the API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        
        # We use 'gemini-pro' for text analysis
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def parse_intent(self, user_text):
        """
        Uses LLM to understand what the user wants.
        Returns a JSON object: {'intent': 'search', 'category': 'plumber', 'location': 'soweto'}
        """
        try:
            # The Magic Prompt: Forces structured JSON output
            prompt = f"""
            You are the brain of a WhatsApp bot.
            Analyze: "{user_text}"
            
            Rules:
            1. 'intent': 'search_listings', 'weather', 'greeting', 'unknown'.
            2. If 'search_listings', extract 'category' (plumber, job, etc) and 'location'.
            3. IMPORTANT: If NO location is mentioned, set 'location' to "Soweto" (Default).
            4. Return ONLY JSON.
            
            Example:
            {{"intent": "search_listings", "category": "service", "keywords": "plumber", "location": "Soweto"}}
            """
            
            response = self.model.generate_content(prompt)
            
            # Clean the response (sometimes LLMs add ```json ... ``` wrappers)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(clean_text)
            
        except Exception as e:
            print(f"AI Brain Error: {e}")
            # Fallback if AI fails
            return {"intent": "unknown"}
        
    def generate_keywords(self, title, category):
        """
        [NEW] reads a listing title and creates searchable tags.
        e.g. "Sparks Fix" -> "electrician, wiring, maintenance, lights"
        """
        try:
            prompt = f"""
            Generate 5 comma-separated search keywords for a service.
            Title: "{title}"
            Category: "{category}"
            
            Rules:
            1. Include synonyms (e.g. if 'Car Wash', add 'cleaning', 'vehicle').
            2. Return ONLY the words separated by commas. No intro text.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.lower().strip()
        except Exception as e:
            print(f"Auto-Tag Error: {e}")
            return title.lower() # Fallback to just using the title
        

# Singleton instance
ai_brain = AIService()