import yfinance as yf
import finplot as fplt

#This should be called from a right click of a stock 
def plot_graph(ticker):
    # CREATE A TICKER INSTANCE FOR TESLA
    stock = yf.Ticker(ticker)

    # RETRIEVE 1 YEAR WORTH OF DAILY DATA OF TESLA
    df = stock.history(interval='1d',period='1y')

    # PLOT THE OHLC CANDLE CHART
    fplt.candlestick_ochl(df[['Open','Close','High','Low']])
    fplt.show()