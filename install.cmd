echo Installing now all required packages
pip install -r requirements.txt --user
pipenv --update
pip install -r requirements.txt --upgrade --user
echo Finished!