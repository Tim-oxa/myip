import os

DB_URL = os.getenv("DB_URL") or ""
DB_NAME = os.getenv("DB_NAME") or "myip"
PORT = os.getenv("PORT") or 8080
