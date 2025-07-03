import os
from dotenv import load_dotenv
# config/config.py

load_dotenv()

class Config:
    user_banco = os.getenv("USER_DB")
    password = os.getenv("PASSWORD_DB")
    ip_banco = os.getenv("IP_BANCO")
    API_TOKEN = os.getenv('API_TOKEN')
    BASE_URL = os.getenv('BASE_URL')
    USER = os.getenv('USER')
    SENHA = os.getenv('SENHA')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{user_banco}:{password}@{ip_banco}/moodle_icev?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False