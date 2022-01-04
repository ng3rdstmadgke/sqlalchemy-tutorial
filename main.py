import sys
import sqlalchemy
from pprint import pprint
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, scoped_session, sessionmaker
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import ForeignKey


DB_DIALECT="mysql"
DB_DRIVER="mysqldb" # mysqlclientならmysqldb, PyMySQLならpymysql
DB_USER="r00t"
DB_PASSWD="r00t1234"
DB_HOST="mido-dev02-devrds-db-back.cxh1e43zwtop.ap-northeast-1.rds.amazonaws.com"
DB_PORT="3306"
DB_NAME="sqlalchemy_tutorial" 

# モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
Base = declarative_base()

class UserRoles(Base):
    """userとroleの中間テーブル"""
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    # ForeignKeyには "テーブル名.カラム名" を指定
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)

class RolePermissions(Base):
    """roleとpermissionの中間テーブル"""
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("role.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permission.id"), nullable=False)

class User(Base):
    """userテーブル
    モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, index=True, unique=True)
    password = Column(String(30))
    # 一対多のリレーション: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    # カスケード: https://docs.sqlalchemy.org/en/14/orm/cascades.html
    terminology_files = relationship(
        "TerminologyFile",           # リレーションモデル名
        back_populates="users",      # リレーション先の変数名
        cascade="all, delete-orphan" # ユーザーを削除したときに、関連するterminology_fileを削除する(default="save-update")
    )
    # 中間テーブルを利用した多対多のリレーション: https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
    roles = relationship("Role", secondary=UserRoles.__tablename__, back_populates="users")

    def __repr__(self):
        return f'<User({self.id}, {self.name}, {self.password}, {self.terminology_files}, {self.roles})>'

class Role(Base):
    """roleテーブル"""
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True, unique=True)

    # リレーション
    users = relationship("User", secondary=UserRoles.__tablename__, back_populates="roles")
    permissions = relationship("Permission", secondary=RolePermissions.__tablename__, back_populates="roles")

    def __repr__(self):
        return f'<Role({self.name}, {self.permissions})>'


class Permission(Base):
    """permissionテーブル"""
    __tablename__ = "permission"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, index=True, unique=True)

    # リレーション
    roles = relationship("Role", secondary=RolePermissions.__tablename__, back_populates="permissions")

    def __repr__(self):
        return f'<Permission({self.name})>'


class TerminologyFile(Base):
    """terminology_fileテーブルの定義
    モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
    """
    __tablename__ = "terminology_file"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    filepath = Column(String(200))

    # リレーション
    users = relationship("User", back_populates="terminology_files")

    def __repr__(self):
        return f'<TerminologyFile({self.id}, {self.user_id}, {self.filepath})>'

def usage():
    print(f"""
[options]
  --connection
  --create-all
  --drop-all
  --select-all
  --select-user <USER_NAME>
  --add-superuser
  --add-user <USER_NAME>
  --add-role <ROLE_NAME>
  --add-permission <PERMISSION_NAME>
  --add-file <USER_NAME> <FILE_PATH>
  --add-file2 <USER_NAME> <FILE_PATH>
  --assoc-user-role <USER_NAME> <ROLE_NAME>
  --assoc-role-permission <USER_NAME> <ROLE_NAME>
  --delete-user <USER_ID>
  --delete-file <USER_ID> <FILE_ID>
[command]
  MYSQL_PWD={DB_PASSWD} mysql -u {DB_USER} -h {DB_HOST} {DB_NAME}
