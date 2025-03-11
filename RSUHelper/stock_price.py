import yfinance as yf
import logging

# Instantiating logging
logger = logging.getLogger(__name__)


def get_stock_price(ticker_symbol: str) -> float | None:
    '''Fetches the current stock price using the Finance API'''

    try: 
        stock = yf.Ticker(ticker_symbol)
        history = stock.history(period="1d")
        closing_price = history.get("Close")

        if closing_price is not None and not closing_price.empty:
            price = closing_price.iloc[-1]
        else:
            price = None

        return round(price, 2) if price is not None else None
    
    except Exception as e:
        logger.error(f"Error fetching stock price for {ticker_symbol}:\t{e}")
        return None