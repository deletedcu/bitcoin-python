import pytest

from getprice import app


@pytest.fixture
def app():
    app.debug = True
    return app
