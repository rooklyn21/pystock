import akshare as ak
import mplfinance as mpf  # Please install mplfinance as follows: pip install mplfinance

stock_us_daily_df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
stock_us_daily_df = stock_us_daily_df[["open", "high", "low", "close", "volume"]]
stock_us_daily_df.columns = ["Open", "High", "Low", "Close", "Volume"]
stock_us_daily_df.index.name = "Date"
stock_us_daily_df = stock_us_daily_df["2021-01-01": "2022-06-18"]
mpf.plot(stock_us_daily_df, type='candle', mav=(5, 10, 20,60,110,200), volume=True, show_nontrading=False)