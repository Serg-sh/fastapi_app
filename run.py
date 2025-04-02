import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api_erp.main import api_erp
from main_config import logging_config

app: FastAPI = api_erp  # main app
logger = logging.getLogger(__name__)
logging_config(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# seconds app
# app.mount("/", )
# app.mount("", )
# app.mount("/", )

main_app = app


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app = 'run:main_app',
                host='127.0.0.1',
                port=8000,
                log_level='info',
                reload=True,)