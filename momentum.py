#momentum-based strategy

import pandas as pd

def momentum_buy_sell(stock):
    hist = stock.history(period="max")
    curr_price = stock.history(period="1d")["Close"][0]
    long_moving_avg = pd.Series(hist['Close']).rolling(window=200).mean().iloc[-1]
    short_moving_avg = pd.Series(hist['Close']).rolling(window=50).mean().iloc[-1]
    curr_close = hist['Close'][-1]
    prev_close = hist['Close'][-2]
    curr_increase = curr_close > prev_close
    pe_ratio = stock.info['forwardPE']
    if curr_increase and curr_price > long_moving_avg and pe_ratio is not None and pe_ratio > 0:
        if pe_ratio < 15:
            return "Buy"#Strong Buy"
        else:
            return "Buy"#Weak Buy"
    elif curr_increase or curr_price > short_moving_avg:
        return "Buy"#Weak Buy"
    elif not curr_increase and curr_price < long_moving_avg:
        if pe_ratio is not None and pe_ratio > 0:
            if pe_ratio > 20:
                return "Sell"#Strong Sell"
            else:
                return "Sell"#Weak Sell"
        else:
            return "Sell"#Weak Sell"
    else:
        return "Sell"#Weak Sell"
