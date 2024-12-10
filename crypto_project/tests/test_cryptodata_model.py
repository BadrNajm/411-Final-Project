import pytest
from crypto_project.models.cryptodata_model import CryptoDataModel
from unittest.mock import patch

def test_get_crypto_price():
    model = CryptoDataModel()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"bitcoin": {"usd": 29000.0}}
        price = model.get_crypto_price("bitcoin")
        assert price == 29000.0

def test_get_price_trends():
    model = CryptoDataModel()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"prices": [[1609459200000, 29000.0]]}
        trends = model.get_price_trends("bitcoin")
        assert trends is not None
        assert "prices" in trends
        assert isinstance(trends["prices"], list)
        assert len(trends["prices"]) > 0

def test_get_top_performing_cryptos():
    model = CryptoDataModel()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": "bitcoin", "price_change_percentage_24h": 5.0},
            {"id": "ethereum", "price_change_percentage_24h": 3.0},
        ]
        top_cryptos = model.get_top_performing_cryptos()
        assert isinstance(top_cryptos, list)
        assert len(top_cryptos) == 2
        assert "id" in top_cryptos[0]
        assert "price_change_percentage_24h" in top_cryptos[0]

def test_compare_cryptos():
    model = CryptoDataModel()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {"id": "bitcoin", "current_price": 29000.0},
            {"id": "ethereum", "current_price": 1800.0},
        ]
        comparison = model.compare_cryptos("bitcoin", "ethereum")
        assert isinstance(comparison, dict)
        assert "bitcoin" in comparison
        assert comparison["bitcoin"]["current_price"] == 29000.0
        assert "ethereum" in comparison
        assert comparison["ethereum"]["current_price"] == 1800.0

def test_get_crypto_price_error_handling():
    model = CryptoDataModel()
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 404
        price = model.get_crypto_price("invalid-crypto")
        assert price is None
