#!/bin/bash

python3 -m venv venv

source venv/bin/activate

cd src
pip install -e ".[dev]"

deactivate

echo "Setup completed successfully!" 