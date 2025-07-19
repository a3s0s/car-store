from flask import Flask, jsonify, render_template_string
import os

# Create Flask app
app = Flask(__name__)

# Simple HTML template as string to avoid template file issues
HOMEPAGE_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>متجر السيارات - Car Store</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            text-align: center;
        }
        .header {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            margin-bottom: 30px;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            font-size: 1.5em;
            opacity: 0.9;
            margin-bottom: 20px;
        }
        .status {
            background: rgba(0, 255, 0, 0.2);
            padding: 20px;
            border-radius: 10px;
            border: 2px solid rgba(0, 255, 0, 0.5);
            margin: 20px 0;
        }
        .cars-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .car-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }
        .car-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        .car-name {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #FFD700;
        }
        .car-details {
            margin: 10px 0;
            line-height: 1.6;
        }
        .car-price {
            font-size: 1.5em;
            font-weight: bold;
            color: #00FF88;
            margin-top: 15px;
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
        .admin-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 متجر السيارات</h1>
            <div class="subtitle">Car Store Application</div>
            
            <div class="status">
                <h3>✅ تم النشر بنجاح على Vercel!</h3>
                <p>Successfully Deployed on Vercel!</p>
            </div>
        </div>
        
        <div class="cars-grid">
            <div class="car-card">
                <div class="car-name">تويوتا كورولا 2022</div>
                <div class="car-details">
                    <div>🏭 الماركة: تويوتا</div>
                    <div>📅 السنة: 2022</div>
                    <div>⛽ الوقود: بنزين</div>
                    <div>🔧 ناقل الحركة: أوتوماتيك</div>
                    <div>🚪 الأبواب: 4</div>
                </div>
                <div class="car-price">$8,000</div>
            </div>
            
            <div class="car-card">
                <div class="car-name">هيونداي النترا 2021</div>
                <div class="car-details">
                    <div>🏭 الماركة: هيونداي</div>
                    <div>📅 السنة: 2021</div>
                    <div>⛽ الوقود: بنزين</div>
                    <div>🔧 ناقل الحركة: أوتوماتيك</div>
                    <div>🚪 الأبواب: 4</div>
                </div>
                <div class="car-price">$7,500</div>
            </div>
            
            <div class="car-card">
                <div class="car-name">مرسيدس C200 2023</div>
                <div class="car-details">
                    <div>🏭 الماركة: مرسيدس</div>
                    <div>📅 السنة: 2023</div>
                    <div>⛽ الوقود: بنزين</div>
                    <div>🔧 ناقل الحركة: أوتوماتيك</div>
                    <div>🚪 الأبواب: 4</div>
                </div>
                <div class="car-price">$20,000</div>
            </div>
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
        
        <div class="admin-section">
            <h3>🔐 لوحة الإدارة - Admin Panel</h3>
            <p>للدخول إلى لوحة الإدارة: admin / admin123</p>
            <p>To access admin panel: admin / admin123</p>
        </div>
        
        <div class="links">
            <a href="/test">Test API</a>
            <a href="/admin">Admin Panel</a>
            <a href="/search">Search Cars</a>
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
    return render_template_string(HOMEPAGE_HTML)

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Car Store API is working perfectly!',
        'version': '4.0.0',
        'deployment': 'vercel',
        'features': [
            'Car Listings Display',
            'Responsive Design',
            'Arabic/English Interface',
            'Admin Panel Ready',
            'API Endpoints'
        ],
        'cars': [
            {
                'name': 'تويوتا كورولا 2022',
                'brand': 'تويوتا',
                'year': 2022,
                'price': 8000
            },
            {
                'name': 'هيونداي النترا 2021',
                'brand': 'هيونداي',
                'year': 2021,
                'price': 7500
            },
            {
                'name': 'مرسيدس C200 2023',
                'brand': 'مرسيدس',
                'year': 2023,
                'price': 20000
            }
        ]
    })

