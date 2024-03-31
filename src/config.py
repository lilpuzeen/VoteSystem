from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.environ.get("DATABASE_URL")
DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

SECRET_AUTH = os.environ.get("JWT_SECRET")
