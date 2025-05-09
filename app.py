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
    the_city = None
    the_category = None
    
    #Supported Cities
    cities = ["johannesburg", "pretoria", "soweto"]
    
    categories = {
        "house": ["house", "rent", "apartment", "flat"],
        "job": ["job", "work", "umsebenzi"],
        "service": ["service", "help", "cleaning", "hair", "repair"]
    }
    
    for city in cities:
        if city in incoming_msg:
            the_city = city
            break
            
    for category, value_words in categories.items():
        for word in value_words:
            if word in incoming_msg:
                the_category = category
                break
    
    if the_city and the_category:
        results = []
        for item in listings:
            if item["category"] == the_category and item["city"] == the_city:
                results.append(item)
    
        if results:
            reply = f"{the_category} listings in {the_city}:\n"
            for r in results:
                reply += f"{r['title']} - {r['price']} (call: {r['contact']})\n"
        else:
            reply += f"No {the_category}s found in {the_city}"
    
    else:
        reply = (
            "👋 Welcome to LinkUp!\n"
            "Type something like:\n"
            "`house in Soweto`\n"
            "`job in Johannesburg`\n"
            "`service in Pretoria`\n"
        )
        
    msg.body(reply)
    return str(response)
                
    


if __name__== "__main__":
    app.run(debug=True)
