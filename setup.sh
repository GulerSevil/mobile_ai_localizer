#!/bin/bash

# Install Python 3.11 using Homebrew
brew install python@3.11

# Create a new virtual environment using Python 3.11
python3.11 -m venv venv_py311

# Activate the virtual environment
source venv_py311/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo "Setup completed successfully!" 