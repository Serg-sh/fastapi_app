
from fastapi import Request
from api_erp.main import app_api_erp

@app_api_erp.get("/admin/dashboard")
async def admin_dashboard(request: Request):
    return {"message": "Welcome to Admin Dashboard"}