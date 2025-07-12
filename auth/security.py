from datetime import datetime, timedelta, timezone
from typing import Optional, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api_erp.utils import models, schemas
from api_erp.utils.database import get_pg_async_session

# Налаштування безпеки
SECRET_KEY = "ваш_секретний_ключ_тут"  # перенести в .env файл
ALGORITHM = "HS256"  # перенести в .env файл
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # перенести в .env файл

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSession, email: str, password: str):
    result = await db.execute(select(models.User)
                              .options(selectinload(models.User.roles)
                                       .selectinload(models.Role.permissions))
                              .where(models.User.email == email)
                              )
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_token_from_request(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ", 1)[1]
    return token


async def get_current_user(request: Request,
                           db: AsyncSession = Depends(get_pg_async_session)) -> models.User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Не вдалося підтвердити облікові дані",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = get_token_from_request(request)
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if email is None or user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.roles).selectinload(models.Role.permissions))
        .where(models.User.email == token_data.email)
    )
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


def get_user_roles(user: models.User) -> list[str]:
    return [role.name_role for role in user.roles]


def get_user_permissions(user: models.User) -> list[str]:
    permissions = set()
    for role in user.roles:
        for perm in role.permissions:
            permissions.add(perm.name_perm)
    return list(permissions)
