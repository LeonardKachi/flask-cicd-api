from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

# Health check - every production system needs this
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "time": datetime.now(timezone.utc).isoformat()
    }), 200

# Sample data endpoint
@app.route('/api/v1/records', methods=['GET'])
def get_records():
    records = [
        {"id": 1, "name": "Biomass Site A", "value": 4200},
        {"id": 2, "name": "Biomass Site B", "value": 3800},
    ]
    return jsonify({"data": records, "count": len(records)}), 200

# Single record endpoint
@app.route('/api/v1/records/<int:record_id>', methods=['GET'])
def get_record(record_id):
    if record_id not in [1, 2]:
        return jsonify({"error": "Record not found"}), 404
    return jsonify({"id": record_id, "name": f"Biomass Site {record_id}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
