#!/bin/bash
brew install python@3.11

python3.11 -m venv venv_py31

source venv_py31/bin/activate

# Upgrade pip
pip install --upgrade pip

cd src
pip install -e ".[dev]"

deactivate

echo "Setup completed successfully!" 