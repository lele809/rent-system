import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash

# 创建Flask应用
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'vercel-deployment-key')

# 基础路由
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 简单的演示登录逻辑
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health():
    return {
        'status': 'success',
        'message': 'Rental Management System is running',
        'platform': 'Vercel Serverless',
        'database': 'Demo mode - no persistent storage'
    }

@app.route('/api/test')
def api_test():
    return {
        'test': 'ok',
        'deployment': 'vercel',
        'timestamp': '2024-08-15'
    }

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return render_template('login.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Please check the application logs'
    }), 500

# Vercel入口点
if __name__ == '__main__':
    app.run(debug=True)
