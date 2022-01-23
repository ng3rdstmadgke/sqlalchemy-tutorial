from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from db.base_class import Base

class User(Base):
    """usersテーブル
    モデル定義: https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#defining-table-metadata-with-the-orm
    """
    __tablename__ = "users"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}
    

    id = Column(Integer, primary_key=True, index=True)
    # collation(照合順序)
    # https://dev.mysql.com/doc/refman/8.0/ja/charset-mysql.html
    username = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # 一対多のリレーション
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#one-to-many
    files = relationship(
        "File",           # リレーションモデル名
        back_populates="users",      # リレーション先の変数名
        # カスケード: https://docs.sqlalchemy.org/en/14/orm/cascades.html
        # "all, delete-orphan": userを削除したときに、関連するfilesを削除する
        # "save-update": userを削除したときに、関連するfilesのuser_idをNullにする (default)
        cascade="all, delete-orphan",
    )
    # 中間テーブルを利用した多対多のリレーション
    # https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    def __repr__(self):
        return f"""<User(
    id={self.id},
    hashed_password={self.hashed_password},
    username={self.username},
    is_superuser={self.is_superuser},
    is_active={self.is_active},
    files={self.files},
    roles={self.roles}
)>"""