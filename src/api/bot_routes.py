from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from src.services.parser_service import MessageParser
from src.services.listing_service import ListingService
from src.services.weather_service import WeatherService  # <-- IMPORT IT

bot_bp = Blueprint('bot', __name__)

# Initialize Services
listing_service = ListingService()
weather_service = WeatherService()  # <-- INITIALIZE IT

@bot_bp.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "")
    
    # 1. Parse intent
    parsed_data = MessageParser.parse(incoming_msg)
    
    reply = ""
    
    # 2. Route Logic
    if parsed_data["type"] == "weather":
        # USE THE SERVICE
        reply = weather_service.get_weather(parsed_data["city"]) 
        
    elif parsed_data["type"] == "search_listings":
        results = listing_service.get_listings(parsed_data["city"], parsed_data["category"])
        reply = listing_service.format_listings_response(results, parsed_data["city"], parsed_data["category"])
        
    else:
        reply = (
            "Welcome to *LinkUp!* 🤖\n\n"
            "I can help you find jobs, houses, or services.\n"
            "Try typing:\n"
            "• _house in Soweto_\n"
            "• _job in Johannesburg_\n"
            "• _weather in Pretoria_"
        )

    # 3. Response
    response = MessagingResponse()
    response.message(reply)
    return str(response)