import json
import sys
import unittest
import coverage
import getprice
import requests

cov = coverage.coverage(branch=True)
cov.start()

from flask import Flask, session, request, json as flask_json
from flask_socketio import SocketIO, send, emit, Namespace
from time import sleep
from threading import Thread, Event, Lock

app = getprice.app
app.config['SECRET_KEY'] = getprice.app.config['SECRET_KEY']
socketio = SocketIO(app)
disconnected = None

appstarted_bitpay_request = requests.get(getprice.bitpay_url)
appstarted_bitpay_data = appstarted_bitpay_request.json()

bitpay_EUR = appstarted_bitpay_data[2]
bitpay_USD = appstarted_bitpay_data[1]

appstarted_bitpay_price = "{0:.2f} {1}".format(bitpay_EUR["rate"], bitpay_EUR["code"])

# Price thread
thread = None
thread_lock = Lock()


def background_thread():
    print("\nBackground Thread started..!")
    print("background_thread -> Requesting price from BitPay")
    while True:
        bitpaydata = requests.get(getprice.bitpay_url)
        bitpaydata = bitpaydata.json()

        bitpay_EUR = bitpaydata[2]
        bitpay_USD = bitpaydata[1]

        global bitpayprice
        bitpayprice = "{0:.2f} {1}".format(bitpay_EUR["rate"], bitpay_EUR["code"])

        print("background_thread -> Got successfully a response to the request!")
        print("background_thread -> Bitpay request -> BitPay price: " + bitpayprice + "\n")
        socketio.send({'price': bitpayprice}, namespace='/price')
        exit(0)


@socketio.on('connect')
def on_connect():
    send('connected')
    send(json.dumps(dict(request.args)))
    send(json.dumps({h: request.headers[h] for h in request.headers.keys()
                     if h not in ['Host', 'Content-Type', 'Content-Length']}))
    print('connect -> Client connected', request.sid)


@socketio.on('disconnect')
def on_disconnect():
    global disconnected
    print('disconnect -> Client disconnected', request.sid)
    disconnected = '/'


@socketio.on('connect', namespace='/price')
def on_connect_test():
    global thread
    print('connect (/price) -> Client connected', request.sid)
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    # Added sleep function so the background function can doing its things right and successful
    # Sleeping for 5 seconds, this should be enough for the background function
    socketio.sleep(5)
    send('connected-test')
    send(json.dumps(dict(request.args)))
    send(json.dumps({h: request.headers[h] for h in request.headers.keys()
                     if h not in ['Host', 'Content-Type', 'Content-Length']}))


@socketio.on('disconnect', namespace='/price')
def on_disconnect_test():
    global disconnected
    print('disconnect (/price) -> Client disconnected', request.sid)
    disconnected = '/test'


@socketio.on('message')
def on_message(message):
    send(message)
    print('def on_message(message) -> Message received -> ' + message)
    return message


@socketio.on('error testing')
def raise_error(data):
    raise AssertionError()


@socketio.on('error testing')
def raise_error(data):
    raise AssertionError()


@socketio.on_error('/test')
def error_handler_namespace(value):
    if isinstance(value, AssertionError):
        global error_testing_namespace
        error_testing_namespace = True
    else:
        raise value
    return value


@socketio.on("error testing", namespace='/price')
def raise_error_namespace(data):
    raise AssertionError()


@socketio.on_error_default
def error_handler_default(value):
    if isinstance(value, AssertionError):
        global error_testing_default
        error_testing_default = True
    else:
        raise value
    print('def error_handler_default -> error_testing_default -> ' + str(error_testing_default))
    print('def error_handler_default -> value -> ' + str(value))
    return value


@socketio.on("error testing", namespace='/unused_namespace')
def raise_error_default(data):
    raise AssertionError()


class TestSocketIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # Connect to price namespace
    def test_connect_namespace(self):
        print("#####################")
        print("\nTest -> test_connect_namespace -> Test started")
        client = socketio.test_client(app, namespace='/price')
        received = client.get_received('/price')
        print("test_connect_namespace (price) -> \n" + str(received))
        self.assertEqual(len(received), 4)
        self.assertEqual(received[0]['args'], {'price': bitpayprice})
        self.assertEqual(received[1]['args'], 'connected-test')
        self.assertEqual(received[2]['args'], '{}')
        self.assertEqual(received[3]['args'], '{}')
        client.disconnect(namespace='/price')
        print("Test -> test_connect_namespace -> Successful\n")

    # Disconnect from price namespace
    def test_disconnect_namespace(self):
        print("Test -> test_disconnect_namespace -> Test started")
        global disconnected
        disconnected = None
        client = socketio.test_client(app, namespace='/price')
        client.disconnect('/price')
        self.assertEqual(disconnected, '/test')
        print("Test -> test_disconnect_namespace -> Successful\n")

    # Random message test
    def test_send(self):
        print("Test -> test_send -> Test started")
        client = socketio.test_client(app)
        client.get_received()
        client.send('echo this message back')
        received = client.get_received()
        print("test_send -> " + str(received))
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], 'echo this message back')
        print("Test -> test_send -> Successful\n")

    # Random Error handling test
    def test_error_handling_default(self):
        print("Test -> test_error_handling_default -> Test started")
        client = socketio.test_client(app, namespace='/unused_namespace')
        client.get_received('/unused_namespace')
        print('test_error_handling_default -> client.get_received(/unused_namespace) -> ' + str(client.get_received('/unused_namespace')))

        global error_testing_default
        error_testing_default = False
        client.emit("error testing", "", namespace='/unused_namespace')

        print('test_error_handling_default (unused_namespace) -> error_testing_default -> ' + str(error_testing_default))
        self.assertTrue(error_testing_default)
        print("Test -> test_error_handling_default -> Successful\n")

    # Basic Flask unit test
    def test_delayed_init(self):
        print("Test -> test_delayed_init -> Test started")
        app = Flask(__name__)
        socketio = SocketIO(allow_upgrades=False, json=flask_json)

        @socketio.on('connect')
        def on_connect():
            send({'connected': 'foo'}, json=True)

        socketio.init_app(app, cookie='foo')
        self.assertFalse(socketio.server.eio.allow_upgrades)
        self.assertEqual(socketio.server.eio.cookie, 'foo')

        client = socketio.test_client(app)
        received = client.get_received()
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['args'], {'connected': 'foo'})
        print("test_delayed_init -> " + str(received))
        print("Test -> test_delayed_init -> Successful\n")

    # Price request
    def test_requests(self):
        print("Test -> test_requests -> Test started")
        with getprice.app.test_request_context():
            assert getprice.requestingexchanges()
        print("Test -> test_requests -> Successful\n")


print("\n##########\nVersion of application: " + getprice.VERSION)
print("Changelog:\n" + getprice.CHANGELOG + "\n##########")

if __name__ == '__main__':
    unittest.main()
