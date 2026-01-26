#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime, timedelta
import shutil
import csv
import logging
import sys

# ===============================
# 設定
# ===============================
SOURCE_DIR = Path.home() / "Documents"
SCRIPT_DIR = Path(__file__).parent
BACKUP_ROOT = SCRIPT_DIR / "backup"
LOG_DIR = SCRIPT_DIR / "logs"
CSV_PATH = BACKUP_ROOT / "backup_list.csv"

BORDER_DATE = datetime.now() - timedelta(days=30)

# ===============================
# ログ設定
# ===============================
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "backup.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ===============================
# バックアップ処理
# ===============================
def backup_files(src_dir :Path, backup_root :Path):
    logging.info("=== Backup Start ===")
    logging.info(f"Source: {src_dir}")
    logging.info(f"BorderDate: {BORDER_DATE}")

    results = []

    try:
        if not src_dir.exists():
            raise FileNotFoundError(f"Source not found: {src_dir}")
        
        backup_root.mkdir(exist_ok=True)

        for path in src_dir.rglob("*"):
            if not path.is_file():
                continue

            # バックアップフォルダを除外
            if backup_root in path.parents:
                continue

            last_modified = datetime.fromtimestamp(path.stat().st_mtime)
            if last_modified < BORDER_DATE:
                continue

            relative_path = path.relative_to(src_dir)
            dst_path = backup_root / relative_path
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                shutil.copy2(path, dst_path)
                status = "Success"
                logging.info(f"SUCCESS: {path}")
            except Exception:
                status = "Skipped"
                logging.warning(f"SKIPPED: {path}")
            
            results.append({
                "FileName" : path.name,
                "OriginalPath" : str(path),
                "LastWriteTime" : last_modified,
                "CopiedAt" : datetime.now(),
                "Status" : status
            })
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        raise

    return results

# ===============================
# CSV 出力
# ===============================
def export_csv(results, csv_path :Path):
    if not results:
        return
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["FileName", "OriginalPath", "LastWriteTime", "CopiedAt", "Status"]
        )
        writer.writeheader()
        writer.writerows(results)

# ===============================
# main
# ===============================
def main():
    try:
        results = backup_files(SOURCE_DIR, BACKUP_ROOT)
        export_csv(results, CSV_PATH)

        success = sum(1 for r in results if r["Status"] == "Success")
        skipped = sum(1 for r in results if r["Status"] != "Success")

        logging.info(f"SUMMARY: Success={success}, Skipped={skipped}")
        logging.info("=== Backup End ===")
    
    except Exception:
        logging.error("Backup aborted")
        sys.exit(1)

if __name__ == "__main__":
    main()