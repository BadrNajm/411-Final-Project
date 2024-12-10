import pytest
from crypto_project.models.cryptodata_model import CryptoDataModel

def test_get_crypto_price():
    model = CryptoDataModel()
    price = model.get_crypto_price("bitcoin")
    assert price is not None
    assert isinstance(price, float)

def test_get_price_trends():
    model = CryptoDataModel()
    trends = model.get_price_trends("bitcoin")
    assert trends is not None
    assert "prices" in trends

def test_get_top_performing_cryptos():
    model = CryptoDataModel()
    top_cryptos = model.get_top_performing_cryptos()
    assert isinstance(top_cryptos, list)
    assert len(top_cryptos) <= 10