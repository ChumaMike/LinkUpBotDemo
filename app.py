from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/home")
@app.route("/")
def home():
    return "Bot is running"

@app.route("/whatsapp", methods=["POST"])
def wahtsapp():
    incoming_msg = request.values.get("Body", "").lower()
    response = MessagingResponse()
    msg = response.message()
    if "house" in incoming_msg or "rent" in incoming_msg:
        msg.body("Here are some places to rent in Rosebank: \n1. 2-bed in Parktown - R15K\n2. Studio in Melrose - R10K")
    elif "job" in incoming_msg:
        msg.body("Available jobs:\n- Sales Assistant in Rosebank\n- Remote Social Media Intern")
    else:
        msg.body("Hi! Welcome to LinkUp. Reply with:\n- 'house' to find rentals\n- 'job' to find jobs")

    return str(response)


if __name__== "__main__":
    app.run(debug=True)
