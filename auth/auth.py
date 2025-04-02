from functools import wraps
from fastapi import HTTPException, status, Request, Depends
from typing import Optional, List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session
from sqlalchemy.orm import selectinload

from api_erp.database.models import User, UserRole, Permission


async def get_current_user(request: Request) -> User:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    async with async_session() as session:
        user = await session.execute(
            select(User).where(User.id == user_id).options(
                selectinload(User.permissions)  # Підвантажуємо права
            )
        )
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user


def has_permission(permission: Permission):
    async def permission_checker(user: User = Depends(get_current_user)):
        if permission not in [p.name for p in user.permissions] and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission {permission.value} required"
            )
        return user

    return permission_checker


def requiresAuth(roles: Optional[List[UserRole]] = None,
                 permissions: Optional[List[Permission]] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(
                request: Request,
                *args,
                **kwargs
        ):
            # Отримуємо поточного користувача
            user = await get_current_user(request)

            # Перевірка ролей
            if roles and user.role not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Required roles: {[r.value for r in roles]}"
                )

            # Перевірка прав
            if permissions:
                user_perms = [p.name for p in user.permissions]
                if not all(perm in user_perms for perm in permissions):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Required permissions: {[p.value for p in permissions]}"
                    )

            # Якщо все ОК - виконуємо роут
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
