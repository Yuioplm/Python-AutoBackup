from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import csv

# 既存のバックアップ処理を再利用
from backup import backup_files, export_csv

app = Flask(__name__)

# =========================
# CSV読み込み 
# =========================
def load_backup_csv(csv_path):
    if not csv_path.exists():
        return []
    
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

# =========================
# 画面表示 
# =========================
@app.route("/", methods=["GET"])
def index():
    backup_root = Path(__file__).parent / "backup"
    csv_path = backup_root / "backup_list.csv"

    records = load_backup_csv(csv_path)

    return render_template("index.html", records=records)

# =========================
# POST : バックアップ実行 
# =========================
@app.route("/run", methods=["POST"])
def run_backup():

    source = request.form.get("source")
    destination = request.form.get("destination")
    border_date = request.form.get("days")

    source_path = Path(source).resolve()
    destination_path = Path(destination).resolve()

    # バックアップ実行
    result = backup_files(source_path, destination_path, border_date)

    # CSV出力
    csv_path = destination_path / "backup_list.csv"
    export_csv(result, csv_path)

    # 実行後トップへ戻す
    return redirect(url_for("index"))

# =========================
# 起動 
# =========================
if __name__ == "__main__":
    app.run(debug=True)