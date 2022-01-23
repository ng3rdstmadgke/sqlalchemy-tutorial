from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey

from db.base_class import Base

class UserRoles(Base):
    """usersとroleの中間テーブル"""
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    # ForeignKeyには "テーブル名.カラム名" を指定
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

class Role(Base):
    """rolesテーブル"""
    __tablename__ = "roles"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    description = Column(String(255))
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # リレーション
    users = relationship("User", secondary=UserRoles.__tablename__, back_populates="roles")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")

    def __repr__(self):
        return f"""<Role(id={self.id}, name={self.name}, description={self.description}, permissions={self.permissions})>"""
