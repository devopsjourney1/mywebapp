from flask import Flask, json
import socket
from prometheus_client import start_http_server


app = Flask(__name__)

start_http_server(8000)

REQUESTS = Counter('requests_total', 'Hello Worlds requested.', labelnames=['path'])
LATENCY = Histogram('latency_seconds', 'Time for a request', labelnames=['path'])

@LATENCY.time()
@app.route("/")
def hello_world():
    REQUESTS.labels("/").inc()
    return f"Hello, World! Served from {socket.gethostname()}"

@LATENCY.time()
@app.route("/bad")
def bad_page():
    REQUESTS.labels("/bad").inc()
    errorcode = 404
    data = {'error': errorcode}
    response = app.response_class(
        response=json.dumps(data),
        status=errorcode,
        mimetype='application/json'
    )
    return response