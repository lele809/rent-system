import sys
import os
from flask import Flask

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 创建Flask应用
app = Flask(__name__)

# 基本配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vercel-deployment-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 基本路由用于测试
@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>租房系统</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>租房管理系统</h1>
    <p>系统正在初始化中...</p>
    <p>如果您看到此页面，说明部署成功！</p>
    <a href="/login">前往登录页面</a>
</body>
</html>'''

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Application is running'}

try:
    # 尝试导入完整的应用
    from app import app as full_app
    app = full_app
except Exception as e:
    print(f"Warning: Could not import full app: {e}")
    # 使用简化版本继续运行
    pass

# Vercel需要的handler函数
def handler(event, context):
    return app(event, context)

# 确保app变量可用
if __name__ == "__main__":
    app.run()
