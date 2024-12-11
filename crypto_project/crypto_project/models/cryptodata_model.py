#Functions for looking up specific crypto to get price, trends, leaderboard for top performing and worst performing cryptos, market cap rankings, compare two cryptos side by side (battle?), price alerts

import datetime
from typing import Dict, List, Optional
import requests

import logging

class CryptoDataModel:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.supported_intervals = ["1h", "24h", "7d", "30d", "1y"]

    def get_crypto_price(self, crypto_id: str) -> Optional[float]:
        """
        Get the current price of a specific cryptocurrency in USD.
        
        Args:
            crypto_id (str): The ID of the cryptocurrency (e.g., 'bitcoin').
            
        Returns:
            float: Current price in USD, or None if the request fails.
        """
        endpoint = f"/simple/price"
        params = {
            "ids": crypto_id,
            "vs_currencies": "usd"
        }
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            if crypto_id in data and "usd" in data[crypto_id]:
                return float(data[crypto_id]["usd"])
            else:
                raise ValueError(f"Unexpected response structure: {data}")
        except (requests.RequestException, ValueError) as e:
            logging.error(f"Failed to fetch price for {crypto_id}: {e}")
            return None


    def get_price_trends(self, crypto_id: str, days: str = "7") -> Optional[Dict]:
        """
        Get price trends for a specific cryptocurrency.
        Args:
            crypto_id (str): The ID of the cryptocurrency.
            days (str): Time range for trend data (e.g., '7', '30').
        Returns:
            dict: Price trend data or None if the request fails.
        """
        endpoint = f"/coins/{crypto_id}/market_chart"
        params = {
            "vs_currency": "usd",
            "days": days,
            "interval": "daily"
        }
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            if "prices" in data:
                return data
            logging.error(f"Unexpected structure for price trends: {data}")
            return None
        except requests.RequestException as e:
            logging.error(f"Request failed for price trends of {crypto_id}: {e}")
            return None

    def get_top_performing_cryptos(self, limit: int = 10) -> List[Dict]:
        """
        Get list of top performing cryptocurrencies.
        
        Args:
            limit (int): Number of cryptocurrencies to return
            
        Returns:
            list: List of top performing cryptocurrencies
        """
        endpoint = "/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "price_change_percentage_24h_desc",
            "per_page": limit,
            "page": 1
        }
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return []

    def set_price_alert(self, crypto_id: str, target_price: float) -> bool:
            """Set price alert for a specific cryptocurrency."""
            try:
                # Get current price to validate crypto_id and compare
                current_price = self.get_crypto_price(crypto_id)
                if current_price is None:
                    logging.error(f"Cannot set alert: Could not fetch price for {crypto_id}.")
                    return False

                alert = {
                    'crypto_id': crypto_id,
                    'target_price': target_price,
                    'current_price': current_price,
                    'timestamp': datetime.now().isoformat()
                }
                logging.info(f"Price alert set for {crypto_id}: {alert}")
                return True

            except Exception as e:
                logging.error(f"Error setting price alert for {crypto_id}: {e}")
                return False
    def compare_cryptos(self, crypto_id1: str, crypto_id2: str) -> Dict:
        """
        Compare two cryptocurrencies side by side.
        Args:
            crypto_id1 (str): First cryptocurrency ID.
            crypto_id2 (str): Second cryptocurrency ID.
        Returns:
            dict: Comparison data for both cryptocurrencies or an empty dict.
        """
        endpoint = "/coins/markets"
        params = {
            "vs_currency": "usd",
            "ids": f"{crypto_id1},{crypto_id2}",
            "order": "market_cap_desc",
            "per_page": 2,
            "page": 1
        }
        try:
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) == 2:
                return {crypto_id1: data[0], crypto_id2: data[1]}
            logging.error(f"Unexpected structure for crypto comparison: {data}")
            return {}
        except requests.RequestException as e:
            logging.error(f"Request failed for crypto comparison {crypto_id1} vs {crypto_id2}: {e}")
            return {}