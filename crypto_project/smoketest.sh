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
###########################################l####

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

# Function to delete the existing user (if any)
delete_user_if_exists() {
  echo "Checking if user already exists..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')

  # If the user exists, delete them
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User 'testuser' exists, deleting user..."
    delete_response=$(curl -s -X DELETE "$BASE_URL/delete-user" -H "Content-Type: application/json" \
      -d '{"username":"testuser"}')
    if echo "$delete_response" | grep -q '"status": "user deleted"'; then
      echo "User 'testuser' deleted successfully."
    else
      echo "Failed to delete user."
      print_json "$delete_response"
      exit 1
    fi
  else
    echo "User 'testuser' does not exist, skipping deletion."
  fi
}


# Function to create a new user
create_user() {
  echo "Creating a new user..."
  response=$(curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"status": "account created"'; then
    echo "User created successfully."
    print_json "$response"
  else
    echo "Failed to create user."
    print_json "$response"
    exit 1
  fi
}

# Function to log in a user
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


###############################################
#
# CryptoData Model
#
###############################################

get_crypto_price() {
  echo "Fetching the price of Bitcoin..."
  response=$(curl -s -X GET "$BASE_URL/crypto-price/bitcoin")
  if echo "$response" | grep -q '"price_usd"'; then
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
  response=$(curl -s -X GET "$BASE_URL/crypto-trends/bitcoin")
  if echo "$response" | grep -q '"crypto_id": "bitcoin"'; then
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
  response=$(curl -s -X GET "$BASE_URL/top-cryptos")
  if echo "$response" | grep -q '"top_cryptos"'; then
    echo "Top-performing cryptocurrencies fetched successfully."
    print_json "$response"
  else
    echo "Failed to fetch top-performing cryptocurrencies."
    print_json "$response"
    exit 1
  fi
}

run_smoke_tests() {
  check_health
  delete_user_if_exists
  create_user
  login_user
  get_crypto_price
  get_price_trends
  get_top_performers
  echo "All tests passed successfully!"
}

# Run the smoke tests
run_smoke_tests
