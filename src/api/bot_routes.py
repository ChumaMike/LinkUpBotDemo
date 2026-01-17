from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from src.services.listing_service import ListingService
from src.services.weather_service import WeatherService
# 1. Import the Brain
from src.services.ai_service import ai_brain 

bot_bp = Blueprint('bot', __name__)
listing_service = ListingService()
weather_service = WeatherService()

@bot_bp.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip() # Keep case for AI context
    latitude = request.values.get("Latitude")
    longitude = request.values.get("Longitude")
    
    response = MessagingResponse()
    reply = ""

    try:
        # A. Handle Location Pins (Highest Priority)
        if latitude and longitude:
            results = listing_service.get_listings_near_me("service", float(latitude), float(longitude))
            reply = listing_service.format_listings_response(results, "your location")

        # B. Handle Text with AI Brain 🧠
        elif incoming_msg:
            # 1. Ask Gemini what this means
            analysis = ai_brain.parse_intent(incoming_msg)
            
            print(f"🤖 AI Analysis: {analysis}") # Debug log to see what Gemini thinks

            intent = analysis.get("intent")
            
            if intent == "search_listings":
                # Extract details
                category = analysis.get("category", "service") # Default to service
                location = analysis.get("location", "Soweto")  # Default location
                keywords = analysis.get("keywords", "")
                
                # Search DB
                results = listing_service.get_listings(location, category)
                reply = listing_service.format_listings_response(results, f"{keywords} in {location}")
            
            elif intent == "weather":
                city = analysis.get("location", "Johannesburg")
                reply = weather_service.get_weather(city)
                
            elif intent == "greeting":
                reply = "👋 Howzit! I'm LinkUp AI. Tell me what you need (e.g., 'My sink is leaking' or 'I need a job')."
                
            else:
                reply = "🤔 I'm not sure I understood. Try sending your Location Pin 📍 or say 'I need a plumber'."

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        reply = "🚨 System hiccup. Please try again."

    response.message(reply)
    return str(response)        