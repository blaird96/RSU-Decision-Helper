import tkinter as tk
from tkinter import ttk
from RSUHelper.calculations import (
    calculate_profit,
    calculate_gains_since_vesting,
)


class RSUResultDisplay:
    def __init__(self, parent_frame):
        self.canvas = tk.Canvas(parent_frame, height=500, width=960)
        self.scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_result = tk.Frame(self.canvas)

        self.scrollable_result.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_result, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def render(self, ticker, current_price, shares, vest_price, predictions):
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
