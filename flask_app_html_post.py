from flask import Flask, render_template, redirect, url_for
from pathlib import Path
from datetime import datetime, timedelta

# 既存のバックアップ処理を再利用
from backup import backup_files, export_csv

app = Flask(__name__)

# ===============================
# ルーティング
# ===============================    
@app.route("/", methods=["GET"])
def index():
    """
    初期画面表示
    """
    return render_template("index.html")

@app.route("/run-backup", methods=["POST"])
def run_backup():
    """
    webからバックアップを実行
    """
    # --- フォームから値を取得 --- #
    source = request.form.get("source")
    backup = request.form.get("backup")
    days = int(request.form.get("days", 30))

    src_dir = Path(source).resolve()
    backup_root = Path(backup).resolve()
    border_date = datetime.now() - timedelta(days=days)

    csv_path = backup_root / "backup_list.csv"

    try:
        results = backup_files(src_dir, backup_root, border_date)
        export_csv(results, csv_path)

        success = sum(1 for r in results if r["Status"] == "Success")
        skipped = sum(1 for r in results if r["Status"] != "Success")

        message = f"Backup finished: Success={success}, Skipped={skipped}"

    except Exception as e:
        message =f"Backup failed: {e}"
    
    return render_template("index.html", message=message)

# ===============================
# エントリーポイント
# ===============================
if __name__ == "__main__":
    app.run(debug=True)