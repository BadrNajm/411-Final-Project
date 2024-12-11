# Crypto Trading Application
# Team Members: Wasay Rizwan, Badr Najm, Evren Yaman

Overview: The Crypto Trading Application is a simple tool designed for crypto traders/investors who want to manage their crypto portfolios, execute trades, and monitor market conditions. 

API: CoinGecko

Features:

- Login Page with Security 2FA
- Price Alerts
- Get price trends for crypto  (1h,24h,1w,1m,1y)
- Track portfolio across multiple cryptocurrencies 
- Display total portfolio valueUSD  (possibly api for currency conversion)
- Look up a specific cryptocurrency and get its price
- Look up a specific cryptocurrency and get its trends
- Buy at market price
- Sell at market price
- Log to track transactions
- Leaderboard for top-performing crypto (from battle model)

Route: /create-user
Request Type: POST  
Purpose: Creates a new user account with a username and password.
Request Body:
    username(String): The user's chosen username.
    password(String): The user's chosen password.
Example Request:
- json
  {
    "username": "newuser123",
    "password": "securepassword"
  }
Response Format:
- Success Response:  
    - json
  {
    "status": "user added",
    "message": "Account created successfully"
  }

Route: /login
Request Type: POST  
Purpose: Logs in a user with a username, password, and 2FA token.
Request Body:
    username(String): The user's username.
    password(String): The user's password.
    token(String): The 2FA token (TOTP).
Example Request:
- json
  {
    "username": "testuser",
    "password": "password123",
    "token": "123456"
  }
Response Format:
- Success Response:  
    - json
  {
    "status": "success",
    "message": "User testuser logged in successfully."
  }

Route: /logout
Request Type: POST  
Purpose: Logs out a user.
Request Body:
    username(String): The user's username.
Example Request:
- json
  {
    "username": "testuser"
  }
Response Format:
- Success Response:  
    - json
  {
    "status": "success",
    "message": "User testuser logged out successfully."
  }

Route: /health
Request Type: GET 
Purpose: Checks if the service is up and running.
Response Format:
- Success Response:  
    - json
  {
    "status": "healthy"
  }

Route: /crypto-price/<crypto_id>
Request Type: GET 
Purpose: Fetches the current price of a specific cryptocurrency in USD.
Request Body:
    crypto_id(String): The cryptocurrency ID (e.g., `bitcoin`).
Response Format:
- Success Response:  
    - json
  {
    "status": "success",
    "crypto_id": "bitcoin",
    "price": 45000.25
  }

Route: /crypto-trends/<crypto_id>
Request Type: GET
Purpose: Fetches price trends for a specific cryptocurrency.
Request Body:
    crypto_id(String): The cryptocurrency ID (e.g., `bitcoin`).
    days(String): Time range (e.g., `1`, `7`, `30`, `365`).
Response Format:
- Success Response:  
    - json
  {
    "status": "success",
    "crypto_id": "bitcoin",
    "trends": [
      {"timestamp": 1625097600, "price": 35000.5},
      {"timestamp": 1625184000, "price": 36000.0}
    ]
  }

Route: /portfolio-value/<user_id>
Request Type: GET
Purpose: Fetches the total value of a user's portfolio in USD.
Request Body:
    user_id(Int): The ID of the user.
Response Format:
- Success Response:
    - json
  {
    "status": "success",
    "total_value": 12500.75
  }

Route: /create-transaction
Request Type: POST
Purpose: Creates a new transaction (buy/sell)
Request Body:
    user_id(Int): The user's ID.
    crypto_id(String): The crytocurrency ID.
    action(String): buy or sell.
    amount(Float): The amount of crypto to trade.
    price(Float): The price per unit.
Example Request
- json
{
    "user_id": 1,
    "crypto_id": "bitcoin",
    "action": "buy",
    "amount": 0.5,
    "price": 45000
}
Response Format:
- Success Response:
    - json
  {
    "status": "transaction added",
    "transaction_id": 123
  }