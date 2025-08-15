import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 在Vercel环境中可能没有python-dotenv
    pass


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here-vercel-deployment')

    # 数据库配置 - 优先使用环境变量中的DATABASE_URL
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        # 如果有DATABASE_URL环境变量，直接使用
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # 在serverless环境中使用内存数据库，避免只读文件系统错误
        # 注意：内存数据库在每次请求后会重置
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10
