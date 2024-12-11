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


## 2. Get Crypto Price

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

### 3. Get Crypto Trends

**Route:** `/api/crypto-trends/<crypto_id>`  
**Request Type:** `GET`  
**Purpose:** Fetches price trends for a cryptocurrency.  
**Request Format:** None  
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
### 4. Get Top Cryptocurrencies

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
### 5. Compare Cryptocurrencies

**Route:** `/api/compare-cryptos/<crypto_id1>/<crypto_id2>`  
**Request Type:** `GET`  
**Purpose:** Compares two cryptocurrencies side by side based on their market data.  
**Request Format:** None  
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
  ### 6. Get Historical Data

- **Route:** `/api/historical-data/<crypto_id>/<days>`
- **Request Type:** `GET`
- **Purpose:** Fetches historical price data for a specific cryptocurrency over a given number of days.
- **Request Format:** None
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





