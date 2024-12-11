import pytest
from unittest.mock import MagicMock, patch
from crypto_project.models.portfolio_model import Portfolio
from crypto_project.models.transaction_model import TransactionModel
from datetime import datetime, timedelta



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
            price=sample_transaction_data["price"],  # Explicitly passing the price
        )

        assert transaction.total_value == 1000.0
        mock_portfolio.adjust_cash_balance.assert_called_once_with(-1000.0)
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()


def test_create_transaction_sell_valid(mock_db_session, sample_transaction_data):
    """Test creating a valid sell transaction."""
    mock_portfolio = MagicMock(spec=Portfolio)
    mock_portfolio.get_crypto_count.return_value = 5.0
    mock_portfolio.adjust_cash_balance.return_value = None
    mock_portfolio.holdings = {"bitcoin": 5.0}

    with patch("crypto_project.models.portfolio_model.Portfolio.get_user_portfolio", return_value=mock_portfolio):
        sample_transaction_data["transaction_type"] = "sell"
        transaction = TransactionModel.create_transaction(
            user_id=sample_transaction_data["user_id"],
            crypto_id=sample_transaction_data["crypto_id"],
            transaction_type=sample_transaction_data["transaction_type"],
            quantity=sample_transaction_data["quantity"],
            price=sample_transaction_data["price"],  # Explicitly passing the price
        )

        assert transaction.total_value == 1000.0
        mock_portfolio.adjust_cash_balance.assert_called_once_with(1000.0)
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()


def test_create_transaction_invalid_input(sample_transaction_data):
    """Test creating a transaction with invalid input."""
    with pytest.raises(ValueError, match="Quantity must be a positive number"):
        TransactionModel.create_transaction(
            user_id=sample_transaction_data["user_id"],
            crypto_id=sample_transaction_data["crypto_id"],
            transaction_type=sample_transaction_data["transaction_type"],
            quantity=-1.0,
            price=sample_transaction_data["price"],  # Explicitly passing the price
        )


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
                price=sample_transaction_data["price"],  # Explicitly passing the price
            )

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

############################################################
# edit_transaction
############################################################

def test_edit_transaction_valid(mock_db_session):
    """Test editing a transaction."""
    mock_transaction = MagicMock()
    with patch("crypto_project.models.transaction_model.TransactionModel.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = mock_transaction

        updated_transaction = TransactionModel.edit_transaction(
            transaction_id=1, target_price=600.0
        )

        assert updated_transaction.target_price == 600.0
        mock_db_session.commit.assert_called_once()

def test_edit_transaction_invalid(mock_db_session):
    """Test editing a transaction that does not exist."""
    with patch("crypto_project.models.transaction_model.TransactionModel.query") as mock_query:
        mock_query.filter_by.return_value.first.return_value = None  # No transaction found

        with pytest.raises(ValueError, match="Transaction with ID 999 not found or inactive"):
            TransactionModel.edit_transaction(transaction_id=999, target_price=600.0)

        # Assert no db operations occurred
        mock_db_session.commit.assert_not_called()



############################################################
# execute_custom_transactions
############################################################

def test_execute_custom_transactions(mock_db_session):
    """Test executing custom transactions."""
    mock_transaction = MagicMock()
    mock_transaction.transaction_type = "buy"
    mock_transaction.target_price = 500.0
    mock_transaction.crypto_id = "bitcoin"
    mock_transaction.active = True

    with patch("crypto_project.models.transaction_model.TransactionModel.query") as mock_query, \
         patch("crypto_project.models.cryptodata_model.CryptoDataModel.get_crypto_price", return_value=400.0):

        mock_query.filter_by.return_value.filter.return_value.all.return_value = [mock_transaction]
        TransactionModel.execute_custom_transactions()

        assert not mock_transaction.active
        mock_db_session.commit.assert_called_once()

############################################################
# execute_recurring_transactions
############################################################



def test_execute_recurring_transactions(mock_db_session):
    """Test executing recurring transactions."""

    class MockTransaction:
        def __init__(self):
            self.recurring = True
            self.active = True
            self.timestamp = datetime.utcnow() - timedelta(days=1)

        def save(self):
            self.timestamp = datetime.utcnow()

    mock_transaction = MockTransaction()

    with patch("crypto_project.models.transaction_model.TransactionModel.query") as mock_query:
        mock_query.filter_by.return_value.filter_by.return_value.all.return_value = [mock_transaction]

        
        with patch("crypto_project.models.transaction_model.db.session.commit", mock_db_session.commit):
            TransactionModel.execute_recurring_transactions()

            
            mock_transaction.save()

            # Assert that the timestamp was updated to a later time
            assert mock_transaction.timestamp > datetime.utcnow() - timedelta(seconds=2)
            mock_db_session.commit.assert_called_once()