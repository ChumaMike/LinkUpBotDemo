from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json
from weather import *

app = Flask(__name__)


with open("listings.json", "r") as file:
    listings = json.load(file)

@app.route("/home")
@app.route("/")
def home():
    return "Bot is running"


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    sender = request.values.get("From")
    response = MessagingResponse()
    msg = response.message()


    cities = ["johannesburg", "pretoria", "soweto"]

    categories = {
        "house": ["house", "rent", "apartment", "flat"],
        "job": ["job", "work", "umsebenzi"],
        "service": ["service", "help", "cleaning", "hair", "repair"]
    }

    the_city = None
    the_category = None
    reply = ""


    if "weather in" in incoming_msg:
        city = incoming_msg.replace("weather in", "").strip()
        reply = get_weather(city)
    else:
        for city in cities:
            if city in incoming_msg:
                the_city = city
                break

        for category, keywords in categories.items():
            if any(word in incoming_msg for word in keywords):
                the_category = category
                break

        if the_city and the_category:
            results = [
                item for item in listings
                if item["category"] == the_category and item["city"] == the_city
            ]

            if results:
                reply = f"{the_category.capitalize()} listings in {the_city.capitalize()}:\n"
                for r in results:
                    reply += f"{r['title']} - {r['price']} (call: {r['contact']})\n"
            else:
                reply = f"No {the_category}s found in {the_city}."
        else:
            reply = (
                "Welcome to LinkUp!\n\n"
                "Type something like:\n"
                "• house in Soweto\n"
                "• job in Johannesburg\n"
                "• service in Pretoria\n"
                "• weather in Johannesburg"
            )

    msg.body(reply)
    return str(response)
                
    


if __name__== "__main__":
    app.run(debug=True)
