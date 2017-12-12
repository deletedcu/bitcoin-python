import pytest
# import requests
from getprice import create_app, requestingexchanges
from flask import Flask, url_for

@pytest.mark.usefixtures('client_class')
class Tests:

    def test_app_running(self, client):

        res = client.get(url_for('ping'))
        print("\nTesting ping test")
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}
        print("Finished testing ping test successfully\n")

    def test_requestexchanges(self):
        app = create_app()
        with app.app_context():
            print("Testing requestingexchanges()\n")
            assert requestingexchanges()
            print("Finished testing requestingexchanges() successfully")

