#!/bin/bash
# filepath: install.sh

set -e  # Exit immediately if a command exits with a non-zero status.

# --- Update Package Lists ---
echo "Updating package lists..."
apt-get update -y

# --- Install Dependencies ---
echo "Installing dependencies: python3, python3-venv, postgresql, nginx..."
apt-get install -y sudo python3 python3-venv postgresql nginx

# --- Project Directory ---
PROJECT_DIR="." # Replace with your actual project directory

# --- Application Directory ---
APP_DIR="$PROJECT_DIR/app"

# --- Create Project Directory (if it doesn't exist) ---
echo "Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"

# --- Create Application Directory (if it doesn't exist) ---
echo "Creating application directory: $APP_DIR"
mkdir -p "$APP_DIR"

# --- Create Virtual Environment ---
VENV_DIR="$APP_DIR/.venv"
echo "Creating virtual environment in: $VENV_DIR"
python3 -m venv "$VENV_DIR"

# --- Activate Virtual Environment ---
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# --- Install Python Requirements ---
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt" # Replace with your actual requirements file path

# Create a dummy requirements.txt if it doesn't exist
if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "No requirements.txt found. Creating a dummy one."
  touch "$REQUIREMENTS_FILE"
fi

cd app # Change to the app directory

echo "Installing Python requirements from: $REQUIREMENTS_FILE"
pip install --upgrade pip  # Upgrade pip
pip install -r "$REQUIREMENTS_FILE"

# --- Configure Nginx (Basic Example - Adapt to your needs) ---
echo "Configuring Nginx (basic example)..."
# Replace with your actual Nginx configuration file content
NGINX_CONFIG="/etc/nginx/sites-available/cn-manager"
echo "
server {
    listen 80;
    server_name your_domain.com; # Replace with your domain

    location / {
        proxy_pass http://127.0.0.1:5000; # Assuming your Flask app runs on port 5000
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
" > "$NGINX_CONFIG"

ln -s "$NGINX_CONFIG" /etc/nginx/sites-enabled/
rm -rf /etc/nginx/sites-enabled/default # Remove default config

nginx -t # Test nginx configuration
systemctl restart nginx

# --- Initialize PostgreSQL (Basic Example - Adapt to your needs) ---
echo "Initializing PostgreSQL (basic example)..."
# You might need to adjust these commands based on your PostgreSQL setup
sudo -u postgres psql -c "CREATE USER cn_manager WITH PASSWORD 'your_password';" # Replace with your password
sudo -u postgres psql -c "CREATE DATABASE cn_manager OWNER cn_manager;"

# --- Deactivate Virtual Environment ---
echo "Deactivating virtual environment..."
deactivate

echo "Setup complete!"