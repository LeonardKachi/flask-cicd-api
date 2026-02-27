from flask import Flask, jsonify, request
from datetime import datetime, timezone
import logging
import sys

# Configure structured logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.after_request
def log_request(response):
    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "ip": request.remote_addr
        }
    )
    return response

@app.route('/health', methods=['GET'])
def health():
    logger.info("health check called")
    return jsonify({
        "status": "healthy",
        "time": datetime.now(timezone.utc).isoformat()
    }), 200

@app.route('/api/v1/records', methods=['GET'])
def get_records():
    records = [
        {"id": 1, "name": "Biomass Site A", "value": 4200},
        {"id": 2, "name": "Biomass Site B", "value": 3800},
    ]
    logger.info("records endpoint called, returning %d records", len(records))
    return jsonify({"data": records, "count": len(records)}), 200

@app.route('/api/v1/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    if record_id not in [1, 2]:
        logger.warning("record not found: %d", record_id)
        return jsonify({"error": "Record not found"}), 404
    logger.info("record %d retrieved", record_id)
    return jsonify({"id": record_id, "name": f"Biomass Site {record_id}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)