import backtrader as bt
import yfinance as yf
import pandas as pd
from nifty500_stocks import stock_list  # ✅ Your Nifty 500 list

class SimpleBuyAndHold(bt.Strategy):
    def __init__(self):
        self.has_bought = False

    def next(self):
        if not self.position and not self.has_bought:
            if pd.notna(self.data.close[0]):
                self.buy()
                self.has_bought = True

def clean_columns(df):
    if isinstance(df.columns[0], tuple):
        df.columns = [col[0].lower() for col in df.columns]
    else:
        df.columns = [col.lower() for col in df.columns]
    return df

def run_backtest(ticker, start='2022-01-01', end='2025-04-01'):
    try:
        df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)

        if df.empty:
            print(f"⚠️ No data for {ticker}, skipping.")
            return

        df = clean_columns(df)

        if 'close' not in df.columns:
            print(f"⚠️ 'close' column not found for {ticker}, skipping.")
            return

        df.dropna(subset=['close'], inplace=True)
        df.index = pd.to_datetime(df.index)

        cerebro = bt.Cerebro()
        data = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(data)
        cerebro.addstrategy(SimpleBuyAndHold)
        cerebro.broker.set_cash(100000)
        cerebro.broker.setcommission(commission=0.001)

        cerebro.run()
        final_value = cerebro.broker.getvalue()
        print(f"✅ {ticker} Final Portfolio Value: ₹{final_value:.2f}")

    except Exception as e:
        print(f"❌ Error with {ticker}: {e}")

# 🧪 Loop through a subset for testing (e.g., first 10 stocks)
if __name__ == "__main__":
    print("📊 Running backtest on Nifty 500 stocks...\n")
    for ticker in stock_list:  # ⚠️ Use `[:10]` for fast testing; change to `stock_list` for full
        print(f"🔄 Backtesting {ticker}...")
        run_backtest(ticker)

