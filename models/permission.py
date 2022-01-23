from datetime import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.schema import ForeignKey

from db.base_class import Base

class RolePermissions(Base):
    """rolesとpermissionsの中間テーブル"""
    __tablename__ = "role_permissions"
    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)

class Permission(Base):
    """permissionテーブル"""
    __tablename__ = "permissions"
    __table_args__ = {'mysql_engine':'InnoDB', 'mysql_charset':'utf8mb4','mysql_collate':'utf8mb4_bin'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255, collation="utf8mb4_bin"), unique=True, index=True, nullable=False)
    description = Column(String(255))
    created = Column(DateTime, default=datetime.now, nullable=False)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # リレーション
    roles = relationship("Role", secondary=RolePermissions.__tablename__, back_populates="permissions")

    def __repr__(self):
        return f"""<Permission(id={self.id}, name={self.name}, description={self.description},)>"""