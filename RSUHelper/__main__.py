import logging

# Local Imports
from .stock_price import get_stock_price
from .arguments import get_user_input
from .calculations import (
    calculate_profit,
    calculate_gains_since_vesting,
    required_gain_to_offset_shorting_loss
)

# Initializing logger
logger = logging.getLogger(__name__)

def main():
    """Main function to handle logic flow."""
    
    ticker_symbol = input("Enter stock ticker symbol (e.g., AAPL): ").upper()
    vest_price = float(input("Enter stock price at vesting: "))
    shares_vested = float(input("Enter number of vested shares: "))

    current_price = get_stock_price(ticker_symbol=ticker_symbol)
    if current_price is None:
        e = logger.error("Could not retrieve stock price. Exiting")
        return e
    
    expected_price = float(input(f"Enter expected stock price in 1 year (current: {current_price})\t"))

    # Computing profit/loss scenarios
    profit_results = calculate_profit(current_price=current_price, expected_price=expected_price, shares_vested=shares_vested)
    gains_since_vesting = calculate_gains_since_vesting(vest_price=vest_price, current_price=current_price, shares_vested=shares_vested)
    required_gain = required_gain_to_offset_shorting_loss(profit_results["Short-Term Profit"], profit_results["Long-Term Profit"], shares_vested)

    # Display results
    print("\nRESULTS:")
    for key, value in profit_results.items():
        print(f"{key}: ${value}")

    print("\nGAINS SINCE VESTING:")
    for key, value in gains_since_vesting.items():
        print(f"{key}: ${value}")

    print("\nREQUIRED PRICE INCREASE TO OFFSET SHORTING LOSS:")
    for key, value in required_gain.items():
        if isinstance(value, bool):
            print(f"{key}: {value}")
        else:
            print(f"{key}: ${value}")



if __name__ == "__main__":
    main()
