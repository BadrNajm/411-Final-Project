from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from crypto_project.db import db
from crypto_project.models.portfolio_model import Portfolio
from crypto_project.models.cryptodata_model import CryptoDataModel
import logging

class TransactionModel(db.Model):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    crypto_id = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)  # "buy" or "sell"
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    target_price = Column(Float, nullable=True)  # For custom buy/sell
    recurring = Column(Boolean, default=False)  # For recurring transactions
    active = Column(Boolean, default=True)  # For pending or recurring transactions

    def __init__(self, user_id, crypto_id, transaction_type, quantity, price, target_price=None, recurring=False):
        self.user_id = user_id
        self.crypto_id = crypto_id
        self.transaction_type = transaction_type
        self.quantity = quantity
        self.price = price
        self.total_value = price * quantity
        self.target_price = target_price
        self.recurring = recurring

    @classmethod
    def create_transaction(cls, user_id, crypto_id, transaction_type, quantity, price, target_price=None, recurring=False):
        """
        Create a new transaction (buy/sell) for a user.

        Args:
            user_id (int): The ID of the user making the transaction.
            crypto_id (str): The ID of the cryptocurrency being traded.
            transaction_type (str): The type of transaction ("buy" or "sell").
            quantity (float): The quantity of the cryptocurrency being traded.
            price (float): The current price of the cryptocurrency.
            target_price (float, optional): The target price for a custom buy/sell transaction.
            recurring (bool, optional): Whether the transaction is recurring (e.g., daily).

        Returns:
            TransactionModel: The newly created transaction.

        Raises:
            ValueError: If the transaction is invalid.
        """
        if quantity <= 0:
            raise ValueError("Quantity must be a positive number.")
        if transaction_type not in ["buy", "sell"]:
            raise ValueError("Transaction type must be 'buy' or 'sell'.")

        # Fetch user's portfolio
        user_portfolio = Portfolio.get_user_portfolio(user_id)

        if transaction_type == "buy":
            total_cost = quantity * price
            if not user_portfolio.validate_cash_for_purchase(total_cost):
                raise ValueError("Insufficient cash balance.")
            user_portfolio.adjust_cash_balance(-total_cost)
            user_portfolio.holdings[crypto_id] = user_portfolio.holdings.get(crypto_id, 0) + quantity

        elif transaction_type == "sell":
            user_crypto_balance = user_portfolio.get_crypto_count(crypto_id)
            if quantity > user_crypto_balance:
                raise ValueError("Insufficient cryptocurrency balance.")
            user_portfolio.holdings[crypto_id] -= quantity
            if user_portfolio.holdings[crypto_id] <= 0:
                del user_portfolio.holdings[crypto_id]
            total_revenue = quantity * price
            user_portfolio.adjust_cash_balance(total_revenue)

        # Create and save the transaction
        new_transaction = cls(
            user_id=user_id,
            crypto_id=crypto_id,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            target_price=target_price,
            recurring=recurring
        )
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction


    @classmethod
    def edit_transaction(cls, transaction_id, **kwargs):
        """
        Edit an existing transaction (e.g., update target price or quantity).

        Args:
            transaction_id (int): The ID of the transaction to edit.
            **kwargs: The attributes to update.

            Raises:
                ValueError: If the transaction ID is invalid or the attribute is not found.

        Returns:
                TransactionModel: The updated transaction.
        """
        logging.info(f"Editing transaction {transaction_id} with updates {kwargs}.")
        transaction = cls.query.filter_by(id=transaction_id, active=True).first()
        if not transaction:
            logging.error(f"Transaction with ID {transaction_id} not found or inactive.")
            raise ValueError(f"Transaction with ID {transaction_id} not found or inactive.")

        for key, value in kwargs.items():
            if hasattr(transaction, key):
                setattr(transaction, key, value)
                logging.info(f"Updated {key} to {value}.")
            else:
                logging.error(f"Invalid attribute: {key}")
                raise ValueError(f"Invalid attribute: {key}")
        db.session.commit()
        logging.info(f"Transaction {transaction_id} updated successfully.")
        return transaction

    @classmethod
    def delete_transaction(cls, transaction_id):
        """
        Soft-delete a transaction by marking it as inactive.

        Args:
            transaction_id (int): The ID of the transaction to delete.

            Raises:
                ValueError: If the transaction ID is invalid or the transaction is already inactive.

        Returns:
            None
        """
        logging.info(f"Deleting transaction {transaction_id}.")
        transaction = cls.query.filter_by(id=transaction_id, active=True).first()
        if not transaction:
            logging.error(f"Transaction with ID {transaction_id} not found or already inactive.")
            raise ValueError(f"Transaction with ID {transaction_id} not found or already inactive.")

        transaction.active = False
        db.session.commit()
        logging.info(f"Transaction {transaction_id} marked as inactive.")

    @classmethod
    def execute_custom_transactions(cls):
        """
        Execute custom buy/sell transactions if target price is reached.
        """
        crypto_data = CryptoDataModel()
        pending_transactions = cls.query.filter_by(active=True).filter(cls.target_price.isnot(None)).all()

        for transaction in pending_transactions:
            current_price = crypto_data.get_crypto_price(transaction.crypto_id)
            if not current_price:
                continue

            if transaction.transaction_type == "buy" and current_price <= transaction.target_price:
                transaction.active = False
                db.session.commit()

            elif transaction.transaction_type == "sell" and current_price >= transaction.target_price:
                transaction.active = False
                db.session.commit()

    @classmethod
    def execute_recurring_transactions(cls):
        """
        Execute recurring transactions (buy/sell at regular intervals).

        Args:
            None

        Returns:
            None
        """
        recurring_transactions = cls.query.filter_by(recurring=True, active=True).all()
        for transaction in recurring_transactions:
            transaction.timestamp = datetime.utcnow() + timedelta(days=1)
            db.session.add(transaction)  
        db.session.commit()  


    @classmethod
    def get_user_transactions(cls, user_id):
        """
        Retrieve all transactions for a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            List[TransactionModel]: A list of transactions for the user.
        """
        return cls.query.filter_by(user_id=user_id).all()