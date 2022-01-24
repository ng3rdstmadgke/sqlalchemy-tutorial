import sys
from db import base
from db import db
from pprint import pprint

def usage():
    print(f"""
[options]
  --create-all
  --drop-all
  --init
  --select-all
  --select-user <USER_ID>
  --add-file <USER_ID> <FILE_ID>
  --assoc-user-role <USER_ID> <ROLE_ID>
  --assoc-role-permission <ROLE_ID> <PERMISSION_ID>
  --delete-user <USER_ID>
  --delete-role <ROLE_ID>
  --delete-permission <PERMISSION_ID>
  --delete-file <USER_ID> <FILE_ID>
""")
    exit(1)

if __name__ == "__main__":
    # ジェネレータから要素を取得
    session = next(db.get_db())
    if len(sys.argv) <= 1:
        usage()
    if sys.argv[1] == "--create-all":
        # テーブル作成
        # https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=create%20table#sqlalchemy.schema.MetaData.create_all
        base.Base.metadata.create_all(db.engine)
    elif sys.argv[1] == "--drop-all":
        # テーブル削除
        # https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=create%20table#sqlalchemy.schema.MetaData.drop_all
        base.Base.metadata.drop_all(db.engine)
    elif sys.argv[1] == "--select-all":
        # クエリ: https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
        result = session.query(base.User).offset(0).limit(10).all()
        pprint(result)
    elif sys.argv[1] == "--select-user":
        # クエリ: https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
        user_id = sys.argv[2]
        result = session.query(base.User).filter(base.User.id == int(user_id)).first()
        pprint(result)
    elif sys.argv[1] == "--add-file":
        user_id = sys.argv[2]
        filename = sys.argv[3]
        user = session.query(base.User).filter(base.User.id == int(user_id)).first()
        user.files.append(base.File( name=filename, content=""))
        session.add(user)
        session.commit()
    elif sys.argv[1] == "--assoc-user-role":
        user_id = sys.argv[2]
        role_id = sys.argv[3]
        user = session.query(base.User).filter(base.User.id == int(user_id)).first()
        role = session.query(base.Role).filter(base.Role.id == int(role_id)).first()
        user.roles.append(role)
        session.add(user)
        session.commit()
    elif sys.argv[1] == "--assoc-role-permission":
        role_id = sys.argv[2]
        permission_id = sys.argv[3]
        role = session.query(base.Role).filter(base.Role.id == int(role_id)).first()
        permission = session.query(base.Permission).filter(base.Permission.id == int(permission_id)).first()
        role.permissions.append(permission)
        session.add(role)
        session.commit()
    elif sys.argv[1] == "--delete-user":
        user_id = sys.argv[2]
        user = session.query(base.User).filter(base.User.id == user_id).first()
        session.delete(user)
        session.commit()
    elif sys.argv[1] == "--delete-role":
        role_id = sys.argv[2]
        role = session.query(base.Role).filter(base.Role.id == role_id).first()
        session.delete(role)
        session.commit()
    elif sys.argv[1] == "--delete-permission":
        permission_id = sys.argv[2]
        permission = session.query(base.Permission).filter(base.Permission.id == permission_id).first()
        session.delete(permission)
        session.commit()
    elif sys.argv[1] == "--delete-file":
        user_id = sys.argv[2]
        file_id = sys.argv[3]
        file_obj = session.query(base.File).filter(base.File.user_id == user_id, base.File.id == file_id).first()
        session.delete(file_obj)
        session.commit()
    elif sys.argv[1] == "--init":
        admin_permission = base.Permission(name="Admin", description="admin permission")
        file_write_permission = base.Permission(name="FileWrite", description="file write permission")
        file_read_permission = base.Permission(name="FileRead", description="file read permission")

        admin_role = base.Role(
            name="Admin",
            description="admin",
            permissions=[ admin_permission, file_write_permission, file_read_permission ]
        )
        file_admin_role = base.Role(
            name="FileAdmin",
            description="file admin",
            permissions=[ file_write_permission, file_read_permission ]
        )
        user_role = base.Role(
            name="UserRole",
            description="user",
            permissions=[file_read_permission],
        )

        admin_user = base.User(
            username = "admin",
            hashed_password = "1234567890",
            is_superuser = True,
            is_active = True,
            roles=[ admin_role ],
            files=[]
        )
        file_admin_user = base.User(
            username = "file_admin",
            hashed_password = "1234567890",
            is_superuser = True,
            is_active = True,
            roles=[ file_admin_role ],
            files=[ base.File(name="file1", content="content1") ]
        )
        normal_user = base.User(
            username = "user",
            hashed_password = "1234567890",
            is_superuser = True,
            is_active = True,
            roles=[ user_role ],
            files=[ base.File(name="file2", content="content2"), base.File(name="file3", content="content3") ]
        )

        session.add(admin_user)
        session.add(file_admin_user)
        session.add(normal_user)
        session.commit()
    else:
        usage()