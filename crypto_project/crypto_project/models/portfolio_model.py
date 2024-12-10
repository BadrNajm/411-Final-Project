import logging
from typing import Dict
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Portfolio:
    def __init__(self, user_id: int, holdings: Dict[str, float]):
        """
        Initializes a portfolio with the user's cryptocurrency holdings.

        Args:
            user_id (int): The ID of the user.
            holdings (Dict[str, float]): A dictionary of cryptocurrency IDs and their quantities.
                                         Example: {"bitcoin": 1.5, "ethereum": 3.0}
        """
        self.user_id = user_id
        self.holdings = holdings

    def get_total_value(self, currency: str = 'USD') -> float:
        """
        Calculates the total value of the portfolio in the specified currency.

        Args:
            currency (str): The currency in which to calculate the portfolio value (default is 'USD').

        Returns:
            float: The total portfolio value.
        """
        total_value = 0.0
        for crypto_id, amount in self.holdings.items():
            price = self._get_crypto_price(crypto_id, currency)
            total_value += price * amount
        logging.info(f"Total portfolio value for user {self.user_id}: {total_value} {currency}")
        return total_value

    def get_portfolio_percentage(self) -> Dict[str, float]:
        """
        Calculates the percentage distribution of each cryptocurrency in the portfolio.

        Returns:
            Dict[str, float]: A dictionary with cryptocurrency IDs and their percentage in the portfolio.
        """
        total_value = self.get_total_value()
        percentages = {}
        for crypto_id, amount in self.holdings.items():
            price = self._get_crypto_price(crypto_id)
            value = price * amount
            percentages[crypto_id] = (value / total_value) * 100
        logging.info(f"Portfolio percentage breakdown for user {self.user_id}: {percentages}")
        return percentages

    def track_profit_loss(self, purchase_prices: Dict[str, float], currency: str = 'USD') -> Dict[str, float]:
        """
        Tracks profit or loss for each cryptocurrency based on purchase prices.

        Args:
            purchase_prices (Dict[str, float]): A dictionary with cryptocurrency IDs and their purchase prices.
            currency (str): The currency in which to calculate profit/loss (default is 'USD').

        Returns:
            Dict[str, float]: A dictionary with cryptocurrency IDs and their profit/loss amounts.
        """
        profit_loss = {}
        for crypto_id, amount in self.holdings.items():
            current_price = self._get_crypto_price(crypto_id, currency)
            purchase_price = purchase_prices.get(crypto_id, 0)
            profit_loss[crypto_id] = (current_price - purchase_price) * amount
        logging.info(f"Profit/loss for user {self.user_id}: {profit_loss}")
        return profit_loss

    def get_crypto_count(self, crypto_id: str) -> float:
        """
        Retrieves the number of units of a specific cryptocurrency in the portfolio.

        Args:
            crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').

        Returns:
            float: The number of units held.
        """
        count = self.holdings.get(crypto_id, 0.0)
        logging.info(f"User {self.user_id} holds {count} units of {crypto_id}")
        return count

    def _get_crypto_price(self, crypto_id: str, currency: str = 'USD') -> float:
        """
        Fetches the current price of a cryptocurrency using the CoinGecko API.

        Args:
            crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
            currency (str): The currency in which to get the price (default is 'USD').

        Returns:
            float: The current price of the cryptocurrency. Returns 0.0 if the price can't be fetched.
        """
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': crypto_id,
            'vs_currencies': currency.lower()
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises an exception for HTTP errors (e.g., 404, 500)
            
            data = response.json()
            price = data.get(crypto_id, {}).get(currency.lower(), None)

            if price is not None:
                logging.info(f"Fetched price for {crypto_id}: {price} {currency.upper()}")
                return price
            else:
                logging.error(f"Price for {crypto_id} in {currency.upper()} not found in response.")
                return 0.0

        except requests.RequestException as e:
            logging.error(f"Network error while fetching price for {crypto_id}: {e}")
            return 0.0
        except ValueError as e:
            logging.error(f"Invalid JSON response while fetching price for {crypto_id}: {e}")
            return 0.0

