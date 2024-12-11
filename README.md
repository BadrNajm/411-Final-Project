# Crypto Trading Application
# Team Members: Wasay Rizwan, Badr Najm, Evren Yaman

Overview: The Crypto Trading Application is a simple tool designed for crypto traders/investors who want to manage their crypto portfolios, execute trades, and monitor market conditions. 

API: CoinGecko

Features:

- Get price trends for crypto  (1h,24h,1w,1m,1y)
- Look up a specific cryptocurrency and get its price
- Look up a specific cryptocurrency and get its trends
- Leaderboard for top-performing crypto 
- Track portfolio across multiple cryptocurrencies
- Price Alerts
- Display total portfolio in USD
- Buy at market price
- Sell at market price
- Create custom buy/sell transactions at target price
- Log to track transactions


## Environment Variables

The application relies on the following environment variables, which should be defined in a `.env` file:

- `DATABASE_URL`: Specifies the database connection URL. Example: `sqlite:///db/crypto_project.db`
- `SQL_CREATE_TRANSACTIONS_TABLE_PATH`: Path to the SQL script for creating the transactions table. Example: `/app/sql/create_transactions_table.sql`
- `SQL_CREATE_USERS_TABLE_PATH`: Path to the SQL script for creating the users table. Example: `/app/sql/create_user_table.sql`
- `CREATE_DB`: A flag to indicate whether the database should be created on startup. Example: `true`

### Example `.env` File (can be found in the repository)

```dotenv
DATABASE_URL=sqlite:///db/crypto_project.db
SQL_CREATE_TRANSACTIONS_TABLE_PATH=/app/sql/create_transactions_table.sql
SQL_CREATE_USERS_TABLE_PATH=/app/sql/create_user_table.sql
CREATE_DB=true
```
--- 
## **Setup and Run Using Docker**
1. **Build and Run the Docker Container**
   Use the provided `run_docker.sh` script to build and run the application in a container:
   ```bash
   bash run_docker.sh
   ```
   
2. **Run Smoke Tests**
   Use the `smoke_test.sh` script to validate routes:
   ```bash
   bash smoke_test.sh
   ```


# Routes Documentation

## 1. Health Check
- **Route:** `/api/health`
- **Request Type:** `GET`
- **Purpose:** Verifies if the application is running.
- **Request Format:** None
- **Response Format:** JSON
  - `status` (String): Health status of the application.
- **Example Request:**
  ```bash
  curl -X GET http://127.0.0.1:5000/api/health
  ```
- **Example Response:**
  ```json
  {
    "status": "healthy"
  }
  ```

---
## 2. Create User

- **Route:** `/api/create-user`
- **Request Type:** `POST`
- **Purpose:** Creates a new user account with a username and password.

**Request Format:** JSON  
- `username` (String): The user's chosen username.  
- `password` (String): The user's chosen password.

**Response Format:** JSON  
- `status` (String): Status of the operation (e.g., "success" or "error").  
- `message` (String): Description of the result (e.g., "Account created successfully" or error details).

**Example Request:**  
```bash
curl -X POST http://127.0.0.1:5000/api/create-user \
-H "Content-Type: application/json" \
-d '{
  "username": "newuser123",
  "password": "securepassword"
}'
```
  

**Example Response:**
  ```json
    {
      "status": "user added",
      "message": "Account created successfully"
    }
  ```

--- 

## 3. Login User

**Route:** `/api/login-user`  
**Request Type:** `POST`  
**Purpose:** Authenticates a user with a username and password.  

**Request Format:** JSON  
- `username` (String): The user's username.  
- `password` (String): The user's password.  

**Response Format:** JSON  
- `status` (String): Status of the operation.  
- `message` (String): Description of the result.  

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/login-user \
-H "Content-Type: application/json" \
-d '{
  "username": "existinguser123",
  "password": "securepassword"
}'
```
**Example Response:**
```json
{
    "status": "success",
    "message": "Login successful"
}

