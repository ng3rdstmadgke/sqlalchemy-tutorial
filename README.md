インストール
```bash
python3.8 -m venv  .venv
source ./venv/bin/activate
pip install -r requirements.txt
```

環境変数読み込み
```
cp sample.env .env
vim .env
export $(cat .env | grep -v -e "^ *#")
```

DB作成
```bash
MYSQL_PWD=xxxxxxxx mysql -u xxxx -h xxxxxxx.com -e "create database sqlalchemy_tutorial"
```

マイグレーション
```bash
# マイグレーションスクリプト生成
# alembic/versions/配下のマイグレーションスクリプトと
# バージョンを管理用テーブル(alembic_version)が生成され、
alembic revision --autogenerate -m "create initial table"

# 最新のバージョンまでマイグレーション
# alembic_versionテーブルに適用されたバージョンが追記される。
alembic upgrade head

# 一番最初までロールバック
# alembic_versionテーブルからバージョンが削除される。
alembic downgrade base

# マイグレーション履歴の確認
alembic history -v

# 次のバージョンにマイグレーション
alembic upgrade +1

# 前のバージョンにロールバック
alembic downgrade -1
```

DBログイン
```bash
./bin/login.sh
```

クエリ実行
```bash
# テーブル作成
python main.py --drop-all && python main.py --create-all

# 初期データ登録
python main.py --init
```
