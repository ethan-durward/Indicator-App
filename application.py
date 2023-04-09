import tkinter as tk
from tkinter import ttk
import yfinance as yf


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stock Analysis App")
        self.geometry("800x600")
        
        # Create menu bar
        self.create_menu()
        
        # Create tabs
        self.tab_notebook = ttk.Notebook(self)
        self.create_favourites_tab()
        self.tab_notebook.pack(expand=1, fill="both")
        
    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        
        # Home menu item
        self.home_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.home_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="Home", menu=self.home_menu)
        
        # Favourites menu item
        self.favourites_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.favourites_menu.add_command(label="Add Favourite")
        self.menu_bar.add_cascade(label="Favourites", menu=self.favourites_menu)
        
        # Backtest menu item
        self.backtest_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.backtest_menu.add_command(label="Backtest")
        self.menu_bar.add_cascade(label="Backtest", menu=self.backtest_menu)
        
        self.config(menu=self.menu_bar)
        
    def create_favourites_tab(self):
        self.favourites_tab = tk.Frame(self.tab_notebook)
        self.tab_notebook.add(self.favourites_tab, text="Favourites")
        
        # Favourite stock data display
        stocks = ["AAPL", "MSFT", "GOOG"]
        indicators = ["Momentum", "RSI", "MACD"]
        
        for i, stock in enumerate(stocks):
            ticker_label = tk.Label(self.favourites_tab, text=stock)
            ticker_label.grid(row=i, column=0, padx=10, pady=10)
            
            stock_label = tk.Label(self.favourites_tab, text="Apple Inc.", font=("TkDefaultFont", 10, "bold"))
            stock_label.grid(row=i, column=1, padx=10, pady=10)
            
            price = get_current_price(stock)
            intraday_change = get_intraday_change(stock)
            intraday_percent_change = get_intraday_percent_change(stock)
            
            price_label = tk.Label(self.favourites_tab, text=f"${price:.2f}")
            price_label.grid(row=i, column=2, padx=10, pady=10)
            
            intraday_change_label = tk.Label(self.favourites_tab, text=f"{intraday_change:.2f}", fg="green" if intraday_change >= 0 else "red")
            intraday_change_label.grid(row=i, column=3, padx=10, pady=10)
            
            intraday_percent_change_label = tk.Label(self.favourites_tab, text=f"{intraday_percent_change:.2f}%", fg="green" if intraday_percent_change >= 0 else "red")
            intraday_percent_change_label.grid(row=i, column=4, padx=10, pady=10)
            
            indicator_var = tk.StringVar(self.favourites_tab)
            indicator_var.set(indicators[0])
            
            indicator_dropdown = tk.OptionMenu(self.favourites_tab, indicator_var, *indicators)
            indicator_dropdown.grid(row=i, column=5, padx=10, pady=10)
            
            bubble = tk.Canvas(self.favourites_tab, width=50)





def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"][0]

def get_intraday_change(ticker):
    stock = yf.Ticker(ticker)
    return round((stock.history(period="1d")["Close"][0] - stock.history(period="1d")["Open"][0]), 2)

def get_intraday_percent_change(ticker):
    stock = yf.Ticker(ticker)
    return round((stock.history(period="1d")["Close"][0] - stock.history(period="1d")["Open"][0]) / stock.history(period="1d")["Open"][0] * 100, 2)





            
if __name__ == "__main__":
    app = App()
    app.mainloop()