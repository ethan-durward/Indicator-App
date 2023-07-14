import tkinter as tk
from tkinter import ttk
from customtkinter import CTkButton
import yfinance as yf
import pandas as pd
import numpy as np
from momentum import momentum_buy_sell 
from RSI_divergence import calculate_RSI
from MACD import calculate_macd 
import requests
#from application import get_current_price, get_intraday_change, get_intraday_percent_change


class StockAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Stock Analyzer")
        self.geometry("800x600")

        # Create the top menu
        self.menu_frame = tk.Frame(self)
        self.menu_frame.pack(side="top", fill="x")

        # Create a wrapper frame for the menu buttons
        self.menu_button_frame = tk.Frame(self.menu_frame)
        self.menu_button_frame.pack(anchor="center")

        # Create the menu buttons
        self.home_button = CTkButton(self.menu_button_frame, text="Home", command=self.show_home)
        self.watch_button = CTkButton(self.menu_button_frame, text="Watch Page", command=self.show_watch)
        self.other_button = CTkButton(self.menu_button_frame, text="Other", command=self.show_other)

        self.home_button.pack(side="left")
        self.watch_button.pack(side="left")
        self.other_button.pack(side="left")

        # Create the content frames
        self.home_frame = tk.Frame(self)
        self.watch_frame = tk.Frame(self)
        self.other_frame = tk.Frame(self)

        # Initialize Home page content
        self.initialize_home_page()

        # Initialize Watch page content
        self.initialize_watch_page()

        # Initialize Other page content
        self.initialize_other_page()

        # Show the Home page by default
        self.show_home()

    def initialize_home_page(self):
        # Create a list of example stock tickers (add or modify as needed)
        self.stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "JPM"]

        # Add the indicator combobox
        self.indicator_var = tk.StringVar()
        self.indicator_combobox = ttk.Combobox(self.home_frame, textvariable=self.indicator_var, state="readonly")
        self.indicator_combobox["values"] = ("momentum", "RSI", "MACD")
        self.indicator_combobox.current(0)  # Set the default value to "momentum"
        self.indicator_combobox.bind("<<ComboboxSelected>>", self.update_stock_boxes)
        self.indicator_combobox.pack(pady=10)

        # Set up a scrollbar and canvas to allow horizontal scrolling
        self.home_canvas = tk.Canvas(self.home_frame)
        self.scrollbar = ttk.Scrollbar(self.home_frame, orient="horizontal", command=self.home_canvas.xview)
        self.scrollable_frame = ttk.Frame(self.home_canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.home_canvas.configure(scrollregion=self.home_canvas.bbox("all")))

        self.home_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.home_canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create the stock boxes in a grid layout
        num_cols = 4
        num_rows = 3
        for i, ticker in enumerate(self.stocks):
            row = i // num_cols
            col = i % num_cols
            stock_frame = self.create_stock_box(ticker, self.scrollable_frame)
            stock_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")

        # Configure column and row weights
        for i in range(num_cols):
            self.scrollable_frame.columnconfigure(i, weight=1)
        for i in range(num_rows):
            self.scrollable_frame.rowconfigure(i, weight=1)

        # Pack the canvas and scrollbar
        self.home_canvas.pack(side="bottom", fill="both", expand=True, padx=20, pady=20)
        self.scrollbar.pack(side="bottom", fill="x", padx=20)


    def update_stock_boxes(self, event=None):
        # Remove the existing stock boxes
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        # Create new stock boxes based on the selected indicator
        for ticker in self.stocks:
            stock_frame = self.create_stock_box(ticker, self.scrollable_frame)
            stock_frame.pack(fill="x", padx=10, pady=5)

    def create_stock_box(self, ticker, parent_frame):
        stock_frame = tk.Frame(parent_frame, bd=1, relief="solid", padx=10, pady=10)

        stock = yf.Ticker(ticker)

        # Get stock information
        stock_info = {
            "ticker": ticker,
            "current_price": get_current_price(stock),
            "intraday_change": get_intraday_change(stock),
            "intraday_percent_change": get_intraday_percent_change(stock),
        }
        
        # Vertically stack the information
        tk.Label(stock_frame, text=ticker, font=("Arial", 14, "bold"), bg=None).grid(row=0, column=0, sticky="w")
        tk.Label(stock_frame, text=f"Price: ${stock_info['current_price']:.2f}", font=("Arial", 10), bg=None).grid(row=1, column=0, sticky="w")
        tk.Label(stock_frame, text=f"Change: ${stock_info['intraday_change']:.2f}", font=("Arial", 10), bg=None).grid(row=2, column=0, sticky="w")
        tk.Label(stock_frame, text=f"{stock_info['intraday_percent_change']:.2f}%", font=("Arial", 10), bg=None).grid(row=3, column=0, sticky="w")

        # Set the background color based on the selected indicator
        selected_indicator = self.indicator_var.get()

        if selected_indicator == "momentum":
            buy_or_sell = momentum_buy_sell(stock)
        
        elif selected_indicator == "RSI":
            buy_or_sell = calculate_RSI(stock)

        elif selected_indicator == "MACD":
            buy_or_sell = calculate_macd(ticker)


        if "Buy" in buy_or_sell:
            stock_frame.configure(bg="green")
        elif "Sell" in buy_or_sell:
            stock_frame.configure(bg="red")
        elif "Hold" in buy_or_sell:
            stock_frame.configure(bg="yellow")

        # Update the background color for the labels
        for label in stock_frame.grid_slaves():
            label.configure(bg=stock_frame.cget('bg'))

        return stock_frame
    
    def update_stock_boxes(self, event=None):
        # Remove the existing stock boxes
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

        # Create new stock boxes based on the selected indicator
        num_cols = 4
        for i, ticker in enumerate(self.stocks):
            row = i // num_cols
            col = i % num_cols
            stock_frame = self.create_stock_box(ticker, self.scrollable_frame)
            stock_frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")

        # Configure column and row weights
        for i in range(num_cols):
            self.scrollable_frame.columnconfigure(i, weight=1)


    def initialize_watch_page(self):
        # Add watch page content here
        pass

    def initialize_other_page(self):
        label = tk.Label(self.other_frame, text="Welcome to my app! Made by Ethan Durward")
        label.pack(padx=20, pady=20)

    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack(fill="both", expand=True)
        self.set_button_color("home")

    def show_watch(self):
        self.hide_all_frames()
        self.watch_frame.pack(fill="both", expand=True)
        self.set_button_color("watch")

    def show_other(self):
        self.hide_all_frames()
        self.other_frame.pack(fill="both", expand=True)
        self.set_button_color("other")

    def hide_all_frames(self):
        self.home_frame.pack_forget()
        self.watch_frame.pack_forget()
        self.other_frame.pack_forget()

    def set_button_color(self, selected_button):
        color_active = "#3399ff"
        color_inactive = "#f0f0f0"
        self.home_button["bg"] = color_active if selected_button == "home" else color_inactive
        self.watch_button["bg"] = color_active if selected_button == "watch" else color_inactive
        self.other_button["bg"] = color_active if selected_button == "other" else color_inactive
    

def get_current_price(stock):
    today = stock.history(period='1d')
    return today['Close'][0]

def get_intraday_change(stock):
    return round((stock.history(period='1d')['Close'][0] - stock.history(period='1d')['Open'][0]), 2)

def get_intraday_percent_change(stock):
    return round((stock.history(period="1d")["Close"][0] - stock.history(period="1d")["Open"][0]) / stock.history(period="1d")["Open"][0] * 100, 2)


if __name__ == "__main__":
    app = StockAnalyzerApp()
    app.mainloop()
