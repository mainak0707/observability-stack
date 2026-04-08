import time
from flask import Flask, request
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry

app = Flask(__name__)

# Use default registry (important for gunicorn compatibility)
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests'
)

ACTIVE_REQUESTS = Gauge(
    'active_requests',
    'Active Requests'
)

@app.before_request
def before_request():
    ACTIVE_REQUESTS.inc()

@app.after_request
def after_request(response):
    ACTIVE_REQUESTS.dec()
    REQUEST_COUNT.inc()
    return response

@app.route("/")
def home():
    time.sleep(2)
    return "Hello, Prometheus!"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)