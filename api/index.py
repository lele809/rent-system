import sys
import os
from flask import Flask

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 创建基础Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vercel-deployment-key')

# 尝试导入完整的应用功能
full_app_loaded = False
import_error = None

try:
    # 先尝试导入必要的模块
    import config
    from models import db
    
    # 配置应用
     app.config.from_object('config.Config')
     db.init_app(app)
     
     # 延迟导入路由，避免循环导入
     with app.app_context():
         try:
             # 初始化数据库表
             db.create_all()
             print("Database tables created successfully")
             
             # 导入所有路由
             import app as full_app_module
             # 复制路由到当前应用
             for rule in full_app_module.app.url_map.iter_rules():
                 if rule.endpoint != 'static':
                     app.add_url_rule(
                         rule.rule,
                         rule.endpoint,
                         full_app_module.app.view_functions[rule.endpoint],
                         methods=rule.methods
                     )
             full_app_loaded = True
             print("Successfully loaded full rental management system")
         except Exception as route_error:
             print(f"Failed to load routes: {route_error}")
             import_error = route_error
            
except Exception as e:
    print(f"Failed to import full app: {e}")
    import_error = e

# 如果完整应用加载失败，提供备用路由
if not full_app_loaded:
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
        <p>错误信息: {str(import_error)}</p>
        <p>请检查依赖和配置</p>
    </div>
</body>
</html>'''

@app.route('/health')
def health():
    if full_app_loaded:
        return {
            'status': 'success',
            'message': 'Full rental management system loaded successfully',
            'platform': 'Vercel Serverless'
        }
    else:
        return {
            'status': 'error',
            'message': f'Failed to load full app: {str(import_error)}',
            'platform': 'Vercel Serverless'
        }

# Vercel入口点
if __name__ == '__main__':
    app.run(debug=True)
