from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from api_erp.utils.database import init_pg_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pg_db()  # Створюємо таблиці
    yield

app_api_erp: FastAPI = FastAPI(title='RAX-ERP',
                               lifespan=lifespan)

app_api_erp.mount('/static', StaticFiles(directory='static/api_erp'), name='static')
templates = Jinja2Templates(directory='templates/api_erp')

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app_api_erp.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
