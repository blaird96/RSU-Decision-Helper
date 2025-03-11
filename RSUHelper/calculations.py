import yfinance as yf
from typing import Dict, Any

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


def get_moving_average(ticker_symbol: str, period="50d") -> float:
    stock = yf.Ticker(ticker_symbol)
    history = stock.histroy(period=period)
    return round(history["Close"].mean(), 2)

def calculate_gains_since_vesting(vest_price: float | int, current_price: float | int, shares_vested: int | float) -> Dict[str, Any]:
    '''Calculate gain/loss since vesting'''

    gain_per_share = current_price - vest_price
    total_gain = gain_per_share * shares_vested

    return {
        "Per Share Gain": gain_per_share,
        "Total Gain Since Vesting": total_gain
    }

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