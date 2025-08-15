from flask import Flask
import os

# 创建Flask应用
app = Flask(__name__)

# 基本配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vercel-deployment-key')

# 基本路由
@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>租房系统</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; text-align: center; }
        .success { color: #28a745; }
        .btn { background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">🏠 租房管理系统</h1>
        <p>✅ Vercel部署成功！</p>
        <p>系统正在运行中...</p>
        <br>
        <a href="/health" class="btn">检查系统状态</a>
    </div>
</body>
</html>'''

@app.route('/health')
def health():
    return {
        'status': 'success',
        'message': 'Rental Management System is running on Vercel',
        'platform': 'Vercel Serverless'
    }

@app.route('/api/test')
def test():
    return {'test': 'ok', 'deployment': 'vercel'}

# Vercel入口点
if __name__ == '__main__':
    app.run(debug=True)
