from flask import Flask, jsonify
import csv
from pathlib import Path

app = Flask(__name__)

@app.route("/backup-status")
def backup_status():
    csv_path = Path("backup/backup_list.csv")
    if not csv_path.exists():
        return jsonify({"error": "No backup CSV found"}), 404
    
    result = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append(row)
    
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)