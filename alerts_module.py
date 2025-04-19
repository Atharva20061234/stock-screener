import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_alerts(stock_list):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("⚠️ Missing bot token or chat ID in environment variables.")
        return

    # Format the message
    message = "🚨 Breakout Alert:\n" + "\n".join(stock_list)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {'chat_id': chat_id, 'text': message}

    # Send the request
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("✅ Alert sent successfully!")
    else:
        print("❌ Failed to send alert:", response.text)

# Test alert (optional)
if __name__ == "__main__":
    send_alerts(["RELIANCE.NS", "TCS.NS"])
