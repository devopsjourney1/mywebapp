from flask import Flask, json
import socket
from prometheus_client import Histogram, Counter, Gauge
import prometheus_client


app = Flask(__name__)

REQUESTS = Counter('requests_total', 'Hello Worlds requested.', labelnames=['path'])
#LATENCY = Histogram('latency_seconds', 'Time for a request', labelnames=['path'])

@app.route("/")
def hello_world():
    REQUESTS.labels("/").inc()
    return f"Hello, World! Served from {socket.gethostname()}"

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

@app.route("/metrics")
def metrics():
    REQUESTS.labels("/metrics").inc()
    return prometheus_client.generate_latest()