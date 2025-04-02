from dotenv import load_dotenv
import os

# load_dotenv('.env')
load_dotenv('.env_dev')

PG_DB_SERVER = os.environ.get('PG_DB_SERVER')
PG_DB_NAME = os.environ.get('PG_DB_NAME')
PG_DB_USER = os.environ.get('PG_DB_USER')
PG_DB_PASS = os.environ.get('PG_DB_PASS')


MSSQL_DB_SERVER = os.environ.get('MSSQL_DB_SERVER')
MSSQL_DB_NAME = os.environ.get('MSSQL_DB_NAME')
MSSQL_DB_USER = os.environ.get('MSSQL_DB_USER')
MSSQL_DB_PASS = os.environ.get('MSSQL_DB_PASS')