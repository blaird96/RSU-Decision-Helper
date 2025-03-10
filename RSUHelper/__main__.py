from arguments import get_user_input
from calculations import calculate_profit

def main():
    """Main function to handle logic flow."""
    current_price, expected_price, shares_vested = get_user_input()
    result = calculate_profit(current_price, expected_price, shares_vested)

    print("\nRESULTS:")
    for key, value in result.items():
        print(f"{key}: ${value:,.2f}")

if __name__ == "__main__":
    main()
