#!/bin/sh
echo "Installing now all required packages:"
pip install -r requirements.txt
# Not needed but you don´t know if something could happen
pipenv install requests
