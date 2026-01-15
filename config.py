import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    # You can add TWILIO_AUTH_TOKEN here later too