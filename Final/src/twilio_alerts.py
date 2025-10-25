# twilio_alerts.py
from twilio.rest import Client

# Twilio credentials
ACCOUNT_SID = "AC6c7690f9d0b31b8d1873288a5968f28a"
AUTH_TOKEN = "a164ce82616975261fecdaf2014f977c"
FROM_NUMBER = "+19788833751"   # Your Twilio phone number
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

