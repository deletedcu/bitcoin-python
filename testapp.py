# import pytest
# import requests
from flask import url_for


class Tests:

    def test_app_running(self, client):

        res = client.get(url_for('ping'))
        assert res.status_code == 200
        assert res.json == {'ping': 'pong'}


