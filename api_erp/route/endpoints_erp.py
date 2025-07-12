
from fastapi import APIRouter, Depends, HTTPException

from api_erp.utils import models
from auth import security



router_erp = APIRouter(prefix="/erp", tags=["ERP"])

@router_erp.get("/")
async def get_erp_info(current_user: models.User = Depends(security.get_current_user)):
    roles = security.get_user_roles(current_user)
    if "admin" in roles:
        return {"message": f"Вітаю, {current_user.email}! Ви маєте доступ як адміністратор."}
    elif "user" in roles:
        return {"message": f"Вітаю, {current_user.email}! Ви маєте доступ як користувач."}
    raise HTTPException(status_code=403, detail=f"{current_user.email} - Недостатньо прав")
