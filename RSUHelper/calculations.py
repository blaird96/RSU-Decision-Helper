def calculate_profit(current_price, expected_price, shares_vested, short_term_tax=0.37, long_term_tax=0.20):
    """Calculate profits and determine whether to hold or sell."""
    short_term_profit = (current_price * shares_vested) * (1 - short_term_tax)
    long_term_profit = (expected_price * shares_vested) * (1 - long_term_tax)

    recommendation = "HOLD" if long_term_profit > short_term_profit else "SHORT"

    return {
        "Short-Term Profit": short_term_profit,
        "Long-Term Profit": long_term_profit,
        "Recommendation": recommendation
    }
