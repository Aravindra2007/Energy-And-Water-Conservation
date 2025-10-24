# twilio_alerts.py
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC855c77cab687272ab71ca1d72d0a36d3"
AUTH_TOKEN = "18a40942933cfe1b63fce2c49eadcf97"
FROM_NUMBER = "+19789589288"   # Your Twilio phone number
TO_NUMBER = "+918919146448"   # Your verified mobile number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms_alert(message):
    try:
        client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=TO_NUMBER
        )
        print("SMS sent:", message)
    except Exception as e:
        print("Twilio SMS failed:", e)
