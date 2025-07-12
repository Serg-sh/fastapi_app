from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from api_erp.route import endpoints_main, endpoints_osi, endpoints_erp
from api_erp.utils.database import init_pg_db
from auth import endpoints_auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_pg_db()  # Створюємо таблиці
    yield

app_erp: FastAPI = FastAPI(title='RAX-ERP',
                           lifespan=lifespan)


# Registering routers
app_erp.include_router(endpoints_auth.router_auth, tags=['Auth'])
app_erp.include_router(endpoints_osi.router_osi, tags=['OSI'])
app_erp.include_router(endpoints_erp.router_erp, tags=['ERP'])
app_erp.include_router(endpoints_main.router_main, tags=['Main'])


# Mounting static files directory
app_erp.mount('/static', StaticFiles(directory='static'), name='static')


# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
]

# Adding CORS middleware to the FastAPI application
app_erp.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
