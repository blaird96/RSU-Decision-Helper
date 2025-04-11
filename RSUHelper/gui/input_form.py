import tkinter as tk
from tkinter import messagebox
from RSUHelper.stock_price import get_stock_price
from RSUHelper.calculations import get_vest_price

class RSUInputForm:
    def __init__(self, root):
        self.root = root
        self.entries = {}
        self._build_inputs()

    def _build_inputs(self):
        labels = [
            ("Ticker Symbol:", "ticker"),
            ("Shares Vested:", "shares"),
            ("Vesting Price (optional):", "vest_price"),
            ("Vesting Date (YYYY-MM-DD, optional):", "vest_date"),
        ]

        for idx, (text, key) in enumerate(labels):
            tk.Label(self.root, text=text).grid(row=idx, column=0, sticky="w", padx=10, pady=2)
            entry = tk.Entry(self.root, justify="left")
            entry.grid(row=idx, column=1, sticky="w", padx=5, pady=2)
            self.entries[key] = entry

    def get_inputs(self):
        try:
            ticker = self.entries["ticker"].get().strip().upper()
            shares = float(self.entries["shares"].get().strip())
            vest_price_input = self.entries["vest_price"].get().strip()
            vest_date_input = self.entries["vest_date"].get().strip()
            
            # Fetch vesting price from Yahoo if vesting data is provided
            vest_price = None
            if vest_date_input:
                vest_price = get_vest_price(ticker, vest_date_input)
                if vest_price is None:
                    raise(ValueError("Could not retrieve vesting price. Please try a different date."))
            
            # If user entered a manual vesting price, override it
            if vest_price_input:
                vest_price = float(vest_price_input)

            if not ticker or not shares:
                raise ValueError("Missing required fields.")

            current_price = get_stock_price(ticker)
            if current_price is None:
                raise ValueError("Failed to fetch current stock price.")

            return ticker, current_price, shares, vest_price_input, vest_date_input

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None
