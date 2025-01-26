from decouple import config
from twilio.rest import Client

# Load credentials
TWILIO_API_KEY = 'AC904b70ae8d64a472781b743a9eac7b4a'
TWILIO_API_SECRET = 'oOwgQmj4724TftYole8O7gVYOVjvMk5S'

# Twilio WhatsApp sandbox number
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# List of recipients
recipients = [
    "whatsapp:+916379077144",
    "whatsapp:+919952741577",
]

# Message content
message_body = "Hello! This is a test message from Vimal Solar."

# Initialize Twilio client
client = Client(TWILIO_API_KEY, TWILIO_API_SECRET)

# Send message
for recipient in recipients:
    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=recipient,
        )
        print(f"Message sent to {recipient}: SID {message.sid}")
    except Exception as e:
        print(f"Failed to send message to {recipient}: {e}")
