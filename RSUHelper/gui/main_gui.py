import tkinter as tk
from RSUHelper.gui.input_form import RSUInputForm
from RSUHelper.gui.result_display import RSUResultDisplay
from RSUHelper.calculations import get_vest_price
from RSUHelper.forecasting import StockForecaster


class RSUHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSU Decision Helper")
        self.root.geometry("1000x700")

        self.input_form = RSUInputForm(root)

        self.button = tk.Button(root, text="Calculate", command=self.run_analysis)
        self.button.grid(row=5, column=0, columnspan=2, pady=10)

        self.output_frame = tk.Frame(root)
        self.output_frame.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.result_display = RSUResultDisplay(self.output_frame)

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
        predictions = forecaster.get_all_predications()
        self.result_display.render(ticker, current_price, shares, vest_price, predictions)


def main():
    root = tk.Tk()
    app = RSUHelperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
