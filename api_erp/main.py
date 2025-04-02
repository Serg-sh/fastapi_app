from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

api_erp: FastAPI = FastAPI()

api_erp.mount('/static', StaticFiles(directory='api_erp/static'), name='static')
templates = Jinja2Templates(directory='templates/api_erp')

origins = [
    "http://localhost",
    "http://localhost:3000",
]

api_erp.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
