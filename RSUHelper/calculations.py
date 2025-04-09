import yfinance as yf
from typing import Dict, Any
from datetime import datetime, timedelta

def calculate_profit(current_price: float, expected_price: float, shares_vested: float | int, short_term_tax=0.37, long_term_tax=0.2) -> Dict[str, Any]:
    ''' Calculate short-term vs. long-term profists and delta'''

    short_term_profit = (current_price * shares_vested) * (1 - short_term_tax)
    long_term_profit = (expected_price * shares_vested) * (1 - long_term_tax)

    # Delta: Profit or loss difference from holding
    delta = long_term_profit - short_term_profit
    recommendation = "HOLD" if long_term_profit > short_term_profit else "SHORT"

    return {
        "Short-Term Profit": short_term_profit,
        "Long-Term Profit": long_term_profit,
        "Delta (Hold vs Short)": delta,
        "Recommendation": recommendation
    }

def calculate_gains_since_vesting(vest_price: float | int, current_price: float | int, shares_vested: int | float) -> Dict[str, Any]:
    '''Calculate gain/loss since vesting'''

    gain_per_share = current_price - vest_price
    total_gain = gain_per_share * shares_vested

    return {
        "Per Share Gain": gain_per_share,
        "Total Gain Since Vesting": total_gain
    }

def get_vest_price(ticker_symbol: str, vesting_date: str) -> float | None:
    """Fetches the stock price oin the vesting date using Yahoo Finance"""
    try:
        vesting_date_obj = datetime.strptime(vesting_date, "%Y-%m-%d")
        today = datetime.today()

        # Ensuring vesting date is in the past
        if vesting_date_obj >= today:
            e = logger.error("Error: Vesting date cannot be in the future")
            print(e)
            return None

        stock = yf.Ticker(ticker_symbol)

        end_date = (vesting_date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
        history = stock.history(start=vesting_date, end=end_date)

        # In the event of no data, look for the nearest prior trading day (up to 10 days back)
        days_back = 1
        while history.empty and days_back < 10:
            new_date = vesting_date_obj - timedelta(days=days_back)
            new_end_date = (new_date + timedelta(days=1)).strftime("%Y-%m-%d")
            history = stock.history(start=new_date.strftime("%Y-%m-%d"), end=new_end_date)
            days_back += 1

        if not history.empty:
            return round(history["Close"].iloc[0], 2)

        if vesting_price is not None and not vesting_price.empty:
            return round(vesting_price.iloc[0], 2)

    except Exception as e:
        print(f"Error fetching vesting price: {e}")

    return None

def required_gain_to_offset_shorting_loss(short_term_profit: float | int, long_term_profit: float | int, shares_vested: float | int) -> Dict[str, Any]:
    ''' Calculates price increase needed to make holding a better option. '''
    
    if long_term_profit > short_term_profit:
        return {
            "Holding Already Better": True,
            "Required Price Increase": 0
        }
    
    loss = short_term_profit - long_term_profit
    required_price_increase = loss / (shares_vested * (1 - 0.2)) # Accounting for long-term tax
    return {
        "Holding Already Better": False,
        "Required Price Increase": round(required_price_increase, 2)
    }