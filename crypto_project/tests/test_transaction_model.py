import pytest
from unittest.mock import MagicMock, patch
from crypto_project.models.portfolio_model import Portfolio
from crypto_project.models.transaction_model import TransactionModel


@pytest.fixture
def mock_portfolio():
    """Mock Portfolio methods."""
    portfolio = MagicMock(spec=Portfolio)
    portfolio.get_cash_balance.return_value = 1000.0
    portfolio.get_crypto_count.return_value = 5.0
    portfolio.validate_cash_for_purchase.return_value = True
    return portfolio


@pytest.fixture
def mock_db_session(mocker):
    """Mock db.session methods."""
    session = mocker.patch("crypto_project.models.transaction_model.db.session")
    return session


@pytest.fixture
def sample_transaction_data():
    """Fixture to provide sample transaction data."""
    return {
        "user_id": 1,
        "crypto_id": "bitcoin",
        "transaction_type": "buy",
        "quantity": 2.0,
        "price": 500.0,
    }


############################################################
# create_transaction
############################################################

def test_create_transaction_buy_valid(mock_db_session, sample_transaction_data):
    """Test creating a valid buy transaction."""
    # Mock Portfolio.get_user_portfolio
    mock_portfolio = MagicMock(spec=Portfolio)
    mock_portfolio.validate_cash_for_purchase.return_value = True
    mock_portfolio.get_cash_balance.return_value = 1000.0
    mock_portfolio.adjust_cash_balance.return_value = None
    mock_portfolio.holdings = {"bitcoin": 1.0}

    with patch("crypto_project.models.portfolio_model.Portfolio.get_user_portfolio", return_value=mock_portfolio):
        transaction = TransactionModel.create_transaction(
            user_id=sample_transaction_data["user_id"],
            crypto_id=sample_transaction_data["crypto_id"],
            transaction_type=sample_transaction_data["transaction_type"],
            quantity=sample_transaction_data["quantity"],
            price=sample_transaction_data["price"],
        )

        # Assert transaction was created
        assert transaction.user_id == sample_transaction_data["user_id"]
        assert transaction.crypto_id == sample_transaction_data["crypto_id"]
        assert transaction.transaction_type == sample_transaction_data["transaction_type"]
        assert transaction.quantity == sample_transaction_data["quantity"]
        assert transaction.price == sample_transaction_data["price"]
        assert transaction.total_value == 1000.0

        # Assert portfolio and db operations
        mock_portfolio.adjust_cash_balance.assert_called_once_with(-1000.0)
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()


def test_create_transaction_buy_insufficient_funds(sample_transaction_data):
    """Test creating a buy transaction with insufficient funds."""
    mock_portfolio = MagicMock(spec=Portfolio)
    mock_portfolio.validate_cash_for_purchase.return_value = False

    with patch("crypto_project.models.portfolio_model.Portfolio.get_user_portfolio", return_value=mock_portfolio):
        with pytest.raises(ValueError, match="Insufficient cash balance"):
            TransactionModel.create_transaction(
                user_id=sample_transaction_data["user_id"],
                crypto_id=sample_transaction_data["crypto_id"],
                transaction_type=sample_transaction_data["transaction_type"],
                quantity=sample_transaction_data["quantity"],
                price=sample_transaction_data["price"],
            )

        # Assert no db operations occurred
        mock_portfolio.adjust_cash_balance.assert_not_called()


############################################################
# delete_transaction
############################################################

def test_delete_transaction_valid(mock_db_session):
    """Test deleting a transaction."""
    mock_transaction = MagicMock()
    mock_transaction.id = 1
    mock_transaction.active = True

    with patch("crypto_project.models.transaction_model.TransactionModel.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_transaction

        TransactionModel.delete_transaction(1)

        # Assert transaction was soft-deleted
        assert mock_transaction.active is False
        mock_db_session.commit.assert_called_once()


def test_delete_transaction_invalid(mock_db_session):
    """Test deleting a transaction that does not exist."""
    with patch("crypto_project.models.transaction_model.TransactionModel.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = None

        with pytest.raises(ValueError, match="Transaction with ID 999 not found or already inactive"):
            TransactionModel.delete_transaction(999)

        # Assert no db operations occurred
        mock_db_session.commit.assert_not_called()