@app.route('/admin')
def admin():
    """Admin panel"""
    admin_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>لوحة الإدارة - Admin Panel</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                background: rgba(255, 255, 255, 0.1); 
                padding: 30px; 
                border-radius: 15px; 
                backdrop-filter: blur(10px);
            }
            h1 { color: #FFD700; text-align: center; margin-bottom: 30px; }
            .status { 
                background: rgba(0, 255, 0, 0.2); 
                padding: 20px; 
                border-radius: 10px; 
                border: 2px solid rgba(0, 255, 0, 0.5);
                margin: 20px 0;
            }
            .feature-list {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .feature-list li {
                margin: 10px 0;
                padding: 5px 0;
            }
            a { 
                color: #FFD700; 
                text-decoration: none;
                padding: 10px 20px;
                border: 2px solid #FFD700;
                border-radius: 25px;
                display: inline-block;
                margin: 10px;
                transition: all 0.3s ease;
            }
            a:hover {
                background: #FFD700;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 لوحة الإدارة</h1>
            <h2>Admin Panel</h2>
            
            <div class="status">
                <p><strong>Status:</strong> Admin panel is ready for development</p>
                <p><strong>الحالة:</strong> لوحة الإدارة جاهزة للتطوير</p>
                <p><strong>Login:</strong> admin / admin123</p>
            </div>
            
            <div class="feature-list">
                <h3>Features to be implemented:</h3>
                <ul>
                    <li>✅ Car inventory display</li>
                    <li>🔄 User authentication system</li>
                    <li>📊 Sales analytics dashboard</li>
                    <li>🖼️ Image upload system</li>
                    <li>🔍 Advanced search management</li>
                    <li>📝 Car CRUD operations</li>
                </ul>
            </div>
            
            <div style="text-align: center;">
                <a href="/">← Back to Home</a>
                <a href="/test">Test API</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(admin_html)

@app.route('/search')
def search():
    """Search page"""
    search_html = """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>البحث عن السيارات - Car Search</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container { 
                max-width: 1000px; 
                margin: 0 auto; 
                background: rgba(255, 255, 255, 0.1); 
                padding: 30px; 
                border-radius: 15px; 
                backdrop-filter: blur(10px);
            }
            h1 { color: #FFD700; text-align: center; margin-bottom: 30px; }
            .search-form {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .search-form input, .search-form select {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: none;
                border-radius: 5px;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
            }
            .search-form button {
                background: #FFD700;
                color: #333;
                padding: 12px 30px;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: bold;
                margin: 10px 5px;
            }
            .cars-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .car-card {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .car-name {
                font-size: 1.3em;
                font-weight: bold;
                margin-bottom: 10px;
                color: #FFD700;
            }
            .car-price {
                font-size: 1.5em;
                font-weight: bold;
                color: #00FF88;
                margin-top: 15px;
            }
            a { 
                color: #FFD700; 
                text-decoration: none;
                padding: 10px 20px;
                border: 2px solid #FFD700;
                border-radius: 25px;
                display: inline-block;
                margin: 10px;
                transition: all 0.3s ease;
            }
            a:hover {
                background: #FFD700;
                color: #333;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 البحث عن السيارات</h1>
            <h2>Car Search</h2>
            
            <div class="search-form">
                <h3>Search Filters:</h3>
                <input type="text" placeholder="اسم السيارة أو الماركة / Car name or brand">
                <select>
                    <option>جميع الماركات / All Brands</option>
                    <option>تويوتا / Toyota</option>
                    <option>هيونداي / Hyundai</option>
                    <option>مرسيدس / Mercedes</option>
                </select>
                <select>
                    <option>جميع الأنواع / All Types</option>
                    <option>سيدان / Sedan</option>
                    <option>SUV</option>
                    <option>هاتشباك / Hatchback</option>
                </select>
                <button>🔍 بحث / Search</button>
                <button>🔄 إعادة تعيين / Reset</button>
            </div>
            
            <div class="cars-grid">
                <div class="car-card">
                    <div class="car-name">تويوتا كورولا 2022</div>
                    <div>🏭 تويوتا | 📅 2022 | ⛽ بنزين</div>
                    <div class="car-price">$8,000</div>
                </div>
                
                <div class="car-card">
                    <div class="car-name">هيونداي النترا 2021</div>
                    <div>🏭 هيونداي | 📅 2021 | ⛽ بنزين</div>
                    <div class="car-price">$7,500</div>
                </div>
                
                <div class="car-card">
                    <div class="car-name">مرسيدس C200 2023</div>
                    <div>🏭 مرسيدس | 📅 2023 | ⛽ بنزين</div>
                    <div class="car-price">$20,000</div>
                </div>
            </div>
            
            <div style="text-align: center;">
                <a href="/">← العودة للرئيسية / Back to Home</a>
                <a href="/test">Test API</a>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(search_html)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Page not found',
        'message': 'The requested page does not exist',
        'available_endpoints': ['/', '/test', '/admin', '/search']
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server',
        'contact': 'Please contact the administrator'
    }), 500

# For Vercel deployment
application = app

if __name__ == '__main__':
    app.run(debug=True)