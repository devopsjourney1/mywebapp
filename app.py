from flask import Flask, json
import socket
from prometheus_client import Histogram, Counter, Gauge, start_http_server
import prometheus_client


app = Flask(__name__)

REQUESTS = Counter('mywebapp_requests_total', 'Hello Worlds requested.', labelnames=['path'])
LATENCY = Histogram('mywebapp_latency_seconds', 'Time for a request', labelnames=['path'])
start_http_server(8001)

@LATENCY.time()
@app.route("/")
def hello_world():
    REQUESTS.labels("/").inc()
    html = f"<h1>My WebApp!</h1> Hello World! Served from <b>{socket.gethostname()}</b><br>"
    return html

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
