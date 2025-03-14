#!/bin/bash

echo "Installing dependencies..."
pkg update -y 2>/dev/null || sudo apt update -y
pkg install python -y 2>/dev/null || sudo apt install python3 -y

echo "Installing Python packages..."
pip install -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt

echo "Installation complete!"
