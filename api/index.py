import sys
import os
from flask import Flask

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 尝试导入完整的应用
try:
    from app import app
    print("Successfully imported full rental management system")
except Exception as e:
    print(f"Failed to import full app: {e}")
    # 创建备用Flask应用
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vercel-deployment-key')
    
    @app.route('/')
    def fallback_index():
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>租房系统 - 加载错误</title>
    <meta charset="utf-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .container {{ max-width: 600px; margin: 0 auto; text-align: center; }}
        .error {{ color: #dc3545; }}
        .info {{ color: #17a2b8; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="error">⚠️ 租房管理系统</h1>
        <p class="info">系统加载遇到问题</p>
        <p>错误信息: {str(e)}</p>
        <p>请检查依赖和配置</p>
    </div>
</body>
</html>'''
    
    @app.route('/health')
    def fallback_health():
        return {{
            'status': 'error',
            'message': f'Failed to load full app: {{str(e)}}',
            'platform': 'Vercel Serverless'
        }}

# Vercel入口点
if __name__ == '__main__':
    app.run(debug=True)
