import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("🔍 Asking Google for available models...")

try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
            count += 1
            
    if count == 0:
        print("❌ No text-generation models found. Check your API Key permissions.")

except Exception as e:
    print(f"❌ ERROR: {e}")