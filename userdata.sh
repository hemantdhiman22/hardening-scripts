#!/bin/bash

# Exit script on any command failure
set -e

# Install git if not already installed
if ! command -v git &> /dev/null; then
    echo "Installing Git..."
    sudo yum install git -y
fi

# Define script directory
SCRIPT_DIR="/home/scripts"

# Create directory if it doesn't exist
if [ ! -d "$SCRIPT_DIR" ]; then
    sudo mkdir -p "$SCRIPT_DIR"
fi

# Navigate to script directory
cd "$SCRIPT_DIR"

# Clone the repository (Skip if already cloned)
REPO_URL="https://github.com/hemantdhiman22/hardening-scripts.git"
REPO_NAME="hardening-scripts"

if [ ! -d "$REPO_NAME" ]; then
    sudo git clone "$REPO_URL"
else
    echo "Repository already exists. Pulling latest changes..."
    cd "$REPO_NAME"
    sudo git pull
fi

# Navigate to the repository directory
cd "$REPO_NAME"

# Ensure Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo yum install python3 -y
fi

# Run hardening scripts
for script in password_age_policy.py pwquality-harden.py sshd_hardening.py upgrade_sshd_version.py; do
    if [ -f "$script" ]; then
        echo "Executing $script..."
        sudo python3 "$script"
    else
        echo "Warning: $script not found!"
    fi
done

echo "Hardening scripts executed successfully."

