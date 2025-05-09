from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import json


app = Flask(__name__)


with open("listings.json", "r") as file:
    listings = json.load(file)

@app.route("/home")
@app.route("/")
def home():
    return "Bot is running"

@app.route("/whatsapp", methods=["POST"])
def wahtsapp():
    incoming_msg = request.values.get("Body", "").lower()
    response = MessagingResponse()
    msg = response.message()
    
    found = False
    reply = ""
    
    cities = ["johannesburg", "pretoria", "soweto"]
    
    categories = {
        "house": ["house", "rent", "apartment", "flat"],
        "job": ["job", "work", "umsebenzi"],
        "service": ["service", "help", "cleaning", "hair", "repair"]
    }
    
    for city in cities:
        if city in incoming_msg:
            the_city = city
            
    for category, value_words in categories.items():
        for word in value_words:
            if word in incoming_msg:
                the_category = category
    
    if the_city and the_category:
        results = []
    


if __name__== "__main__":
    app.run(debug=True)
