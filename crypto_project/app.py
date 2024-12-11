from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
from werkzeug.exceptions import BadRequest, Unauthorized

from config import ProductionConfig
from crypto_project.db import db
from crypto_project.models.transaction_model import TransactionModel
from crypto_project.models.portfolio_model import Portfolio
from crypto_project.models.user_model import Users
from crypto_project.models.cryptodata_model import CryptoDataModel

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

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

            if not username or not password:
                raise BadRequest("Both 'username' and 'password' are required.")

            Users.create_user(username, password)
            return jsonify({'status': 'account created', 'username': username}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/login', methods=['POST'])
    def login():
        """Log in a user."""
        try:
            data = request.json
            username = data.get('username')
            password = data.get('password')

            if not Users.check_password(username, password):
                raise Unauthorized("Invalid username or password.")

            return jsonify({'message': f"User {username} logged in successfully."}), 200
        except Unauthorized as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/update-password', methods=['PUT'])
    def update_password():
        """Update a user's password."""
        try:
            data = request.json
            username = data.get('username')
            old_password = data.get('old_password')
            new_password = data.get('new_password')

            if not Users.check_password(username, old_password):
                raise Unauthorized("Incorrect old password.")

            Users.update_password(username, new_password)
            return jsonify({'status': 'password updated'}), 200
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

    @app.route('/api/compare-cryptos', methods=['GET'])
    def compare_cryptos():
        """Compare two cryptocurrencies."""
        try:
            crypto1 = request.args.get('crypto1')
            crypto2 = request.args.get('crypto2')
            if not crypto1 or not crypto2:
                raise BadRequest("Both 'crypto1' and 'crypto2' parameters are required.")

            comparison = crypto_model.compare_cryptos(crypto1, crypto2)
            return jsonify({'comparison': comparison}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/set-price-alert', methods=['POST'])
    def set_price_alert():
        """Set a price alert for a cryptocurrency."""
        try:
            data = request.json
            crypto_id = data.get('crypto_id')
            target_price = data.get('target_price')

            if not crypto_id or target_price is None:
                raise BadRequest("'crypto_id' and 'target_price' are required.")

            alert_set = crypto_model.set_price_alert(crypto_id, target_price)
            if not alert_set:
                raise ValueError("Failed to set price alert.")

            return jsonify({'status': 'alert set', 'crypto_id': crypto_id, 'target_price': target_price}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
