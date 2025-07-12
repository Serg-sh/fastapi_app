import logging

from fastapi import FastAPI

from core.logger import logging_config
from main_api_erp import app_erp

app: FastAPI = app_erp  # main app
logger = logging.getLogger(__name__)
logging_config(level=logging.INFO)


# seconds app
# app.mount("/", )

main_app: FastAPI = app

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app = 'run:main_app',
                host='127.0.0.1',
                port=8000,
                log_level='info',
                reload=True,)