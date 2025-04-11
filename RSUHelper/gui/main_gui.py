import tkinter as tk
from RSUHelper.gui.input_form import RSUInputForm
from RSUHelper.gui.result_display import RSUResultDisplay
from RSUHelper.calculations import get_vest_price
from RSUHelper.forecasting import StockForecaster


class RSUHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSU Decision Helper")
        self.root.geometry("1200x750")

        self.short_term_tax = tk.DoubleVar(value=0.37)
        self.long_term_tax = tk.DoubleVar(value=0.20)
        self.simulation_count = tk.IntVar(value=1000)
        self.arima_order = tk.StringVar(value="5,1,0")

        # Left panel for input
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.input_form = RSUInputForm(self.input_frame)
        self.button = tk.Button(self.input_frame, text="Calculate", command=self.run_analysis)
        self.button.grid(row=5, column=0, columnspan=2, pady=10)

        self.advanced_button = tk.Button(self.input_frame, text="Advanced Options", command=self.toggle_advanced)
        self.advanced_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.advanced_frame = tk.Frame(self.input_frame)
        self.advanced_visible = False
        self._build_advanced_options()

        # Right panel for output
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.result_display = RSUResultDisplay(self.output_frame)

    def _build_advanced_options(self):
        tk.Label(self.advanced_frame, text="Short-Term Tax Rate (%):").grid(row=0, column=0, sticky="w")
        tk.Entry(self.advanced_frame, textvariable=self.short_term_tax).grid(row=0, column=1, sticky="w")

        tk.Label(self.advanced_frame, text="Long-Term Tax Rate (%):").grid(row=1, column=0, sticky="w")
        tk.Entry(self.advanced_frame, textvariable=self.long_term_tax).grid(row=1, column=1, sticky="w")

        tk.Label(self.advanced_frame, text="Monte Carlo Simulations:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.advanced_frame, textvariable=self.simulation_count).grid(row=2, column=1, sticky="w")

        tk.Label(self.advanced_frame, text="ARIMA Order (p,d,q):").grid(row=3, column=0, sticky="w")
        tk.Entry(self.advanced_frame, textvariable=self.arima_order).grid(row=3, column=1, sticky="w")

    def toggle_advanced(self):
        if self.advanced_visible:
            self.advanced_frame.grid_forget()
            self.advanced_visible = False
        else:
            self.advanced_frame.grid(row=7, column=0, columnspan=2, pady=5)
            self.advanced_visible = True

    def run_analysis(self):
        inputs = self.input_form.get_inputs()
        if not inputs:
            return

        ticker, current_price, shares, vest_price_input, vest_date_input = inputs

        if vest_price_input:
            vest_price = float(vest_price_input)
        elif vest_date_input:
            vest_price = get_vest_price(ticker, vest_date_input)
            if vest_price is None:
                return
        else:
            return

        forecaster = StockForecaster(ticker)

        # Use simulation settings
        try:
            forecaster.rng = forecaster.rng  # Keep deterministic seed
            forecaster.simulations = int(self.simulation_count.get())
            arima_order = tuple(map(int, self.arima_order.get().split(",")))
            forecaster.arima_order = arima_order
        except Exception as e:
            print(f"Error applying advanced forecasting settings: {e}")

        predictions = forecaster.get_all_predications()

        self.result_display.short_term_tax = self.short_term_tax.get()
        self.result_display.long_term_tax = self.long_term_tax.get()
        self.result_display.render(ticker, current_price, shares, vest_price, predictions)


def main():
    root = tk.Tk()
    app = RSUHelperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
