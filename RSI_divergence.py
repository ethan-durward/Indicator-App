#relative strength index indicator accounting for divergence

import pandas as pd
import numpy as np

def calculate_RSI(stock, period=14):
    # Get historical data using yfinance
    stock_data = stock.history(period="1y")

    # Calculate price change and gain/loss
    stock_data['price_change'] = stock_data['Close'].diff()
    stock_data['gain'] = stock_data['price_change'].apply(lambda x: x if x > 0 else 0)
    stock_data['loss'] = stock_data['price_change'].apply(lambda x: abs(x) if x < 0 else 0)

    # Calculate average gain/loss over given period
    stock_data['avg_gain'] = stock_data['gain'].rolling(window=period).mean()
    stock_data['avg_loss'] = stock_data['loss'].rolling(window=period).mean()

    # Calculate RSI
    stock_data['RS'] = stock_data['avg_gain'] / stock_data['avg_loss']
    stock_data['RSI'] = 100 - (100 / (1 + stock_data['RS']))

    # Calculate divergence
    stock_data['RSI_change'] = stock_data['RSI'].diff()
    stock_data['price_change_sign'] = np.sign(stock_data['price_change'])
    stock_data['divergence'] = np.where(
        (stock_data['RSI_change'].shift(1) > 0) & (stock_data['price_change_sign'].shift(1) < 0),
        'Bullish Divergence',
        np.where(
            (stock_data['RSI_change'].shift(1) < 0) & (stock_data['price_change_sign'].shift(1) > 0),
            'Bearish Divergence',
            'No Divergence'
        )
    )

    # Return RSI and divergence signals
    current_rsi = stock_data['RSI'].iloc[-1]
    divergence_signal = stock_data['divergence'].iloc[-1]

    # Generate buy, sell, and hold signals based on RSI and divergence signals
    if current_rsi < 30 or (divergence_signal == 'Bullish Divergence' and current_rsi < 50):
        return "Buy"
    elif current_rsi > 70 or (divergence_signal == 'Bearish Divergence' and current_rsi > 50):
        return "Sell"
    else:
        return "Hold"
