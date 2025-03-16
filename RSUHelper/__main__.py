import logging

# Local Imports
from RSUHelper.stock_price import get_stock_price
from RSUHelper.forecasting import StockForecaster
from RSUHelper.arguments import get_user_input
from RSUHelper.calculations import (
    calculate_profit,
    calculate_gains_since_vesting,
    required_gain_to_offset_shorting_loss
)

# Initializing logger
logger = logging.getLogger(__name__)

class DisplayResults:
    """Handles displaying stock predictions and profit analysis resutlts."""
    
    @staticmethod
    def show_predictions(predictions, current_price, vest_price, shares_vested):
        print("\nStock Price Predicitons: ")
        for method, predicted_price in predictions.items():
            if predicted_price is not None:
                print(f"{method}:\t${predicted_price}")
                DisplayResults.show_analysis(method, predicted_price, current_price, vest_price, shares_vested)

    @staticmethod
    def show_analysis(method, predicted_price, current_price, vest_price, shares_vested):
        profit_results = calculate_profit(current_price=current_price, expected_price=predicted_price, shares_vested=shares_vested)
        gains_since_vesting = calculate_gains_since_vesting(vest_price=vest_price, current_price=current_price, shares_vested=shares_vested)
        required_gain = required_gain_to_offset_shorting_loss(profit_results["Short-Term Profit"], profit_results["Long-Term Profit"], shares_vested)

        for key, value in profit_results.items():
                formatted_value = f"${value:.2f}" if isinstance(value, (int, float)) else value
                print(f"{key}: {formatted_value}")

        print("\nGAINS SINCE VESTING:")
        for key, value in gains_since_vesting.items():
            formatted_value = f"${value:.2f}" if isinstance(value, (int, float)) else value
            print(f"{key}: {formatted_value}")

        print("\nREQUIRED PRICE INCREASE TO OFFSET SHORTING LOSS:")
        for key, value in required_gain.items():
            formatted_value = f"${value:.2f}" if isinstance(value, (int, float)) else value
            print(f"{key}: {formatted_value}")

        print("\n" + "-" * 25 + "\n")
    
def process_predictions(ticker_symbol, current_price, vest_price, shares_vested):
    """Processes stock predictions and delegates display to DisplayResults class."""
    forecaster = StockForecaster(ticker_symbol)
    predictions = forecaster.get_all_predications()
    DisplayResults.show_predictions(predictions, current_price, vest_price, shares_vested)

def get_user_inputs():
    """Handles user input for stock-related data."""
    ticker_symbol = input("Enter ticker symbol (e.g., AAPL): ").upper()
    vest_price = float(input("Enter stock price at vesting: "))
    shares_vested = float(input("Enter the number of vested shares: "))
    return ticker_symbol, vest_price, shares_vested

def main():
    """Main function to handle logic flow."""
    ticker_symbol, vest_price, shares_vested = get_user_inputs()
    current_price = get_stock_price(ticker_symbol=ticker_symbol)
    if current_price is None:
        e = logger.error("Could not retrieve stock price. Exiting.")
        return e

    process_predictions(ticker_symbol, current_price, vest_price, shares_vested)

if __name__ == "__main__":
    main()
