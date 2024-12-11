import pytest
from unittest.mock import patch
from crypto_project.models.portfolio_model import Portfolio

@pytest.fixture
def portfolio():
    """Fixture to create a Portfolio instance with sample holdings and cash balance."""
    return Portfolio(user_id=1, holdings={"bitcoin": 2, "ethereum": 3}, cash_balance=1000.0)

@pytest.fixture
def mock_get_crypto_price():
    """Fixture to mock the CryptoDataModel.get_crypto_price method."""
    with patch('crypto_project.models.cryptodata_model.CryptoDataModel.get_crypto_price') as mock_price:
        yield mock_price

######################################################
#
#    Tests for Total Portfolio Value
#
######################################################

def test_get_total_value(portfolio, mock_get_crypto_price):
    """Test calculating the total portfolio value."""
    mock_get_crypto_price.side_effect = lambda crypto_id: {"bitcoin": 100.0, "ethereum": 200.0}[crypto_id]
    total_value = portfolio.get_total_value()
    assert total_value == 800.0  # (2 * 100) + (3 * 200)

def test_get_total_value_with_api_error(portfolio, mock_get_crypto_price):
    """Test total portfolio value calculation with API errors."""
    mock_get_crypto_price.side_effect = Exception("Network error")
    total_value = portfolio.get_total_value()
    assert total_value == 0.0  # Should handle the error gracefully

######################################################
#
#    Tests for Portfolio Percentage
#
######################################################

def test_get_portfolio_percentage(portfolio, mock_get_crypto_price):
    """Test calculating the portfolio percentage distribution."""
    mock_get_crypto_price.side_effect = lambda crypto_id: {"bitcoin": 100.0, "ethereum": 100.0}[crypto_id]
    percentages = portfolio.get_portfolio_percentage()
    assert percentages == {"bitcoin": 40.0, "ethereum": 60.0}

######################################################
#
#    Tests for Profit/Loss Calculation
#
######################################################

def test_track_profit_loss(portfolio, mock_get_crypto_price):
    """Test calculating profit or loss for each cryptocurrency."""
    mock_get_crypto_price.side_effect = lambda crypto_id: {"bitcoin": 150.0, "ethereum": 250.0}[crypto_id]
    purchase_prices = {"bitcoin": 100.0, "ethereum": 200.0}
    profit_loss = portfolio.track_profit_loss(purchase_prices)
    assert profit_loss == {"bitcoin": 100.0, "ethereum": 150.0}

######################################################
#
#    Tests for Crypto Count
#
######################################################

def test_get_crypto_count(portfolio):
    """Test retrieving the number of units of a specific cryptocurrency."""
    assert portfolio.get_crypto_count("bitcoin") == 2.0
    assert portfolio.get_crypto_count("ethereum") == 3.0
    assert portfolio.get_crypto_count("dogecoin") == 0.0

######################################################
#
#    Tests for Error Handling
#
######################################################

def test_get_total_value_invalid_data(portfolio, mock_get_crypto_price):
    """Test handling invalid data from the API."""
    mock_get_crypto_price.side_effect = lambda crypto_id: None
    total_value = portfolio.get_total_value()
    assert total_value == 0.0
