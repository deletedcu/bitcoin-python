echo Installing now all required packages
pip install -r requirements.txt
pipenv --update
pip install -r requirements.txt --upgrade
echo Finished!