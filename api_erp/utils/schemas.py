from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None
    roles: List[str] = []


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RoleCreate(BaseModel):
    name_role: str
    permissions: List[str]


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    roles: List[str]
