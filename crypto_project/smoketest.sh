#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Utility Functions
#
###############################################

print_json() {
  if [ "$ECHO_JSON" = true ]; then
    echo "$1" | jq .
  fi
}

###############################################
#
# Health Checks
#
###############################################

check_health() {
  echo "Checking health status..."
  response=$(curl -s -X GET "$BASE_URL/health")
  if echo "$response" | grep -q '"status": "healthy"'; then
    echo "Service is healthy."
    print_json "$response"
  else
    echo "Health check failed."
    print_json "$response"
    exit 1
  fi
}

###############################################
#
# User Management
#
###############################################

create_user() {
  echo "Creating a new user..."
  response=$(curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"status": "user added"'; then
    echo "User created successfully."
    print_json "$response"
  else
    echo "Failed to create user."
    print_json "$response"
    exit 1
  fi
}

login_user() {
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
    print_json "$response"
  else
    echo "Failed to log in user."
    print_json "$response"
    exit 1
  fi
}

logout_user() {
  echo "Logging out user..."
  response=$(curl -s -X POST "$BASE_URL/logout" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}')
  if echo "$response" | grep -q '"message": "User testuser logged out successfully."'; then
    echo "User logged out successfully."
    print_json "$response"
  else
    echo "Failed to log out user."
    print_json "$response"
    exit 1
  fi
}

###############################################
#
# CryptoData Model
#
###############################################

get_crypto_price() {
  echo "Fetching the price of Bitcoin..."
  response=$(curl -s -X GET "$BASE_URL/crypto-price/bitcoin")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Crypto price fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch crypto price."
    print_json "$response"
    exit 1
  fi
}

get_price_trends() {
  echo "Fetching price trends for Bitcoin..."
  response=$(curl -s -X GET "$BASE_URL/crypto-trends/bitcoin?days=7")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Crypto price trends fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch crypto price trends."
    print_json "$response"
    exit 1
  fi
}

get_top_performers() {
  echo "Fetching top-performing cryptocurrencies..."
  response=$(curl -s -X GET "$BASE_URL/top-performers")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Top-performing cryptocurrencies fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch top-performing cryptocurrencies."
    print_json "$response"
    exit 1
  fi
}

set_price_alert() {
  echo "Setting a price alert for Bitcoin at $45,000..."
  response=$(curl -s -X POST "$BASE_URL/set-price-alert" -H "Content-Type: application/json" \
    -d '{"crypto_id":"bitcoin", "target_price":45000}')
  if echo "$response" | grep -q '"status": "alert set"'; then
    echo "Price alert set successfully."
    print_json "$response"
  else
    echo "Failed to set price alert."
    print_json "$response"
    exit 1
  fi
}

compare_cryptos() {
  echo "Comparing Bitcoin and Ethereum..."
  response=$(curl -s -X GET "$BASE_URL/compare-cryptos?crypto1=bitcoin&crypto2=ethereum")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Cryptos compared successfully."
    print_json "$response"
  else
    echo "Failed to compare cryptos."
    print_json "$response"
    exit 1
  fi
}

###############################################
#
# Portfolio Management
#
###############################################

get_portfolio_value() {
  echo "Fetching total portfolio value..."
  response=$(curl -s -X GET "$BASE_URL/portfolio-value/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Portfolio value fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch portfolio value."
    print_json "$response"
    exit 1
  fi
}

get_portfolio_percentage() {
  echo "Fetching portfolio percentage distribution..."
  response=$(curl -s -X GET "$BASE_URL/portfolio-percentage/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Portfolio percentage distribution fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch portfolio percentage distribution."
    print_json "$response"
    exit 1
  fi
}

track_profit_loss() {
  echo "Tracking profit/loss for portfolio..."
  response=$(curl -s -X GET "$BASE_URL/portfolio-profit-loss/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Profit/loss tracked successfully."
    print_json "$response"
  else
    echo "Failed to track profit/loss."
    print_json "$response"
    exit 1
  fi
}

get_crypto_count() {
  echo "Fetching crypto count for Bitcoin..."
  response=$(curl -s -X GET "$BASE_URL/crypto-count/1/bitcoin")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Crypto count fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch crypto count."
    print_json "$response"
    exit 1
  fi
}

###############################################
#
# Transaction Management
#
###############################################

create_transaction() {
  echo "Creating a new transaction (buy Bitcoin)..."
  response=$(curl -s -X POST "$BASE_URL/create-transaction" -H "Content-Type: application/json" \
    -d '{"user_id": 1, "crypto_id": "bitcoin", "action": "buy", "amount": 0.5, "price": 40000}')
  if echo "$response" | grep -q '"status": "transaction added"'; then
    echo "Transaction created successfully."
    print_json "$response"
  else
    echo "Failed to create transaction."
    print_json "$response"
    exit 1
  fi
}

get_all_transactions() {
  echo "Fetching all transactions for user 1..."
  response=$(curl -s -X GET "$BASE_URL/get-transactions/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Transactions fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch transactions."
    print_json "$response"
    exit 1
  fi
}

get_transaction_by_id() {
  echo "Fetching transaction with ID 1..."
  response=$(curl -s -X GET "$BASE_URL/get-transaction/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Transaction fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch transaction by ID."
    print_json "$response"
    exit 1
  fi
}

delete_transaction() {
  echo "Deleting transaction with ID 1..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-transaction/1")
  if echo "$response" | grep -q '"status": "transaction deleted"'; then
    echo "Transaction deleted successfully."
    print_json "$response"
  else
    echo "Failed to delete transaction."
    print_json "$response"
    exit 1
  fi
}

validate_balance_for_transaction() {
  echo "Validating sufficient balance for a $20000 transaction..."
  response=$(curl -s -X GET "$BASE_URL/validate-transaction/1/20000")
  if echo "$response" | grep -q '"status": "sufficient funds"'; then
    echo "Sufficient balance for transaction."
    print_json "$response"
  else
    echo "Insufficient balance for transaction."
    print_json "$response"
    exit 1
  fi
}

###############################################
#
# Run All Smoke Tests
#
###############################################

run_smoke_tests() {
  print_json
  check_health
  create_user
  login_user
  get_crypto_price
  get_price_trends
  get_top_performers
  set_price_alert
  compare_cryptos
  get_portfolio_value
  get_portfolio_percentage
  track_profit_loss
  get_crypto_count
  create_transaction
  get_all_transactions
  get_transaction_by_id
  delete_transaction
  validate_balance_for_transaction
  logout_user
  echo "All smoke tests passed successfully!"
}

# Execute the smoke tests
run_smoke_tests
