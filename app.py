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
    
    for city in listings:
        if city in incoming_msg:
            if "house" in incoming_msg or "rent" in incoming_msg:
                houses = listings[city].get("houses", [])
    
                if houses:
                    msg.body(f"Houses in {city}:\n\n" + "\n".join(houses))
                else:
                    msg.body(f"No houses found in {city}")
                found = True
                
            elif "job" in incoming_msg or "work" in incoming_msg:
                jobs = listings[city].get("jobs", [])
                
                if jobs:
                    msg.body(f"Jobs in {city}:\n\n" + "\n".join(jobs))
                else:
                    msg.body(f"Umsebenzi unqabile in {city}")
                found = True
    if not found:
        msg.body("Hi! Welcome to LinkUp.\nType something like 'house in Rosebank' or 'job in Soweto'.")

    return str(response)


if __name__== "__main__":
    app.run(debug=True)
