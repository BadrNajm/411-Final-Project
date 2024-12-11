import logging
from typing import Dict, Optional
from crypto_project.models.cryptodata_model import CryptoDataModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Portfolio:
    def __init__(self, user_id: int, holdings: Dict[str, float], cash_balance: float):
        """
        Initializes a portfolio with the user's cryptocurrency holdings.

        Args:
            user_id (int): The ID of the user.
            holdings (Dict[str, float]): A dictionary of cryptocurrency IDs and their quantities.
                                         Example: {"bitcoin": 1.5, "ethereum": 3.0}
            cash_balance (float): The user's cash balance in USD.                             
        """
        self.user_id = user_id
        self.holdings = holdings
        self.cash_balance = cash_balance
        self.crypto_data = CryptoDataModel()  # Centralized API interaction

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
            try:
                price = self.crypto_data.get_crypto_price(crypto_id)  # Fetch price using CryptoDataModel
                if price is not None:
                    total_value += price * amount
            except Exception as e:
                logging.error(f"Error fetching price for {crypto_id}: {e}")
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
            price = self.crypto_data.get_crypto_price(crypto_id)  # Fetch price using CryptoDataModel
            if price is not None and total_value > 0:
                value = price * amount
                percentages[crypto_id] = (value / total_value) * 100
        logging.info(f"Portfolio percentage breakdown for user {self.user_id}: {percentages}")
        return percentages

    def track_profit_loss(self, purchase_prices: Dict[str, float]) -> Dict[str, float]:
        """
        Tracks profit or loss for each cryptocurrency based on purchase prices.

        Args:
            purchase_prices (Dict[str, float]): A dictionary with cryptocurrency IDs and their purchase prices.

        Returns:
            Dict[str, float]: A dictionary with cryptocurrency IDs and their profit/loss amounts.
        """
        profit_loss = {}
        for crypto_id, amount in self.holdings.items():
            current_price = self.crypto_data.get_crypto_price(crypto_id)  # Fetch price using CryptoDataModel
            purchase_price = purchase_prices.get(crypto_id, 0)
            if current_price is not None:
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

    @classmethod
    def get_user_portfolio(cls, user_id: int) -> Optional['Portfolio']:
        """
        Retrieves the portfolio for a given user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Portfolio: The user's portfolio instance, or None if not found.
        """
        portfolio = cls.query.filter_by(user_id=user_id).first()
        if not portfolio:
            raise ValueError(f"No portfolio found for user ID {user_id}.")
        return portfolio

    def get_cash_balance(self) -> float:
        """
        Retrieves the user's current cash balance.

        Returns:
            float: The user's available fiat currency balance.
        """
        return self.cash_balance

    def adjust_cash_balance(self, amount: float) -> None:
        """
        Adjusts the user's cash balance.

        Args:
            amount (float): The amount to adjust (positive for deposits, negative for spending).

        Raises:
            ValueError: If the adjustment results in a negative balance.
        """
        new_balance = self.cash_balance + amount
        if new_balance < 0:
            raise ValueError("Insufficient cash balance.")
        self.cash_balance = new_balance

    def validate_cash_for_purchase(self, total_cost: float) -> bool:
        """
        Validates if the user has enough cash for a purchase.

        Args:
            total_cost (float): The total cost of the purchase.

        Returns:
            bool: True if the user has sufficient balance, False otherwise.
        """
        return self.cash_balance >= total_cost
