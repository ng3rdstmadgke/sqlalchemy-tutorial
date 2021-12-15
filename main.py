import sys
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, scoped_session, sessionmaker
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import ForeignKey


DB_DIALECT="mysql"
DB_DRIVER="mysqldb" # mysqlclientならmysqldb, PyMySQLならpymysql
DB_USER="r00t"
DB_PASSWD="r00t1234"
DB_HOST="mido-dev02-devrds-db-back.cxh1e43zwtop.ap-northeast-1.rds.amazonaws.com"
DB_PORT="3306"
DB_DBNAME="sqlalchemy_tutorial" 

# モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
Base = declarative_base()

class UserRoles(Base):
    """userとroleの中間テーブル"""
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    # ForeignKeyには "テーブル名.カラム名" を指定
    user_id = Column(Integer, ForeignKey("user.id"))
    role_id = Column(Integer, ForeignKey("role.id"))

class RolePermissions(Base):
    """roleとpermissionの中間テーブル"""
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    permission_id = Column(Integer, ForeignKey("permission.id"))


class User(Base):
    """userテーブル
    モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(30))
    # 一対多のリレーション: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # relationship("リレーション先モデルクラス名" , back_poplulates="自テーブル名")
    terminology_file = relationship("TerminologyFile", back_populates="user")
    # 中間テーブルを利用した多対多のリレーション: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
    role = relationship("Role", secondary=UserRoles.__tablename__, back_populates="user")

    def __repr__(self):
        return f'<User({self.username}, {self.password}, {self.terminology_file}, {self.role})>'

class Role(Base):
    """roleテーブル"""
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))

    # リレーション
    user = relationship("User", secondary=UserRoles.__tablename__, back_populates="role")
    permission = relationship("Permission", secondary=RolePermissions.__tablename__, back_populates="role")

    def __repr__(self):
        return f'<Role({self.name}, {self.permission})>'


class Permission(Base):
    """permissionテーブル"""
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))

    # リレーション
    role = relationship("Role", secondary=RolePermissions.__tablename__, back_populates="permission")

    def __repr__(self):
        return f'<Permission({self.name})>'


class TerminologyFile(Base):
    """terminology_fileテーブルの定義
    モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
    """
    __tablename__ = "terminology_file"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    # リレーション
    user = relationship("User", back_populates="terminology_file")

def usage():
    print("""
[options]
--connection
--create-all
--drop-all
""")

def conn():
    engine = sqlalchemy.create_engine(
        f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_DBNAME}?charset=utf8mb4'
    )
    conn = engine.connect()
    result = conn.execute(sqlalchemy.text("select 'hello world'"))
    print(result.all())
    conn.close()

if __name__ == "__main__":
    engine = sqlalchemy.create_engine(
        f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_DBNAME}?charset=utf8mb4'
    )
    # scoped_sessionで作成したセッションはシングルトンとなる
    # https://qiita.com/tosizo/items/86d3c60a4bb70eb1656e
    Session =  scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    if sys.argv[1] == "--conn":
        conn()
    elif sys.argv[1] == "--create-all":
        # テーブル作成
        # https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=create%20table#sqlalchemy.schema.MetaData.create_all
        Base.metadata.create_all(engine)
    elif sys.argv[1] == "--drop-all":
        # テーブル削除
        # https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=create%20table#sqlalchemy.schema.MetaData.drop_all
        Base.metadata.drop_all(engine)
    elif sys.argv[1] == "--insert":
        with Session() as session:
            p1 = Permission()
            p1.name = "AdminTerminologyFullAccess"
            session.add(p1)

            p2 = Permission()
            p2.name = "AdminTerminologyReadOnlyAccess"
            session.add(p2)

            p3 = Permission()
            p3.name = "PowerUserAccess"
            session.add(p3)

            r1 = Role()
            r1.name = "AdminRole"
            r1.permission.append(p1)
            r1.permission.append(p3)
            session.add(r1)

            r2 = Role()
            r2.name = "NormalRole"
            r2.permission.append(p2)
            session.add(r2)

            session.commit()
        
        with Session() as session:
            u1 = User()
            u1.username = "admin"
            u1.password = "hogehoge"
            u1.role.append(r1)
            session.add(u1)

            u2 = User()
            u2.username = "ktamido"
            u2.password = "fugafuga"
            u2.role.append(r2)
            session.add(u2)

            session.commit()
    elif sys.argv[1] == "--select":
        with Session() as session:
            # クエリ: https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
            stmt = select(User)
            result = session.execute(stmt).scalars().all()
            print(result)

            stmt = select(User).filter_by(username="admin")
            result = session.execute(stmt).all()
            print(result)


    else:
        usage()