from dotenv import load_dotenv
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest, Unauthorized
import os

from config import ProductionConfig, TestConfig
from crypto_project.db import db
from crypto_project.models.transaction_model import TransactionModel
from crypto_project.models.user_model import Users
from crypto_project.models.cryptodata_model import CryptoDataModel
import logging

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # Database Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')  # Use DATABASE_URL from .env
    

    

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

    crypto_model = CryptoDataModel()

    ####################################################
    #
    # Healthchecks
    #
    ####################################################

    @app.route('/api/health', methods=['GET'])
    def healthcheck():
        """Health check route to verify the service is running."""
        return jsonify({'status': 'healthy'}), 200

    ##########################################################
    #
    # User Management
    #
    ##########################################################

    @app.route('/api/create-account', methods=['POST'])
    def create_account():
        """Create a new user account."""
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            # Validate inputs
            if not username or not password:
                raise BadRequest("'username' and 'password' are required.")

            # Check if username already exists
            if Users.query.filter_by(username=username).first():
                raise ValueError(f"User with username '{username}' already exists.")

            # Create new user
            Users.create_user(username, password)
            return jsonify({'status': 'account created', 'username': username}), 201

        except ValueError as e:
            # Handle duplicate username error
            logging.error(f"Error creating user: {str(e)}")
            return jsonify({'error': str(e)}), 400  # 400 for bad request (duplicate username)
        except BadRequest as e:
            # Handle missing input error
            logging.error(f"Bad request error: {str(e)}")
            return jsonify({'error': str(e)}), 400  # 400 for missing input
        except Exception as e:
            # Handle unexpected errors
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500  # 500 for internal server error

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user():
        """Delete a user by username."""
        try:
            data = request.json
            username = data.get('username')

            if not username:
                raise BadRequest("'username' is required.")

            # Delete the user
            Users.delete_user(username)
            return jsonify({'status': 'user deleted', 'username': username}), 200
        except ValueError as e:
            # Handle user not found error
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            # Handle unexpected errors
            return jsonify({'error': str(e)}), 500


    @app.route('/api/login', methods=['POST'])
    def login():
        """Log in a user."""
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            # Validate login credentials
            if not Users.check_password(username, password):
                raise Unauthorized("Invalid username or password.")

            return jsonify({'message': f"User {username} logged in successfully."}), 200
        except Unauthorized as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    ##########################################################
    #
    # CoinGecko API Interaction
    #
    ##########################################################

    @app.route('/api/crypto-price/<string:crypto_id>', methods=['GET'])
    def get_crypto_price(crypto_id):
        """Fetch the current price of a cryptocurrency."""
        try:
            price = crypto_model.get_crypto_price(crypto_id)
            if price is None:
                raise ValueError(f"Failed to fetch price for {crypto_id}.")
            return jsonify({'crypto_id': crypto_id, 'price_usd': price}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/crypto-trends/<string:crypto_id>', methods=['GET'])
    def get_crypto_trends(crypto_id):
        """Fetch price trends for a cryptocurrency."""
        try:
            trends = crypto_model.get_price_trends(crypto_id)
            if not trends:
                raise ValueError(f"Failed to fetch trends for {crypto_id}.")
            return jsonify({'crypto_id': crypto_id, 'trends': trends}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/top-cryptos', methods=['GET'])
    def get_top_cryptos():
        """Fetch top-performing cryptocurrencies."""
        try:
            top_cryptos = crypto_model.get_top_performing_cryptos()
            return jsonify({'top_cryptos': top_cryptos}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/compare-cryptos/<string:crypto_id1>/<string:crypto_id2>', methods=['GET'])
    def compare_cryptos(crypto_id1, crypto_id2):
        """Compare two cryptocurrencies."""
        try:
            comparison = crypto_model.compare_cryptos(crypto_id1, crypto_id2)
            if not comparison:
                raise ValueError(f"Failed to compare {crypto_id1} and {crypto_id2}.")
            return jsonify({'comparison': comparison}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
        
    @app.route('/api/historical-data/<string:crypto_id>/<int:days>', methods=['GET'])
    def get_historical_data(crypto_id, days):
        """Fetch historical data for a cryptocurrency."""
        try:
            trends = crypto_model.get_price_trends(crypto_id, days=str(days))
            if not trends:
                raise ValueError(f"Failed to fetch historical data for {crypto_id} over {days} days.")
            return jsonify({'crypto_id': crypto_id, 'historical_data': trends}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    ##########################################################
    #
    # Transaction Management
    #
    ##########################################################

    @app.route('/api/create-transaction', methods=['POST'])
    def create_transaction():
        """Create a new transaction."""
        try:
            data = request.json
            user_id = data.get('user_id')
            crypto_id = data.get('crypto_id')
            transaction_type = data.get('transaction_type')
            quantity = data.get('quantity')
            price = data.get('price')

            if not all([user_id, crypto_id, transaction_type, quantity, price]):
                raise BadRequest("All fields ('user_id', 'crypto_id', 'transaction_type', 'quantity', 'price') are required.")

            transaction = TransactionModel.create_transaction(
                user_id=user_id,
                crypto_id=crypto_id,
                transaction_type=transaction_type,
                quantity=quantity,
                price=price
            )
            return jsonify({'status': 'transaction created', 'transaction_id': transaction.id}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    ##########################################################
    #
    # Alerts and Monitoring
    #
    ##########################################################

    @app.route('/api/set-price-alert', methods=['POST'])
    def set_price_alert():
        """Set a price alert for a cryptocurrency."""
        try:
            data = request.json
            crypto_id = data.get('crypto_id')
            target_price = data.get('target_price')

            # Validate inputs
            if not crypto_id or target_price is None:
                raise BadRequest("'crypto_id' and 'target_price' are required.")

            logging.info(f"Setting price alert for {crypto_id} at {target_price}.")

            # Attempt to set the price alert
            alert_set = crypto_model.set_price_alert(crypto_id, target_price)
            if not alert_set:
                raise ValueError(f"Failed to set price alert for {crypto_id}.")

            return jsonify({'status': 'alert set', 'crypto_id': crypto_id, 'target_price': target_price}), 201
        except BadRequest as e:
            logging.error(f"Bad request error: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except ValueError as e:
            logging.error(f"Value error: {str(e)}")
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': str(e)}), 500


    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