```

--- 

## 4. Get Crypto Price

**Route:** `/api/crypto-price/<crypto_id>`  
**Request Type:** `GET`  
**Purpose:** Fetches the current price of a cryptocurrency.  
**Request Format:** None  
**Response Format:** JSON  
- `crypto_id` (String): ID of the cryptocurrency.  
- `price_usd` (Float): Current price in USD.

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/crypto-price/bitcoin
```

- **Example Response:**
  ```json
   {
      "crypto_id": "bitcoin",
      "price_usd": 50234.12
  }

  ```

---

## 5. Get Crypto Trends

**Route:** `/api/crypto-trends/<crypto_id>`  
**Request Type:** `GET`  
**Purpose:** Fetches price trends for a cryptocurrency.  
**Request Format:** None  
**Required Parameters:**  
- `crypto_id` (String): The ID of the cryptocurrency to fetch trends for.

**Response Format:** JSON  
- `crypto_id` (String): ID of the cryptocurrency.  
- `trends` (List): Historical price trends for the cryptocurrency.

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/crypto-trends/bitcoin
```

- **Example Response:**
  ```json
   {
    "crypto_id": "bitcoin",
    "trends": [
        [1634083200000, 60000.23],
        [1634169600000, 60500.12],
        [1634256000000, 61000.34]
    ]





---
## 6. Get Top Cryptocurrencies

**Route:** `/api/top-cryptos`  
**Request Type:** `GET`  
**Purpose:** Fetches a list of top-performing cryptocurrencies based on their 24-hour price change.  
**Request Format:** None  
**Response Format:** JSON  
- `top_cryptos` (List): A list of top-performing cryptocurrencies, including their details such as name, symbol, and price.

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/top-cryptos
```
- **Example Response:**
  ```json
  {
    "top_cryptos": [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 61000,
            "price_change_percentage_24h": 5.23
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "current_price": 4000,
            "price_change_percentage_24h": 3.89
        }
    ]
---
## 7. Compare Cryptocurrencies

**Route:** `/api/compare-cryptos/<crypto_id1>/<crypto_id2>`  
**Request Type:** `GET`  
**Purpose:** Compares two cryptocurrencies side by side based on their market data.  
**Request Format:** None  
**Required Parameters:**  
- `crypto_id1` (String): ID of the first cryptocurrency.  
- `crypto_id2` (String): ID of the second cryptocurrency.

**Response Format:** JSON  
- `comparison` (Object): Contains the details of both cryptocurrencies, including their names, symbols, current prices, and market caps.

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/compare-cryptos/bitcoin/ethereum
```
- **Example Response:**
  ```json
  {
      "comparison": {
          "bitcoin": {
              "id": "bitcoin",
              "symbol": "btc",
              "name": "Bitcoin",
              "current_price": 61000,
              "market_cap": 1140000000000
          },
          "ethereum": {
              "id": "ethereum",
              "symbol": "eth",
              "name": "Ethereum",
              "current_price": 4000,
              "market_cap": 450000000000
          }
      }
  }

  ```

  ---
  ## 8. Get Historical Data

- **Route:** `/api/historical-data/<crypto_id>/<days>`
- **Request Type:** `GET`
- **Purpose:** Fetches historical price data for a specific cryptocurrency over a given number of days.
- **Request Format:** None
- **Required Parameters:**  
- `crypto_id` (String): ID of the cryptocurrency.  
- `days` (Integer): Number of days for which historical data is requested.


- **Response Format:** JSON  
  - `crypto_id` (String): ID of the cryptocurrency.  
  - `historical_data` (Object): Contains historical price data, including timestamps and prices.

**Example Request:**
```bash
curl -X GET http://127.0.0.1:5000/api/historical-data/bitcoin/7
```  
- **Example Response:**
  ```json
  {
  "crypto_id": "bitcoin",
  "historical_data": {
    "prices": [
      [1634083200000, 60000.23],
      [1634169600000, 60500.12],
      [1634256000000, 61000.34]
    ]
  }





