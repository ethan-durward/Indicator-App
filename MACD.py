#Moving Average Convergence Divergence

import pandas as pd

def calculate_ema(ticker, window):
    # Get historical data for the stock
    df = pd.read_csv(f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=0&period2=9999999999&interval=1d&events=history&includeAdjustedClose=true')
    
    # Calculate EMA using the closing price
    ema = df['Adj Close'].ewm(span=window, adjust=False).mean()
    
    return ema

def calculate_macd(ticker):
    # Get the 12-day and 26-day EMAs
    ema_12 = calculate_ema(ticker, 12)
    ema_26 = calculate_ema(ticker, 26)
    
    # Calculate the MACD line
    macd_line = ema_12 - ema_26
    
    # Calculate the signal line
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    
    # Calculate the histogram
    histogram = macd_line - signal_line
    
    return macd_line, signal_line, histogram
