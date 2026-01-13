import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
import logging

from app.database import get_shipment_counts

app = Flask(__name__)

# logging configuration
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s"
)

try:
    file_handler = logging.FileHandler("logs/service.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
except PermissionError:
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.error("File logging unavailable, falling back to stdout")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok"}), 200

@app.route("/metrics", methods=["GET"])
def metrics():
    logging.info("Received request for /metrics")
    try:
        counts = get_shipment_counts()
        logging.info("Successfully retrieved shipment metrics")
        return jsonify(counts), 200
    except Exception:
        logging.exception("Error while processing /metrics request")
        return jsonify({"error": "internal service error"}), 500

if __name__ == "__main__":
    logging.info("Starting internal metrics service")
    app.run(host="0.0.0.0", port=5000)
