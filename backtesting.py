from mySecrets import alpaca_keys
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from alpaca.data import StockHistoricalDataClient, StockTradesRequest
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


#trading_client = TradingClient(api_key=alpaca_keys["KEY"], secret_key=alpaca_keys["SECRET"])

historical_data_client = StockHistoricalDataClient(alpaca_keys["KEY"], alpaca_keys["SECRET"])

request_param = StockTradesRequest(
    symbol_or_symbols= "AAPL",
    start = datetime(2024, 6, 7, 14, 0),
    end = datetime(2024, 6, 7, 14, 15)
    )

# Hours M-F, 8AM-5PM EST

trades = historical_data_client.get_stock_trades(request_param)

# print(trades)

# Fetch historical data symbol = 'QQQ' start_date = '2015-01-01' end_date = '2022-12-31' data = yf.download(symbol, start=start_date, end=end_date)


# Fetch historical data 
symbol = 'AAPL' 
start_date = '2015-01-01' 
end_date = '2022-12-31' 
data = yf.download(symbol, start=start_date, end=end_date)

def rsi(data, period): 
    delta = data.diff().dropna() 
    gain = delta.where(delta > 0, 0) 
    loss = -delta.where(delta < 0, 0) 
    avg_gain = gain.rolling(window=period).mean() 
    avg_loss = loss.rolling(window=period).mean() 
    rs = avg_gain / avg_loss 
    return 100 - (100 / (1 + rs)) # Calculate the 14-day RSI data['RSI'] = rsi(data['Close'], 14)

data['Signal'] = 0 
data.loc[data['RSI'] < 30, 'Signal'] = 1 
data.loc[data['RSI'] > 70, 'Signal'] = -1

data['Daily_Return'] = data['Close'].pct_change() 
data['Strategy_Return'] = data['Daily_Return'] * data['Signal'].shift(1) 
data['Cumulative_Return'] = (1 + data['Strategy_Return']).cumprod()