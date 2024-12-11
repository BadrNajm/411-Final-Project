import hashlib
import logging
import os
import pyotp
from datetime import datetime
from typing import Dict, List, Optional
import requests
from sqlalchemy.exc import IntegrityError
from crypto_project.db import db
from crypto_project.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)


class CryptoDataModel:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.supported_intervals = ["1h", "24h", "7d", "30d", "1y"]
        logger.info("Initialized CryptoDataModel")

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
            logger.info(f"Requesting price for {crypto_id} from CoinGecko API")
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            if crypto_id in data and "usd" in data[crypto_id]:
                logger.info(f"Fetched price for {crypto_id}: {data[crypto_id]['usd']}")
                return float(data[crypto_id]["usd"])
            else:
                raise ValueError(f"Unexpected response structure: {data}")
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Failed to fetch price for {crypto_id}: {e}")
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
            logger.info(f"Requesting price trends for {crypto_id} over {days} days")
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            if "prices" in data:
                logger.info(f"Fetched price trends for {crypto_id}")
                return data
            logger.error(f"Unexpected structure for price trends: {data}")
            return None
        except requests.RequestException as e:
            logger.error(f"Request failed for price trends of {crypto_id}: {e}")
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
            logger.info(f"Requesting top {limit} performing cryptocurrencies")
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched top {limit} performing cryptocurrencies")
            return data
        except requests.RequestException as e:
            logger.error(f"Request failed for top performing cryptocurrencies: {e}")
            return []

    def set_price_alert(self, crypto_id: str, target_price: float) -> bool:
        """Set price alert for a specific cryptocurrency."""
        try:
            logger.info(f"Setting price alert for {crypto_id} at {target_price}")
            current_price = self.get_crypto_price(crypto_id)
            if current_price is None:
                logger.error(f"Cannot set alert: Could not fetch price for {crypto_id}.")
                return False

            alert = {
                'crypto_id': crypto_id,
                'target_price': target_price,
                'current_price': current_price,
                'timestamp': datetime.now().isoformat()
            }
            logger.info(f"Price alert set for {crypto_id}: {alert}")
            return True
        except Exception as e:
            logger.error(f"Error setting price alert for {crypto_id}: {e}")
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
            logger.info(f"Comparing {crypto_id1} vs {crypto_id2}")
            response = requests.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list) and len(data) == 2:
                logger.info(f"Comparison data for {crypto_id1} and {crypto_id2}: {data}")
                return {crypto_id1: data[0], crypto_id2: data[1]}
            logger.error(f"Unexpected structure for crypto comparison: {data}")
            return {}
        except requests.RequestException as e:
            logger.error(f"Request failed for crypto comparison {crypto_id1} vs {crypto_id2}: {e}")
            return {}
