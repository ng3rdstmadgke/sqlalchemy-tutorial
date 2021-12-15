インストール
```bash
python3.8 -m venv  .venv
source ./venv/bin/activate
pip install -r requirements.txt
```

DB作成
```bash
MYSQL_PWD=r00t1234 mysql -u r00t -h mido-dev02-devrds-db-back.cxh1e43zwtop.ap-northeast-1.rds.amazonaws.com -e "create database sqlalchemy_tutorial"
```

クエリ実行
```bash
# テーブル作成
python main.py --drop-all && python main.py --create-all

# insert
python main.py --insert

# select
python main.py --select
```