# Python-AutoBackup

Documents フォルダ配下の「最近更新されたファイル」を抽出し、
フォルダ構造を維持したまま backup フォルダへコピーする
Python バックアップスクリプトです。

コピー結果は CSV とログファイルに出力されます。


## 概要

このスクリプトは以下を行います。

- Documents フォルダ配下を再帰的に走査
- 直近 30 日以内に更新されたファイルを抽出
- フォルダ構造を保持したまま backup フォルダへコピー
- コピー結果を CSV に出力
- 実行ログを logs/backup.log に記録

バックアップ先フォルダは自動的に除外されます。


## 対象フォルダ

対象フォルダは以下に固定されています。

Path.home() / "Documents"


## 抽出条件

以下の条件をすべて満たすファイルが対象になります。

- 最終更新日時が直近 30日以内
- backup フォルダ配下ではない


## フォルダ構成

Python-AutoBackup/  
 ├─ backup/  
 │   └─ （バックアップされたファイル）  
 ├─ logs/  
 │   └─ backup.log  
 ├─ backup.py  
 └─ README.md

※ backup フォルダ、logs フォルダは実行時に自動作成されます。


## バックアップ先

バックアップ先は、スクリプトと同じディレクトリ配下の backup フォルダです。

<スクリプト配置フォルダ>\backup\

Documents 配下のフォルダ構造を維持したままコピーされます。


## CSV 出力ファイル

コピー結果は以下の CSV に出力されます。

backup/backup_list.csv


### CSV 列

FileName        ファイル名  
OriginalPath   元のフルパス  
LastWriteTime  最終更新日時  
CopiedAt       コピー実行日時  
Status         Success または Skipped


## ログファイル

ログは以下に出力されます。

logs/backup.log


### ログ内容

- バックアップ開始・終了
- 対象フォルダ
- 基準日
- 対象ファイル件数
- 各ファイルのコピー結果 SUCCESS / SKIPPED
- SUMMARY を確認可能


### ログ例

2026-01-15 09:00:01 [INFO] === Backup Start ===  
2026-01-15 09:00:01 [INFO] Source: C:\Users\User\Documents  
2026-01-15 09:00:01 [INFO] BorderDate: 2025-12-15  
2026-01-15 09:00:02 [INFO] Success : C:\Users\User\Documents\sample.txt  
2026-01-15 09:00:02 [WARNING] Skipped : C:\Users\User\Documents\open.xlsx  
2026-01-15 09:00:03 [INFO] SUMMARY: Success=5, Skipped=1 
2026-01-15 09:00:03 [INFO] === Backup End ===  


## 実行方法

以下を実行します。

python backup.py


## 注意事項

- backupフォルダはコピー対象から除外されます
