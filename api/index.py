from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'car-store-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///car_store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define models directly here to avoid import issues
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    performance_level = db.Column(db.String(50))
    fuel_type = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    engine_size = db.Column(db.Float)
    doors = db.Column(db.Integer)
    car_type = db.Column(db.String(50))
    color = db.Column(db.String(50))
    mileage = db.Column(db.Integer)
    country_origin = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Features
    leather_seats = db.Column(db.Boolean, default=False)
    sunroof = db.Column(db.Boolean, default=False)
    gps_system = db.Column(db.Boolean, default=False)
    backup_camera = db.Column(db.Boolean, default=False)
    entertainment_system = db.Column(db.Boolean, default=False)
    safety_features = db.Column(db.Boolean, default=False)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)

# Initialize database
try:
    with app.app_context():
        db.create_all()
        
        # Add sample cars if none exist
        if Car.query.count() == 0:
            sample_cars = [
                Car(
                    name='تويوتا كورولا 2022',
                    brand='تويوتا',
                    model='كورولا',
                    year=2022,
                    price=8000,
                    performance_level='medium',
                    fuel_type='gasoline',
                    transmission='automatic',
                    engine_size=1.8,
                    doors=4,
                    car_type='sedan',
                    color='أبيض',
                    mileage=25000,
                    country_origin='اليابان',
                    description='سيارة اقتصادية موثوقة مع استهلاك وقود ممتاز',
                    image_url='/static/images/cars/placeholder.jpg',
                    leather_seats=False,
                    sunroof=False,
                    gps_system=True,
                    backup_camera=True,
                    entertainment_system=True,
                    safety_features=True
                ),
                Car(
                    name='هيونداي النترا 2021',
                    brand='هيونداي',
                    model='النترا',
                    year=2021,
                    price=7500,
                    performance_level='medium',
                    fuel_type='gasoline',
                    transmission='automatic',
                    engine_size=2.0,
                    doors=4,
                    car_type='sedan',
                    color='فضي',
                    mileage=30000,
                    country_origin='كوريا الجنوبية',
                    description='سيارة عملية بتصميم عصري وميزات متقدمة',
                    image_url='/static/images/cars/hyundai-elantra.jpg',
                    leather_seats=True,
                    sunroof=True,
                    gps_system=True,
                    backup_camera=True,
                    entertainment_system=True,
                    safety_features=True
                ),
                Car(
                    name='مرسيدس C200 2023',
                    brand='مرسيدس',
                    model='C200',
                    year=2023,
                    price=20000,
                    performance_level='high',
                    fuel_type='gasoline',
                    transmission='automatic',
                    engine_size=2.0,
                    doors=4,
                    car_type='sedan',
                    color='أسود',
                    mileage=15000,
                    country_origin='ألمانيا',
                    description='سيارة فاخرة بأداء عالي وتقنيات متطورة',
                    image_url='/static/images/cars/placeholder.jpg',
                    leather_seats=True,
                    sunroof=True,
                    gps_system=True,
                    backup_camera=True,
                    entertainment_system=True,
                    safety_features=True
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
        latest_cars = Car.query.filter(Car.is_available == True)\
                              .order_by(Car.created_at.desc())\
                              .limit(6).all()
        
        # Simple filter options
        filter_options = {
            'brands': db.session.query(Car.brand).distinct().all(),
            'car_types': db.session.query(Car.car_type).distinct().all(),
            'fuel_types': db.session.query(Car.fuel_type).distinct().all()
        }
        
        return render_template('index.html', 
                             filter_options=filter_options,
                             latest_cars=latest_cars)
    except Exception as e:
        return f"Error loading homepage: {e}", 500

@app.route('/search')
def search():
    """صفحة البحث والنتائج"""
    try:
        search_text = request.args.get('search_text', '')
        brand = request.args.get('brand', '')
        car_type = request.args.get('car_type', '')
        
        # Build query
        cars = Car.query.filter(Car.is_available == True)
        
        if search_text:
            cars = cars.filter(
                Car.name.contains(search_text) | 
                Car.brand.contains(search_text) |
                Car.model.contains(search_text)
            )
        
        if brand:
            cars = cars.filter(Car.brand == brand)
            
        if car_type:
            cars = cars.filter(Car.car_type == car_type)
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = 12
        
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
        
        filter_options = {
            'brands': db.session.query(Car.brand).distinct().all(),
            'car_types': db.session.query(Car.car_type).distinct().all()
        }
        
        return render_template('search.html',
                             search_results=search_results,
                             filter_options=filter_options,
                             current_criteria={
                                 'search_text': search_text,
                                 'brand': brand,
                                 'car_type': car_type
                             })
    except Exception as e:
        return f"Search error: {e}", 500

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
            admin.last_login = datetime.utcnow()
            db.session.commit()
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
                             total_searches=0,
                             recent_cars=recent_cars,
                             recent_searches=[])
    except Exception as e:
        return f"Dashboard error: {e}", 500

@app.route('/test')
def test():
    """Test endpoint"""
    try:
        car_count = Car.query.count()
        admin_count = Admin.query.count()
        
        return jsonify({
            'status': 'success',
            'message': 'Car Store Application is working perfectly!',
            'version': '3.0.0',
            'database': {
                'cars': car_count,
                'admins': admin_count,
                'status': 'connected'
            },
            'features': [
                'Car Listings',
                'Search & Filter',
                'Car Details',
                'Admin Panel',
                'Database Integration'
            ]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Test failed: {str(e)}'
        }), 500

# Template filters
@app.template_filter('format_price')
def format_price_filter(price):
    if price is None:
        return "0"
    return "{:,}".format(int(price))

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