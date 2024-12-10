from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized

from config import ProductionConfig
from crypto_project.db import db
from crypto_project.models.transaction_model import TransactionModel
from crypto_project.models.user_model import Users

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    ####################################################
    #
    # Healthchecks
    #
    ####################################################

    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """Health check route to verify the service is running."""
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

    ##########################################################
    #
    # User management
    #
    ##########################################################

    @app.route('/api/create-user', methods=['POST'])
    def create_user() -> Response:
        """Route to create a new user."""
        app.logger.info('Creating new user')
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

            Users.create_user(username, password)
            app.logger.info("User added: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user() -> Response:
        """Route to delete a user."""
        app.logger.info('Deleting user')
        try:
            data = request.get_json()
            username = data.get('username')

            if not username:
                return make_response(jsonify({'error': 'Invalid input, username is required'}), 400)

            Users.delete_user(username)
            app.logger.info("User deleted: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    ##########################################################
    #
    # Transactions
    #
    ##########################################################

    @app.route('/api/create-transaction', methods=['POST'])
    def create_transaction() -> Response:
        """Route to create a new transaction."""
        app.logger.info('Creating new transaction')
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            crypto_id = data.get('crypto_id')
            transaction_type = data.get('transaction_type')
            quantity = data.get('quantity')
            price = data.get('price')

            if not user_id or not crypto_id or not transaction_type or not quantity or not price:
                return make_response(jsonify({'error': 'All fields are required'}), 400)

            TransactionModel.create_transaction(user_id, crypto_id, transaction_type, quantity, price)
            app.logger.info("Transaction created: %s", data)
            return make_response(jsonify({'status': 'transaction created'}), 201)
        except Exception as e:
            app.logger.error("Failed to create transaction: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/get-user-transactions/<int:user_id>', methods=['GET'])
    def get_user_transactions(user_id: int) -> Response:
        """Route to get all transactions for a user."""
        try:
            app.logger.info(f"Getting transactions for user ID: {user_id}")
            transactions = TransactionModel.get_user_transactions(user_id)
            return make_response(jsonify({'status': 'success', 'transactions': [tx.serialize() for tx in transactions]}), 200)
        except Exception as e:
            app.logger.error("Failed to retrieve transactions: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    ##########################################################
    #
    # Initialize Database
    #
    ##########################################################

    @app.route('/api/init-db', methods=['POST'])
    def init_db():
        """Route to initialize or recreate database tables."""
        try:
            with app.app_context():
                app.logger.info("Dropping all existing tables.")
                db.drop_all()
                app.logger.info("Creating all tables from models.")
                db.create_all()
            app.logger.info("Database initialized successfully.")
            return jsonify({"status": "success", "message": "Database initialized successfully."}), 200
        except Exception as e:
            app.logger.error("Failed to initialize database: %s", str(e))
            return jsonify({"status": "error", "message": "Failed to initialize database."}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
