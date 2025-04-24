import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

message = "🚀 Test Message from your local bot!"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {"chat_id": CHAT_ID, "text": message}

response = requests.post(url, data=payload)

# Only print status if there’s an error
response_json = response.json()
if response_json.get("ok") == False:
    print(f"Error: {response_json.get('description')}")
else:
    print("Message sent successfully!")
