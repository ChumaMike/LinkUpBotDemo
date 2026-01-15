from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from src.services.parser_service import MessageParser
from src.services.listing_service import ListingService
from src.services.weather_service import WeatherService

bot_bp = Blueprint('bot', __name__)

# Initialize Services
listing_service = ListingService()
weather_service = WeatherService()

@bot_bp.route("/whatsapp", methods=["POST"])
def whatsapp():
    # 1. Grab incoming data
    incoming_msg = request.values.get("Body", "").lower()
    latitude = request.values.get("Latitude")
    longitude = request.values.get("Longitude")
    
    reply = ""

    # 2. Check: Did they send a Location Pin? 📍
    if latitude and longitude:
        try:
            user_lat = float(latitude)
            user_lon = float(longitude)
            
            # Smart Logic: If they send a pin, we assume they want Services nearby (Plumbers, etc.)
            # Later, we can make this smarter (remember if they asked for jobs vs houses)
            results = listing_service.get_listings_near_me("service", user_lat, user_lon)
            reply = listing_service.format_listings_response(results, "your location")
            
        except ValueError:
            reply = "Error: Invalid location data received."

    # 3. Check: Did they send Text? 💬
    elif incoming_msg:
        # Parse the intent
        parsed_data = MessageParser.parse(incoming_msg)
        
        if parsed_data["type"] == "weather":
            reply = weather_service.get_weather(parsed_data["city"]) 
            
        elif parsed_data["type"] == "search_listings":
            results = listing_service.get_listings(parsed_data["city"], parsed_data["category"])
            reply = listing_service.format_listings_response(results, parsed_data["city"], parsed_data["category"])
            
        else:
            # Help Message
            reply = (
                "👋 *Welcome to LinkUp Geo!*\n\n"
                "I can find things near you.\n"
                "📍 *Send your Location Pin* to find services nearby.\n\n"
                "Or type:\n"
                "• _house in Soweto_\n"
                "• _weather in Pretoria_"
            )
            
    # 4. Send Response
    response = MessagingResponse()
    response.message(reply)
    return str(response)