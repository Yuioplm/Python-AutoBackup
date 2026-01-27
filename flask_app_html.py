from flask import Flask, render_template
from pathlib import Path
import csv

app = Flask(__name__)

# ===============================
# 設定
# ===============================
SCRIPT_DIR = Path(__file__).parent
CSV_PATH = SCRIPT_DIR / "backup" / "backup_list.csv"

# ===============================
# CSV 読み込み
# ===============================
def load_backup_csv(csv_path: Path):
    """
    backup_list.csvを読み込み、
    list[dict]として返す
    """
    if not csv_path.exists():
        return []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

# ===============================
# ルーティング
# ===============================    
@app.route("/")
def index():
    records = load_backup_csv(CSV_PATH)
    return render_template(
        "index.html",
        records = records
    )

# ===============================
# エントリーポイント
# ===============================
if __name__ == "__main__":
    app.run(debug=True)