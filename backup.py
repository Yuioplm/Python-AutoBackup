#!/usr/bin/env python3

import argparse
from pathlib import Path
from datetime import datetime, timedelta
import shutil
import csv
import logging
import sys

# ===============================
# 引数解析
# ===============================
def parse_args():
    parser = argparse.ArgumentParser(
        description="AutoBackup: copy recently modified files"
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Source directory to scan"
    )
    parser.add_argument(
        "--backup",
        required=True,
        help="Backup root directory"
    )

    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Files modified within N days (default: 30)"
    )
    return parser.parse_args()

# ===============================
# ログ設定
# ===============================
def setup_logger(log_dir: Path):
    log_dir = log_dir.resolve()
    log_dir.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "backup.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

# ===============================
# バックアップ処理
# ===============================
def backup_files(src_dir :Path, backup_root :Path, border_date: datetime):
    logging.info("=== Backup Start ===")
    logging.info(f"Source: {src_dir}")
    logging.info(f"BackupRoot: {backup_root}")
    logging.info(f"BorderDate: {border_date}")

    results = []

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
        if last_modified < border_date:
            continue

        relative_path = path.relative_to(src_dir)
        dst_path = backup_root / relative_path
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(path, dst_path)
            status = "Success"
            logging.info(f"SUCCESS: {path}")
        except Exception as e:
            status = "Skipped"
            logging.warning(f"SKIPPED: {path}({e})")
        
        results.append({
            "FileName" : path.name,
            "OriginalPath" : str(path),
            "LastWriteTime" : last_modified.isoformat(),
            "CopiedAt" : datetime.now().isoformat(),
            "Status" : status
        })

    return results

# ===============================
# CSV 出力
# ===============================
def export_csv(results, csv_path :Path):
    if not results:
        return

    csv_path.parent.mkdir(parents=True, exist_ok=True)

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
    args = parse_args()

    src_dir = Path(args.source).resolve()
    backup_root = Path(args.backup).resolve()
    border_date = datetime.now() - timedelta(days=args.days)

    script_dir = Path(__file__).parent
    log_dir = script_dir / "logs"
    csv_path = backup_root / "backup_list.csv"

    setup_logger(log_dir)

    try:
        results = backup_files(src_dir, backup_root, border_date)
        export_csv(results, csv_path)

        success = sum(1 for r in results if r["Status"] == "Success")
        skipped = sum(1 for r in results if r["Status"] != "Success")

        logging.info(f"SUMMARY: Success={success}, Skipped={skipped}")
        logging.info("=== Backup End ===")
    
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        logging.error("Backup aborted")
        sys.exit(1)

if __name__ == "__main__":
    main()