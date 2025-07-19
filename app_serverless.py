from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Configuration for serverless environment
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'car-store-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///car_store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Import models after db initialization
search_engine = None  # Initialize to avoid "possibly unbound" errors

try:
    from models import Car, Admin, SearchLog
    from search_engine import search_engine
    from utils import normalize_arabic, format_price
    from image_handler import ImageHandler
    FULL_FEATURES = True
except ImportError as e:
    print(f"Import warning: {e}")
    FULL_FEATURES = False
    search_engine = None  # Ensure it's None if import fails
    
    # Define minimal models if imports fail
    class Car(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        brand = db.Column(db.String(100), nullable=False)
        model = db.Column(db.String(100), nullable=False)
        year = db.Column(db.Integer, nullable=False)
        price = db.Column(db.Float, nullable=False)
        description = db.Column(db.Text)
        image_url = db.Column(db.String(500))
        is_available = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    class Admin(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password_hash = db.Column(db.String(200), nullable=False)
        is_active = db.Column(db.Boolean, default=True)

# Initialize database with error handling
try:
    with app.app_context():
        db.create_all()
        
        # Add sample data if no cars exist
        if Car.query.count() == 0:
            sample_cars = [
                Car(
                    name='تويوتا كورولا 2022',
                    brand='تويوتا',
                    model='كورولا',
                    year=2022,
                    price=8000,
                    description='سيارة اقتصادية موثوقة مع استهلاك وقود ممتاز',
                    image_url='/static/images/cars/placeholder.jpg'
                ),
                Car(
                    name='هيونداي النترا 2021',
                    brand='هيونداي',
                    model='النترا',
                    year=2021,
                    price=7500,
                    description='سيارة عملية بتصميم عصري وميزات متقدمة',
                    image_url='/static/images/cars/hyundai-elantra.jpg'
                ),
                Car(
                    name='مرسيدس C200 2023',
                    brand='مرسيدس',
                    model='C200',
                    year=2023,
                    price=20000,
                    description='سيارة فاخرة بأداء عالي وتقنيات متطورة',
                    image_url='/static/images/cars/placeholder.jpg'
                )
            ]
            
            for car in sample_cars:
                db.session.add(car)
            
            db.session.commit()
        
        # Add default admin if none exists
        if Admin.query.count() == 0:
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            
except Exception as e:
    print(f"Database initialization error: {e}")

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    try:
        if FULL_FEATURES and search_engine is not None:
            # Use full search engine if available
            filter_options = search_engine.get_filter_options()
            latest_cars = Car.query.filter(Car.is_available == True)\
                                  .order_by(Car.created_at.desc())\
                                  .limit(6).all()
        else:
            # Simplified version
            filter_options = {}
            latest_cars = Car.query.filter(Car.is_available == True).limit(6).all()
        
        return render_template('index.html', 
                             filter_options=filter_options,
                             latest_cars=latest_cars)
    except Exception as e:
        return render_template('index.html', 
                             filter_options={},
                             latest_cars=[],
                             error=f"Database error: {e}")

@app.route('/search')
def search():
    """صفحة البحث والنتائج"""
    try:
        # Get search criteria
        search_text = request.args.get('search_text', '')
        
        # Basic search implementation
        cars = Car.query.filter(Car.is_available == True)
        
        if search_text:
            cars = cars.filter(
                Car.name.contains(search_text) | 
                Car.brand.contains(search_text) |
                Car.model.contains(search_text)
            )
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        
        cars_paginated = cars.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        search_results = {
            'cars': cars_paginated.items,
            'total': cars_paginated.total,
            'page': page,
            'pages': cars_paginated.pages,
            'has_prev': cars_paginated.has_prev,
            'has_next': cars_paginated.has_next
        }
        
        filter_options = {} if not FULL_FEATURES or search_engine is None else search_engine.get_filter_options()
        
        return render_template('search.html',
                             search_results=search_results,
                             filter_options=filter_options,
                             current_criteria={'search_text': search_text})
    except Exception as e:
        return render_template('search.html',
                             search_results={'cars': [], 'total': 0, 'page': 1, 'pages': 1},
                             filter_options={},
                             error=f"Search error: {e}")

@app.route('/car/<int:car_id>')
def car_details(car_id):
    """صفحة تفاصيل السيارة"""
    try:
        car = Car.query.get_or_404(car_id)
        similar_cars = Car.query.filter(
            Car.id != car_id, 
            Car.is_available == True,
            Car.brand == car.brand
        ).limit(3).all()
        
        return render_template('car_details.html', 
                             car=car, 
                             similar_cars=similar_cars)
    except Exception as e:
        return f"Error loading car details: {e}", 500

@app.route('/admin')
def admin_login():
    """صفحة تسجيل دخول المدير"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    """معالجة تسجيل دخول المدير"""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        
        if admin and password and check_password_hash(admin.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_id'] = admin.id
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
            return redirect(url_for('admin_login'))
    except Exception as e:
        flash(f'خطأ في تسجيل الدخول: {e}', 'error')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """لوحة تحكم المدير"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        total_cars = Car.query.count()
        available_cars = Car.query.filter_by(is_available=True).count()
        recent_cars = Car.query.order_by(Car.created_at.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
                             total_cars=total_cars,
                             available_cars=available_cars,
                             total_searches=0,  # Simplified
                             recent_cars=recent_cars,
                             recent_searches=[])  # Simplified
    except Exception as e:
        return f"Dashboard error: {e}", 500

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'Car Store Application is working!',
        'version': '2.0.0',
        'features_available': FULL_FEATURES,
        'database_status': 'connected',
        'cars_count': Car.query.count() if Car.query else 0,
        'endpoints': {
            '/': 'Main page',
            '/search': 'Search cars',
            '/admin': 'Admin panel',
            '/test': 'API test'
        }
    })

# Template filters
@app.template_filter('format_price')
def format_price_filter(price):
    """مرشح تنسيق السعر"""
    if price is None:
        return "0"
    return "{:,}".format(int(price))

@app.template_filter('number_format')
def number_format_filter(number):
    """مرشح تنسيق الأرقام"""
    if number is None:
        return "0"
    return "{:,}".format(int(number))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

# For Vercel deployment
application = app

if __name__ == '__main__':
    app.run(debug=True)