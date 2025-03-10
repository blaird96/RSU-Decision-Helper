# RSU-Decision-Helper

## Overview

RSU-Decision-Helper is a Python-based tool designed to help employees analyze whether they should sell their Restricted Stock Units (RSUs) immediately or hold them for at least one year to take advantage of long-term capital gains tax rates.

## Features
* Calculates net profit for short-term (selling immediately) and long-term (holding for a year) scenarios.
* Uses customizable tax rates for short-term and long-term capital gains.
* Provides a recommendation based on which option yields a higher net return.
* Simple command-line input for ease of use.
* Expandable to include stock price forecasting or Monte Carlo simulations in the future.

## Installation
Ensure you have Python installed (Python 3.x recommended). Then, clone the repository:
```
$ git clone https://github.com/yourusername/RSU-Decision-Helper.git
$ cd RSU-Decision-Helper
```

## Usage
Run the script and input stock data when prompted:
`$ python rsu_decision_helper.py`

The script will ask for:
* Current stock price (the price of the stock today)
* Expected stock price after 1 year (your best estimate or a target price)
* Number of vested shares (how many RSUs you own)

**Example:**
```
Enter current stock price: 150
Enter expected stock price in 1 year: 180
Enter number of vested shares: 100
```
**Sample Output**
```
Short-Term Profit (Immediate Sale): $9,450.00
Long-Term Profit (Hold 1 Year): $14,400.00
Recommendation: HOLD
```

## Code Example
```
def calculate_profit(current_price, expected_price, shares_vested, short_term_tax=0.37, long_term_tax=0.20):
    short_term_profit = (current_price * shares_vested) * (1 - short_term_tax)
    long_term_profit = (expected_price * shares_vested) * (1 - long_term_tax)
    recommendation = "HOLD" if long_term_profit > short_term_profit else "SHORT"
    return {"Short-Term Profit": short_term_profit, "Long-Term Profit": long_term_profit, "Recommendation": recommendation}
```

## Future Enhancements
* Implement a Monte Carlo simulation for stock price projections.
* Allow users to enter different tax brackets based on personal income.
* Add a GUI or web interface for easier interaction.

## Contributions

Contributions are welcome! Feel free to fork this repository and submit a pull request with improvements.

## License
This project is licensed under the MIT License.

## Author

Developed by Laird, Brendan M.

