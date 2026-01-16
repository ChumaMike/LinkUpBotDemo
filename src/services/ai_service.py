import os
import google.generativeai as genai
import json

class AIService:
    def __init__(self):
        # Configure the API
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        
        # We use 'gemini-pro' for text analysis
        self.model = genai.GenerativeModel('gemini-pro')

    def parse_intent(self, user_text):
        """
        Uses LLM to understand what the user wants.
        Returns a JSON object: {'intent': 'search', 'category': 'plumber', 'location': 'soweto'}
        """
        try:
            # The Magic Prompt: Forces structured JSON output
            prompt = f"""
            You are the brain of a WhatsApp bot for 'LinkUp Geo', a township service marketplace.
            Analyze the following user text and extract the intent.
            
            User Text: "{user_text}"
            
            Rules:
            1. Identify the 'intent'. Options: 'search_listings', 'weather', 'greeting', 'unknown'.
            2. If 'search_listings', extract 'category' (e.g., plumber, electrician, rental, job) and 'location' (city/township).
            3. If the user describes a problem (e.g., "burst pipe"), map it to the correct category (e.g., "service").
            4. Return ONLY valid JSON. No markdown, no conversational text.
            
            Example Output:
            {{"intent": "search_listings", "category": "service", "keywords": "plumber", "location": "soweto"}}
            """
            
            response = self.model.generate_content(prompt)
            
            # Clean the response (sometimes LLMs add ```json ... ``` wrappers)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            
            return json.loads(clean_text)
            
        except Exception as e:
            print(f"AI Brain Error: {e}")
            # Fallback if AI fails
            return {"intent": "unknown"}

# Singleton instance
ai_brain = AIService()