import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # 数据库配置 - 优先使用环境变量中的DATABASE_URL
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # 如果有DATABASE_URL环境变量，直接使用
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # 否则使用SQLite作为备用数据库
        SQLALCHEMY_DATABASE_URI = 'sqlite:///rental_system.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10
