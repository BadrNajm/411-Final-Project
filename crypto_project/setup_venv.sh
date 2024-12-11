#!/bin/bash
# Set the name of the virtual environment directory
VENV_DIR="crypto_project_venv"
REQUIREMENTS_FILE="requirements.lock"

# Function to activate the virtual environment
activate_venv() {
  source "$VENV_DIR/bin/activate"
}

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"

  activate_venv

  # Install dependencies from requirements.lock if it exists
  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install --no-cache-dir -r "$REQUIREMENTS_FILE"
  else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
  fi
else
  activate_venv
  echo "Virtual environment already exists. Activated."
fi
