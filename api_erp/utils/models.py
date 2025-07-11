from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# Таблиця для зв'язку ролей і дозволів
role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

# Таблиця для зв'язку користувачів і ролей
user_roles = Table(
    'user_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True)
    name_perm = Column(String, unique=True, nullable=False)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name_role = Column(String, unique=True, nullable=False)
    permissions = relationship('Permission', secondary=role_permissions, backref='roles')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    status = Column(Boolean, default=True)
    roles = relationship('Role', secondary=user_roles, backref='users')