""")
    exit(1)

def conn():
    engine = sqlalchemy.create_engine(
        f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
    )
    conn = engine.connect()
    result = conn.execute(sqlalchemy.text("select 'hello world'"))
    print(result.all())
    conn.close()


if __name__ == "__main__":
    engine = sqlalchemy.create_engine(
        f'{DB_DIALECT}+{DB_DRIVER}://{DB_USER}:{DB_PASSWD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4'
    )
    # scoped_sessionで作成したセッションはシングルトンとなる
    # https://qiita.com/tosizo/items/86d3c60a4bb70eb1656e
    Session =  scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )

    if len(sys.argv) <= 1:
        usage()
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
    elif sys.argv[1] == "--select-all":
        with Session() as session:
            # クエリ: https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
            stmt = select(User)
            result = session.execute(stmt).scalars().all()
            pprint(result)
    elif sys.argv[1] == "--select-user":
        username = sys.argv[2]
        with Session() as session:
            stmt = select(User).filter_by(name=username)
            result = session.execute(stmt).scalar_one()
            pprint(result)
    elif sys.argv[1] == "--get-user":
        user_id = sys.argv[2]
        with Session() as session:
            result = session.get(User, int(user_id))
            pprint(result)
    elif sys.argv[1] == "--add-superuser":
        with Session() as session:
            p1 = Permission()
            p1.name = "AdminTerminologyFullAccess"

            p2 = Permission()
            p2.name = "PowerUserAccess"

            r1 = Role()
            r1.name = "AdminRole"
            r1.permissions.append(p1)
            r1.permissions.append(p2)

            u1 = User()
            u1.name = "admin"
            u1.password = "hogehoge"
            u1.roles.append(r1)
            session.add(u1)
            session.commit()
    elif sys.argv[1] == "--add-user":
        username = sys.argv[2]
        with Session() as session:
            user = User()
            user.name = username
            user.password = "hogehogehogehoge"
            session.add(user)
            session.commit()
    elif sys.argv[1] == "--add-role":
        rolename = sys.argv[2]
        with Session() as session:
            role = Role()
            role.name = rolename
            session.add(role)
            session.commit()
    elif sys.argv[1] == "--add-permission":
        permissionname = sys.argv[2]
        with Session() as session:
            permission = Permission()
            permission.name = permissionname
            session.add(permission)
            session.commit()
    elif sys.argv[1] == "--add-file":
        username = sys.argv[2]
        filename = sys.argv[3]
        with Session() as session:
            stmt = select(User).filter(User.name == username).order_by(User.id)
            user: User = session.execute(stmt).scalar_one()
            terminology_file = TerminologyFile()
            terminology_file.filepath = filename
            uid = user.id
            terminology_file.user_id = uid
            session.add(terminology_file)
            session.commit()
    elif sys.argv[1] == "--add-file2":
        username = sys.argv[2]
        filename = sys.argv[3]
        with Session() as session:
            terminology_file = TerminologyFile()
            terminology_file.filepath = filename
            stmt = select(User).filter(User.name == username).order_by(User.id)
            user: User = session.execute(stmt).first().scalar_one()
            user.terminology_files.append(terminology_file)
            session.add(user)
            session.commit()
    elif sys.argv[1] == "--assoc-user-role":
        user_name = sys.argv[2]
        role_name = sys.argv[3]
        with Session() as session:
            stmt = select(User).where(User.name == user_name)
            user: User = session.execute(stmt).first()[0]
            stmt = select(Role).where(Role.name == role_name)
            role: Role = session.execute(stmt).first()[0]
            user.roles.append(role)
            session.add(user)
            session.commit()
    elif sys.argv[1] == "--assoc-role-permission":
        role_name = sys.argv[2]
        permission_name = sys.argv[3]
        with Session() as session:
            stmt = select(Role).where(Role.name == role_name)
            role: Role = session.execute(stmt).first()[0]
            stmt = select(Permission).where(Permission.name == permission_name)
            permission: Permission = session.execute(stmt).first()[0]
            role.permissions.append(permission)
            session.add(role)
            session.commit()
    elif sys.argv[1] == "--delete-user":
        user_id = sys.argv[2]
        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            session.delete(user)
            session.commit()
    elif sys.argv[1] == "--delete-role":
        name = sys.argv[2]
        with Session() as session:
            pass
    elif sys.argv[1] == "--delete-permission":
        name = sys.argv[2]
        with Session() as session:
            pass
    elif sys.argv[1] == "--delete-file":
        user_id = sys.argv[2]
        file_id = sys.argv[3]
        with Session() as session:
            terminology_file = session \
                .query(TerminologyFile) \
                .filter(
                    TerminologyFile.user_id == user_id,
                    TerminologyFile.id == file_id
                ).first()
            session.delete(terminology_file)
            session.commit()
    else:
        usage()