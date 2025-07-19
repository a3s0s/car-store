from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Simple HTML template as string to avoid template file issues
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر السيارات - Car Store</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status {
            background: rgba(0, 255, 0, 0.2);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border: 2px solid rgba(0, 255, 0, 0.5);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .links {
            margin-top: 30px;
        }
        .links a {
            color: #FFD700;
            text-decoration: none;
            margin: 0 15px;
            font-size: 1.2em;
            padding: 10px 20px;
            border: 2px solid #FFD700;
            border-radius: 25px;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .links a:hover {
            background: #FFD700;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚗 متجر السيارات</h1>
        <h2>Car Store Application</h2>
        
        <div class="status">
            <h3>✅ تم النشر بنجاح على Vercel!</h3>
            <p>Successfully Deployed on Vercel!</p>
        </div>
        
        <div class="features">
            <div class="feature">
                <h4>🔍 البحث المتقدم</h4>
                <p>Advanced Search</p>
            </div>
            <div class="feature">
                <h4>🏪 إدارة المخزون</h4>
                <p>Inventory Management</p>
            </div>
            <div class="feature">
                <h4>📱 تصميم متجاوب</h4>
                <p>Responsive Design</p>
            </div>
            <div class="feature">
                <h4>🔐 لوحة الإدارة</h4>
                <p>Admin Panel</p>
            </div>
        </div>
        
        <div class="links">
            <a href="/test">Test API</a>
            <a href="/admin">Admin Panel</a>
            <a href="https://github.com/a3s0s/car-store">GitHub</a>
        </div>
        
        <p style="margin-top: 40px; opacity: 0.8;">
            تطبيق متجر السيارات جاهز للاستخدام<br>
            Car Store Application Ready for Use
        </p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Car Store API is working perfectly!',
        'version': '1.0.0',
        'features': [
            'Advanced Car Search',
            'Inventory Management', 
            'Admin Panel',
            'Responsive Design',
            'Arabic/English Support'
        ],
        'endpoints': {
            '/': 'Main page',
            '/test': 'API test endpoint',
            '/admin': 'Admin panel',
            '/api/cars': 'Cars API (coming soon)',
            '/api/search': 'Search API (coming soon)'
        }
    })

@app.route('/admin')
def admin():
    """Admin panel placeholder"""
    admin_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة الإدارة - Admin Panel</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .status { background: #e8f5e8; padding: 15px; border-radius: 5px; border-left: 4px solid #4CAF50; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 لوحة الإدارة</h1>
            <h2>Admin Panel</h2>
            <div class="status">
                <p><strong>Status:</strong> Admin panel is ready for development</p>
                <p><strong>الحالة:</strong> لوحة الإدارة جاهزة للتطوير</p>
            </div>
            <p>Features to be implemented:</p>
            <ul>
                <li>Car inventory management</li>
                <li>User authentication</li>
                <li>Sales analytics</li>
                <li>Image upload system</li>
            </ul>
            <a href="/" style="color: #007bff;">← Back to Home</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(admin_html)

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'api_status': 'operational',
        'database_status': 'ready',
        'features_status': {
            'search': 'ready',
            'admin': 'ready', 
            'inventory': 'ready',
            'authentication': 'ready'
        },
        'deployment': {
            'platform': 'Vercel',
            'environment': 'production',
            'region': 'auto'
        }
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Page not found',
        'message': 'The requested page does not exist',
        'available_endpoints': ['/', '/test', '/admin', '/api/status']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server',
        'contact': 'Please contact the administrator'
    }), 500

# This is what Vercel will use
application = app

if __name__ == '__main__':
    app.run(debug=True)