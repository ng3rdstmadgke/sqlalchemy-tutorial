import sys
from db import base
from db import db

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
""")
    exit(1)

if __name__ == "__main__":
    Session = db.get_db()
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
    elif sys.argv[1] == "--init":
        session = next(db.get_db())
        admin_permission = base.Permission(
            name="Admin",
            description="admin permission",
        )

        file_write_permission = base.Permission(
            name="FileWrite",
            description="file write permission",
        )

        file_read_permission = base.Permission(
            name="FileRead",
            description="file read permission",
        )

        admin_role = base.Role(
            name="Admin",
            description="admin",
            permissions=[
                admin_permission,
                file_write_permission,
                file_read_permission,
            ]
        )

        file_admin_role = base.Role(
            name="FileAdmin",
            description="file admin",
            permissions=[
                file_write_permission,
                file_read_permission,
            ]
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
            files=[
                base.File(name="file1", content="content1")
            ]
        )

        normal_user = base.User(
            username = "user",
            hashed_password = "1234567890",
            is_superuser = True,
            is_active = True,
            roles=[ user_role ],
            files=[
                base.File(name="file2", content="content2"),
                base.File(name="file3", content="content3"),
            ]
        )
        session.add(admin_user)
        session.add(file_admin_user)
        session.add(normal_user)
        session.commit()



#    elif sys.argv[1] == "--select-all":
#        with Session() as session:
#            # クエリ: https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
#            stmt = select(User)
#            result = session.execute(stmt).scalars().all()
#            pprint(result)
#    elif sys.argv[1] == "--select-user":
#        username = sys.argv[2]
#        with Session() as session:
#            stmt = select(User).filter_by(name=username)
#            result = session.execute(stmt).scalar_one()
#            pprint(result)
#    elif sys.argv[1] == "--get-user":
#        user_id = sys.argv[2]
#        with Session() as session:
#            result = session.get(User, int(user_id))
#            pprint(result)
#    elif sys.argv[1] == "--add-superuser":
#        with Session() as session:
#            p1 = Permission()
#            p1.name = "AdminTerminologyFullAccess"
#
#            p2 = Permission()
#            p2.name = "PowerUserAccess"
#
#            r1 = Role()
#            r1.name = "AdminRole"
#            r1.permissions.append(p1)
#            r1.permissions.append(p2)
#
#            u1 = User()
#            u1.name = "admin"
#            u1.password = "hogehoge"
#            u1.roles.append(r1)
#            session.add(u1)
#            session.commit()
#    elif sys.argv[1] == "--add-user":
#        username = sys.argv[2]
#        with Session() as session:
#            user = User()
#            user.name = username
#            user.password = "hogehogehogehoge"
#            session.add(user)
#            session.commit()
#    elif sys.argv[1] == "--add-role":
#        rolename = sys.argv[2]
#        with Session() as session:
#            role = Role()
#            role.name = rolename
#            session.add(role)
#            session.commit()
#    elif sys.argv[1] == "--add-permission":
#        permissionname = sys.argv[2]
#        with Session() as session:
#            permission = Permission()
#            permission.name = permissionname
#            session.add(permission)
#            session.commit()
#    elif sys.argv[1] == "--add-file":
#        username = sys.argv[2]
#        filename = sys.argv[3]
#        with Session() as session:
#            stmt = select(User).filter(User.name == username).order_by(User.id)
#            user: User = session.execute(stmt).scalar_one()
#            terminology_file = TerminologyFile()
#            terminology_file.filepath = filename
#            uid = user.id
#            terminology_file.user_id = uid
#            session.add(terminology_file)
#            session.commit()
#    elif sys.argv[1] == "--add-file2":
#        username = sys.argv[2]
#        filename = sys.argv[3]
#        with Session() as session:
#            terminology_file = TerminologyFile()
#            terminology_file.filepath = filename
#            stmt = select(User).filter(User.name == username).order_by(User.id)
#            user: User = session.execute(stmt).first().scalar_one()
#            user.terminology_files.append(terminology_file)
#            session.add(user)
#            session.commit()
#    elif sys.argv[1] == "--assoc-user-role":
#        user_name = sys.argv[2]
#        role_name = sys.argv[3]
#        with Session() as session:
#            stmt = select(User).where(User.name == user_name)
#            user: User = session.execute(stmt).first()[0]
#            stmt = select(Role).where(Role.name == role_name)
#            role: Role = session.execute(stmt).first()[0]
#            user.roles.append(role)
#            session.add(user)
#            session.commit()
#    elif sys.argv[1] == "--assoc-role-permission":
#        role_name = sys.argv[2]
#        permission_name = sys.argv[3]
#        with Session() as session:
#            stmt = select(Role).where(Role.name == role_name)
#            role: Role = session.execute(stmt).first()[0]
#            stmt = select(Permission).where(Permission.name == permission_name)
#            permission: Permission = session.execute(stmt).first()[0]
#            role.permissions.append(permission)
#            session.add(role)
#            session.commit()
#    elif sys.argv[1] == "--delete-user":
#        user_id = sys.argv[2]
#        with Session() as session:
#            user = session.query(User).filter(User.id == user_id).first()
#            session.delete(user)
#            session.commit()
#    elif sys.argv[1] == "--delete-role":
#        name = sys.argv[2]
#        with Session() as session:
#            pass
#    elif sys.argv[1] == "--delete-permission":
#        name = sys.argv[2]
#        with Session() as session:
#            pass
#    elif sys.argv[1] == "--delete-file":
#        user_id = sys.argv[2]
#        file_id = sys.argv[3]
#        with Session() as session:
#            terminology_file = session \
#                .query(TerminologyFile) \
#                .filter(
#                    TerminologyFile.user_id == user_id,
#                    TerminologyFile.id == file_id
#                ).first()
#            session.delete(terminology_file)
#            session.commit()
#    else:
#        usage()