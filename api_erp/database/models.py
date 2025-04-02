from sqlalchemy import Column, Integer, String, Enum, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

Base = declarative_base()

# Допоміжна таблиця для зв'язку many-to-many (користувач ↔ права)
user_permission = Table(
    "user_permission",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("permission_id", Integer, ForeignKey("permissions.id")),
)

class UserRole(PyEnum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class Permission(PyEnum):
    CREATE_ITEM = "create_item"
    DELETE_USER = "delete_user"
    VIEW_STATS = "view_stats"
    EDIT_ITEM = "edit_item"

class PermissionModel(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True)
    name = Column(Enum(Permission), unique=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USER)
    permissions = relationship("PermissionModel", secondary=user_permission)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_id = Column(Integer)