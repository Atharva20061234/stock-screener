from screener import detect_breakout
from alerts_module import send_alerts
import datetime
import warnings
warnings.filterwarnings("ignore")

# Nifty 500 stock list
from nifty500_stocks import stock_list as nifty_500_symbols  # If saved in nifty500_stocks.py

# NSE timings (adjust your own timezone logic if needed)
current_time = datetime.datetime.now().time()

# Run during NSE hours only
if datetime.time(9, 15) <= current_time <= datetime.time(15, 30):
    print("🔄 Running breakout check within NSE time window...")

    breakout_stocks = detect_breakout(nifty_500_symbols)

    if breakout_stocks:
        print(f"✅ Breakout stocks: {', '.join(breakout_stocks)}")
        send_alerts(breakout_stocks)
    else:
        print("📉 No breakout stocks found.")
else:
    print("⏰ Outside NSE trading hours. Skipping.")

