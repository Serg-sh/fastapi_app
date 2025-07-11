from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import timedelta

from api_erp.utils import schemas, models
from api_erp.utils.database import get_pg_async_session
from auth import security

router = APIRouter(prefix="/api/v1")


@router.post("/login/token", response_model=schemas.Token)
async def login_for_access_token(response: Response,
                                 login_data: schemas.UserLogin,
                                 db: AsyncSession = Depends(get_pg_async_session)
                                 ):

    user = await security.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невірний email або пароль"
        )
    roles = security.get_user_roles(user)
    access_token = security.create_access_token(
        data={"sub": user.email, "user_id": user.id, "roles": roles},
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=security.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/permissions", status_code=201)
async def create_permission(name_perm: str,
                            db: AsyncSession = Depends(get_pg_async_session)
                            ):

    from sqlalchemy import select
    result = await db.execute(select(models.Permission).where(models.Permission.name_perm == name_perm))
    existing_perm = result.scalar_one_or_none()
    if existing_perm:
        raise HTTPException(status_code=400, detail="Дозвіл з таким іменем вже існує")
    new_perm = models.Permission(name_perm=name_perm)
    db.add(new_perm)
    await db.commit()
    await db.refresh(new_perm)
    return {"id": new_perm.id, "name_perm": new_perm.name_perm}

@router.post("/roles", status_code=201)
async def create_role(role_data: schemas.RoleCreate,
                      db: AsyncSession = Depends(get_pg_async_session)
                      ):
    from sqlalchemy import select
    # Перевірка, чи існує роль
    result = await db.execute(select(models.Role).where(models.Role.name_role == role_data.name_role))
    existing_role = result.scalar_one_or_none()
    if existing_role:
        raise HTTPException(status_code=400, detail="Роль з таким іменем вже існує")
    # Знаходимо дозволи
    permissions = []
    for perm_name in role_data.permissions:
        perm_result = await db.execute(select(models.Permission).where(models.Permission.name_perm == perm_name))
        perm = perm_result.scalar_one_or_none()
        if not perm:
            raise HTTPException(status_code=400, detail=f"Дозвіл '{perm_name}' не існує")
        permissions.append(perm)
    new_role = models.Role(name_role=role_data.name_role, permissions=permissions)
    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)
    return {"id": new_role.id, "name_role": new_role.name_role,
            "permissions": [p.name_perm for p in new_role.permissions]}


@router.post("/register", status_code=201)
async def register_user(user_data: schemas.UserCreate,
                        db: AsyncSession = Depends(get_pg_async_session)
                        ):

    from sqlalchemy import select
    # Перевірка, чи існує користувач з таким email
    result = await db.execute(select(models.User).where(models.User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Користувач з таким email вже існує")
    hashed_password = security.get_password_hash(user_data.password)
    # Додаємо ролі
    roles = []
    for role_name in user_data.roles:
        role_result = await db.execute(select(models.Role).where(models.Role.name_role == role_name))
        role = role_result.scalar_one_or_none()
        if not role:
            raise HTTPException(status_code=400, detail=f"Роль '{role_name}' не існує")
        roles.append(role)
    new_user = models.User(email=user_data.email, password=hashed_password, roles=roles)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    # Підвантажуємо ролі асинхронно через selectinload
    result = await db.execute(
        select(models.User)
        .options(selectinload(models.User.roles))
        .where(models.User.id == new_user.id)
    )
    user_with_roles = result.scalar_one_or_none()
    return {"id": user_with_roles.id, "email": user_with_roles.email,
            "roles": [r.name_role for r in user_with_roles.roles]}


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_pg_async_session)):
    from sqlalchemy import select
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    await db.delete(user)
    await db.commit()
    return Response(status_code=204)



# Приклад захищеного ендпоінта
@router.get("/protected-resource")
async def protected_resource(
        current_user: models.User = Depends(security.get_current_user)
):
    roles = security.get_user_roles(current_user)
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Недостатньо прав")
    return {"message": f"Вітаю, {current_user.email}! Ви маєте доступ як адміністратор."}
