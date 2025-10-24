# twilio_alerts.py
from twilio.rest import Client

# Twilio credentials (replace with your own)
ACCOUNT_SID = "TwilioAccount_SID"
AUTH_TOKEN = "TwilioAuthToken"
FROM_NUMBER = "+123456789"   # Twilio phone number
TO_NUMBER = "+91xxxxxxxxx"   # Your phone number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms_alert(message):
    client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

