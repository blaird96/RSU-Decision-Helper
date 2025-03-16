def get_user_input():
    """Prompt user for stock information and return values."""
    try:
        current_price = float(input("Enter current stock price: "))
        expected_price = float(input("Enter expected stock price in 1 year: "))
        shares_vested = int(input("Enter number of vested shares: "))
        return current_price, expected_price, shares_vested
    
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return get_user_input()
