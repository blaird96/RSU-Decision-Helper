import tkinter as tk
from tkinter import messagebox, ttk
from RSUHelper.calculations import (
    calculate_profit,
    calculate_gains_since_vesting,
    required_gain_to_offset_shorting_loss,
    get_vest_price,
)
from RSUHelper.forecasting import StockForecaster
from RSUHelper.stock_price import get_stock_price


class RSUHelperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSU Decision Helper")
        self.root.geometry("1000x700")  # Increased window size for better output display
        self.create_widgets()

    def create_widgets(self):
        labels = [
            ("Ticker Symbol:", "ticker"),
            ("Shares Vested:", "shares"),
            ("Vesting Price (optional):", "vest_price"),
            ("Vesting Date (YYYY-MM-DD, optional):", "vest_date"),
        ]
        self.entries = {}

        for idx, (text, key) in enumerate(labels):
            tk.Label(self.root, text=text).grid(row=idx, column=0, sticky="w", padx=10, pady=2)
            entry = tk.Entry(self.root, justify="left")
            entry.grid(row=idx, column=1, sticky="w", padx=5, pady=2)
            self.entries[key] = entry

        tk.Button(self.root, text="Calculate", command=self.run_analysis).grid(
            row=len(labels), column=0, columnspan=2, pady=10
        )

        self.output_frame = tk.Frame(self.root)
        self.output_frame.grid(row=len(labels) + 1, column=0, columnspan=2, sticky="nsew")

        self.canvas = tk.Canvas(self.output_frame, height=500, width=960)  # Expanded canvas width
        self.scrollbar = ttk.Scrollbar(self.output_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_result = tk.Frame(self.canvas)

        self.scrollable_result.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_result, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def get_user_inputs(self):
        try:
            ticker = self.entries["ticker"].get().strip().upper()
            shares = float(self.entries["shares"].get().strip())
            vest_price_input = self.entries["vest_price"].get().strip()
            vest_date_input = self.entries["vest_date"].get().strip()

            if not ticker or not shares:
                raise ValueError("Missing required fields.")

            current_price = get_stock_price(ticker)
            if current_price is None:
                raise ValueError("Failed to fetch current stock price.")

            return ticker, current_price, shares, vest_price_input, vest_date_input

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None

    def get_vesting_price(self, ticker, vest_price_input, vest_date_input):
        if vest_price_input:
            return float(vest_price_input)
        elif vest_date_input:
            price = get_vest_price(ticker, vest_date_input)
            if price is None:
                messagebox.showerror("Vesting Price Error", "Could not retrieve vesting price.")
            return price
        else:
            messagebox.showerror("Missing Input", "Enter either a vesting price or a vesting date.")
            return None

    def run_forecasts(self, ticker):
        forecaster = StockForecaster(ticker)
        return forecaster.get_all_predications()

    def display_grid_output(self, ticker, current_price, shares, vest_price, predictions):
        for widget in self.scrollable_result.winfo_children():
            widget.destroy()

        row = 0
        tk.Label(self.scrollable_result, text=f"{ticker} — Current: ${current_price:.2f} — Shares: {shares} — Vest Price: ${vest_price:.2f}", font=("Helvetica", 10, "bold")).grid(row=row, column=0, columnspan=5, pady=5, sticky="w")
        row += 1

        gains = calculate_gains_since_vesting(vest_price, current_price, shares)
        short_term = calculate_profit(current_price, current_price, shares)

        tk.Label(self.scrollable_result, text="Short-Term Profit:").grid(row=row, column=0, sticky="w", padx=10)
        tk.Label(self.scrollable_result, text=f"${short_term['Short-Term Profit']:.2f}").grid(row=row, column=1, sticky="w")
        tk.Label(self.scrollable_result, text="Gain Since Vesting:").grid(row=row, column=2, sticky="w")
        tk.Label(self.scrollable_result, text=f"${gains['Total Gain Since Vesting']:.2f}").grid(row=row, column=3, sticky="w")
        row += 2

        headers = ["Method", "Forecasted Price", "Long-Term Profit", "Delta", "Recommendation"]
        for col, header in enumerate(headers):
            tk.Label(self.scrollable_result, text=header, font=("Helvetica", 10, "underline")).grid(row=row, column=col, sticky="w", padx=10)
        row += 1

        for method, predicted_price in predictions.items():
            if predicted_price is None:
                continue

            profit = calculate_profit(current_price, predicted_price, shares)
            tk.Label(self.scrollable_result, text=method).grid(row=row, column=0, sticky="w", padx=10)
            tk.Label(self.scrollable_result, text=f"${predicted_price:.2f}").grid(row=row, column=1, sticky="w")
            tk.Label(self.scrollable_result, text=f"${profit['Long-Term Profit']:.2f}").grid(row=row, column=2, sticky="w")
            tk.Label(self.scrollable_result, text=f"${profit['Delta (Hold vs Short)']:.2f}").grid(row=row, column=3, sticky="w")
            tk.Label(self.scrollable_result, text=profit['Recommendation']).grid(row=row, column=4, sticky="w")
            row += 1

    def run_analysis(self):
        inputs = self.get_user_inputs()
        if not inputs:
            return

        ticker, current_price, shares, vest_price_input, vest_date_input = inputs
        vest_price = self.get_vesting_price(ticker, vest_price_input, vest_date_input)

        if vest_price is None:
            return

        predictions = self.run_forecasts(ticker)
        self.display_grid_output(ticker, current_price, shares, vest_price, predictions)


def main():
    root = tk.Tk()
    app = RSUHelperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
