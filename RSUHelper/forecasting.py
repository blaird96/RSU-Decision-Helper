import numpy as np
import pandas as pd
import yfinance as yf
import logging

# Statistical Modeling Imports
from arch import arch_model
from statsmodels.tsa.arima.model import ARIMA as arima

# Initializing logging
logger = logging.getLogger(__name__)

class StockForecaster:
    def __init__(self, ticker_symbol: str, period="2y", simulations=1000, arima_order=(5, 1, 0)):
        self.ticker_symbole = ticker_symbol
        self.stock = yf.Ticker(ticker_symbol)
        self.history = self.stock.history(period=period)
        self.rng = np.random.default_rng(0)
        self.preprocessing_data()
        self.simulations = simulations
        self.arima_order = arima_order
        self.preprocessing_data()

    def preprocessing_data(self):
        """Prepares historical data for forecasting models."""
        if self.history.empty:
            logger.error("Insufficient datra for preprocessing.")
        
        # Standardizing date index for ARIMA
        if not isinstance(self.history.index, pd.PeriodIndex):
            self.history.index = pd.DatetimeIndex(self.history.index).tz_localize(None).to_period("D")

        # Scale returns for GARCH (if applicable)
        if "Close" in self.history.columns:
            self.history["Scaled Returns"] =self.history["Close"].pct_change().dropna() * 100  # Scaling for better optimizer performance


    def get_moving_average(self, period=50) -> float:
        ''' Retires the moving average; default period is 50 days'''
        return round(self.history["Close"].rolling(window=period).mean().iloc[-1], 2)  #NTS: iloc retrieves last line from a df (-1)


    def get_exponential_moving_get_moving_average(self, span=50) -> float:
        ema = self.history["Close"].ewm(span=span, adjust=False).mean()
        return round(ema.iloc[-1], 2)
    
    def predict_arima(self) -> float | None:
        if self.history.empty:
            logger.error("Insufficient data for ARIMA.")
            return None
        
        model = arima(self.history["Close"], order=(self.arima_order))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=252)  # Predict 252 represents the number of trading days.
        return round(forecast.iloc[-1], 2)
    
    def predict_garch(self) -> float | None:
        ''' Provides analysis with an emphasis on volatility '''
        if self.history.empty:
            logger.error("Insufficient data for GARCH.")
        
        returns = self.history["Scaled Returns"].dropna()
        garch = arch_model(returns, vol='Garch', p=1, q=1)  # GARCH(1,1) is the most commonly used GARCH method in financial analysis due to financial clustering.
        garch_fit = garch.fit(disp="off")
        forecast = garch_fit.forecast(horizon=252)
        expected_return = forecast.mean.iloc[-1, -1]
        last_price = self.history["Close"].iloc[-1]
        return round(last_price * (1 + expected_return), 2)
    

    def monte_carlo_simulation(self, days=252) -> float | None:
        ''' Statistical method reliant on a normal distribution '''

        if self.history.empty:
            logger.error("Insufficient data for Monte Carlo simulation.")
            return None
        
        log_returns = np.log(1 + self.history["Close"]).pct_change().dropna()
        drift = log_returns.mean() - (0.5 * log_returns.var())
        volatility = log_returns.std()
        last_price = self.history["Close"].iloc[-1]

        future_prices = np.zeros(self.simulations)
        for i in range(self.simulations):
            daily_returns = self.rng.normal(drift, volatility, days)
            price_series = last_price * np.exp(np.cumsum(daily_returns))
            future_prices[i] = price_series[-1]

        return round(np.mean(future_prices), 2)
    
    def get_all_predications(self):
        predictions = {
            "Moving Average (50d)": self.get_moving_average(),
            "Exponential Moving Average (50d)": self.get_exponential_moving_get_moving_average(),
            "ARIMA Prediction": self.predict_arima(),
            "GARCH Prediction": self.predict_garch(),
            "Monte Carlo Simulation": self.monte_carlo_simulation(days=252) 
        }

        return predictions
