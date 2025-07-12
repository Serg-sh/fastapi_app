
from fastapi import APIRouter, Request

from core.templates import templates_erp

router_main = APIRouter(prefix="", tags=["Main"])

@router_main.get("/")
def home(request: Request):
    return templates_erp.TemplateResponse("index.html",
                                          {"request": request,
                                           "title": "RAX-ERP"})