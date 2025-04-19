import yfinance as yf
from nifty500_stocks import stock_list
from alerts_module import send_alerts

def detect_breakout(stock):
    try:
        # Multi-timeframe data download
        data_daily = yf.download(stock, period="5d", interval="1d", progress=False)
        data_hourly = yf.download(stock, period="5d", interval="1h", progress=False)
        data_weekly = yf.download(stock, period="5d", interval="1wk", progress=False)

        # Check if any data is missing
        if data_daily.empty or data_hourly.empty or data_weekly.empty:
            print(f"⚠ No data found for {stock}. Skipping.")
            return False

        # Debugging: print the last few rows of each timeframe to inspect
        print(f"\n🔍 Data for {stock}:")
        print("Daily data (last 5 days):")
        print(data_daily.tail())
        print("Hourly data (last 5 hours):")
        print(data_hourly.tail())
        print("Weekly data (last 5 weeks):")
        print(data_weekly.tail())

        if len(data_daily) < 5 or len(data_hourly) < 5 or len(data_weekly) < 5:
            print(f"⚠ Not enough data for {stock}. Skipping.")
            return False

        # Daily timeframe calculations
        prev_close = data_daily['Close'].iloc[-2]
        today_high = data_daily['High'].iloc[-1]
        today_volume = data_daily['Volume'].iloc[-1]
        avg_volume_daily = data_daily['Volume'].iloc[-5:-1].mean()

        # Hourly timeframe volume comparison
        avg_volume_hourly = data_hourly['Volume'].iloc[-5:].mean()

        # Weekly timeframe volume comparison
        avg_volume_weekly = data_weekly['Volume'].iloc[-1]  # Only one value, volume of the last week

        # Multi-timeframe breakout conditions
        price_breakout_daily = today_high > prev_close * 1.01
        volume_spike_daily = today_volume > avg_volume_daily * 1.5
        volume_spike_hourly = today_volume > avg_volume_hourly * 1.5
        volume_spike_weekly = today_volume > avg_volume_weekly * 1.5

        # Ensuring breakout condition is met across multiple timeframes
        price_breakout = price_breakout_daily  # Price breakout condition based on daily high
        volume_spike = volume_spike_daily and volume_spike_hourly and volume_spike_weekly  # Volume spike condition across all timeframes

        return price_breakout and volume_spike

    except Exception as e:
        print(f"⚠ Error with {stock}: {e}")
        return False

def run_screener():
    breakout_stocks = []

    for stock in stock_list:
        print(f"\n🔍 Checking {stock}...")
        if detect_breakout(stock):
            print(f"✅ {stock} is breaking out!")
            send_alert(stock)
            breakout_stocks.append(stock)

    if breakout_stocks:
        print(f"\n✅ Breakouts detected: {breakout_stocks}")
    else:
        print("\n📉 No breakout stocks detected.")

if __name__ == "__main__":
    run_screener()



