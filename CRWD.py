import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import time

pio.renderers.default = 'browser'

tickers = [
   "FACTU"
]




today = datetime.today()
start_date = '2020-01-01'

for ticker in tickers:
    print(f"\n=== {ticker} ===")
    time.sleep(10)
    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(start=start_date, end=today.strftime('%Y-%m-%d'))
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        continue

    if data.empty or 'Close' not in data:
        print(f"No data found for {ticker}. Skipping.")
        continue

    '''data.columns = data.columns.get_level_values(0)'''
    close_prices = data['Close']
    trading_days = len(close_prices)

    # Dates for return calculations
    one_year_ago = today - timedelta(days=365)
    three_years_ago = today - timedelta(days=365 * 3)

    # --- Return Calculations ---
    try:
        if trading_days >= 252:
            idx_1y = close_prices.index.get_indexer([one_year_ago], method='nearest')[0]
            price_1y = close_prices.iloc[idx_1y]
            periods = trading_days - idx_1y
            ret_1y = (close_prices.iloc[-1] - price_1y) / price_1y
            annual_1y = (1 + ret_1y) ** (252 / periods) - 1
            print(f"1-Year Annualized Return:    {annual_1y:.2%}")
        else:
            print("Not enough data for 1-year return.")

        if trading_days >= 252 * 3:
            idx_3y = close_prices.index.get_indexer([three_years_ago], method='nearest')[0]
            price_3y = close_prices.iloc[idx_3y]
            periods = trading_days - idx_3y
            ret_3y = (close_prices.iloc[-1] - price_3y) / price_3y
            annual_3y = (1 + ret_3y) ** (252 / periods) - 1
            print(f"3-Year Annualized Return:    {annual_3y:.2%}")
        else:
            print("Not enough data for 3-year return.")

        # Since IPO
        price_ipo = close_prices.iloc[0]
        ret_ipo = (close_prices.iloc[-1] - price_ipo) / price_ipo
        annual_ipo = (1 + ret_ipo) ** (252 / trading_days) - 1
        print(f"Since IPO Annualized Return: {annual_ipo:.2%}")

    except Exception as e:
        print(f"Error calculating returns: {e}")

    # --- Indicators ---
    data['MA14'] = data['Close'].rolling(window=14).mean()
    data['MA20'] = data['Close'].rolling(window=20).mean()

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))

    data_clean = data.dropna(subset=['MA14', 'MA20', 'RSI'])

    if data_clean.empty:
        print(f"Not enough data to plot indicators for {ticker}.")
        continue

    # --- MA Chart ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_clean.index, y=data_clean['Close'], name='Close'))
    fig.add_trace(go.Scatter(x=data_clean.index, y=data_clean['MA14'], name='14-day MA'))
    fig.add_trace(go.Scatter(x=data_clean.index, y=data_clean['MA20'], name='20-day MA'))
    fig.update_layout(title=f"{ticker} Closing Price with MA14 & MA20",
                      xaxis_title="Date", yaxis_title="Price (USD)",
                      template="plotly_white")
    fig.show()

    # --- RSI Chart ---
    fig_rsi = px.line(data_clean, x=data_clean.index, y='RSI', title=f"{ticker} RSI (Relative Strength Index)")
    fig_rsi.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Overbought (70)", annotation_position="top right")
    fig_rsi.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Oversold (30)", annotation_position="bottom right")
    fig_rsi.update_layout(template="plotly_white")
    fig_rsi.show()
