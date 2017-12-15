import pytest
# import requests
import getprice
from flask import Flask, url_for, request


class Tests:

    def test_requests(self):
        with getprice.app.test_request_context():
            assert getprice.requestingexchanges()


