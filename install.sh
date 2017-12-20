#!/bin/sh
echo "Installing now all required packages:"
pip install -r requirements.txt
# Updating pipenv & pip
pipenv --update
# Needed if you already installed the packages and to upgrade them
pip install -r requirements.txt --upgrade
echo "Finished!"
