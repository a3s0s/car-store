from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import db, Car, Admin, SearchLog
from database import init_database
from search_engine import search_engine
from utils import normalize_arabic, format_price, validate_search_criteria
from image_handler import ImageHandler
import json
from datetime import datetime

def create_app():
    """إنشاء تطبيق Flask"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # تهيئة قاعدة البيانات
    db.init_app(app)
    
    # تهيئة قاعدة البيانات عند بدء التطبيق (non-blocking)
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully")
            # Initialize database in background to avoid blocking startup
            try:
                init_database(app)
                print("Database initialized with sample data")
            except Exception as init_error:
                print(f"Database sample data initialization warning: {init_error}")
                # Continue without sample data - app will still work
        except Exception as e:
            print(f"Database creation error: {e}")
            # Try to continue anyway - some deployments create tables differently
    
    return app

app = create_app()

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    # الحصول على خيارات المرشحات
    filter_options = search_engine.get_filter_options()
    
    # الحصول على السيارات المميزة
    featured_cars = Car.query.filter(Car.is_available == True, Car.is_featured == True)\
                            .order_by(Car.created_at.desc())\
                            .limit(4).all()
    
    # الحصول على أحدث السيارات
    latest_cars = Car.query.filter(Car.is_available == True)\
                          .order_by(Car.created_at.desc())\
                          .limit(6).all()
    
    # الحصول على الإحصائيات الحقيقية
    total_cars = Car.query.filter(Car.is_available == True).count()
    total_brands = len(filter_options.get('brands', []))
    
    return render_template('index.html',
                         filter_options=filter_options,
                         featured_cars=featured_cars,
                         latest_cars=latest_cars,
                         total_cars=total_cars,
                         total_brands=total_brands)

@app.route('/search')
def search():
    """صفحة البحث والنتائج"""
    # الحصول على معايير البحث من الطلب
    criteria = {}
    
    # النص البحثي
    search_text = request.args.get('search_text') or request.args.get('q')
    if search_text:
        criteria['search_text'] = search_text.strip()
    
    # الميزانية
    if request.args.get('budget'):
        criteria['budget'] = request.args.get('budget')
    
    # نطاق السعر
    if request.args.get('price_min'):
        criteria['price_min'] = request.args.get('price_min')
    if request.args.get('price_max'):
        criteria['price_max'] = request.args.get('price_max')
    
    # المعايير الأساسية
    basic_criteria = ['performance_level', 'fuel_type', 'transmission', 'car_type', 'brand']
    for criterion in basic_criteria:
        if request.args.get(criterion):
            criteria[criterion] = request.args.get(criterion)
    
    # معايير السنة
    if request.args.get('year_from'):
        criteria['year_from'] = request.args.get('year_from')
    if request.args.get('year_to'):
        criteria['year_to'] = request.args.get('year_to')
    
    # معايير أخرى
    other_criteria = ['doors', 'engine_size_min', 'engine_size_max', 'mileage_max', 'color', 'country_origin']
    for criterion in other_criteria:
        if request.args.get(criterion):
            criteria[criterion] = request.args.get(criterion)
    
    # الميزات الإضافية
    features = ['leather_seats', 'sunroof', 'gps_system', 'backup_camera', 'entertainment_system', 'safety_features']
    for feature in features:
        if request.args.get(feature) == 'on':
            criteria[feature] = True
    
    # معايير التصفح والترتيب
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 12))
    sort_by = request.args.get('sort_by', 'price_asc')
    
    # تنفيذ البحث
    search_results = search_engine.search(criteria, page, per_page, sort_by)
    
    # تسجيل عملية البحث
    try:
        search_log = SearchLog(
            search_criteria=json.dumps(criteria, ensure_ascii=False),
            results_count=search_results['total'],
            user_ip=request.remote_addr
        )
        db.session.add(search_log)
        db.session.commit()
    except Exception as e:
        print(f"خطأ في تسجيل البحث: {e}")
    
    # الحصول على خيارات المرشحات
    filter_options = search_engine.get_filter_options()
    
    return render_template('search.html',
                         search_results=search_results,
                         filter_options=filter_options,
                         current_criteria=criteria,
                         current_sort=sort_by)

@app.route('/car/<int:car_id>')
def car_details(car_id):
    """صفحة تفاصيل السيارة"""
    car = Car.query.get_or_404(car_id)
    
    # الحصول على سيارات مشابهة
    similar_cars = search_engine.get_similar_cars(car_id)
    
    return render_template('car_details.html', 
                         car=car, 
                         similar_cars=similar_cars)

@app.route('/api/search_suggestions')
def search_suggestions():
    """API للحصول على اقتراحات البحث"""
    query = request.args.get('q', '').strip()
    suggestions = search_engine.get_search_suggestions(query)
    return jsonify(suggestions)

@app.route('/api/latest-cars')
def api_latest_cars():
    """API للحصول على أحدث السيارات مع التصفح"""
    page = int(request.args.get('page', 1))
    per_page = 6
    
    cars = Car.query.filter(Car.is_available == True)\
                   .order_by(Car.created_at.desc())\
                   .offset((page - 1) * per_page)\
                   .limit(per_page).all()
    
    cars_data = []
    for car in cars:
        cars_data.append({
            'id': car.id,
            'name': car.name,
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'price': car.price,
            'fuel_type': car.fuel_type,
            'transmission': car.transmission,
            'mileage': car.mileage,
            'image_url': car.image_url,
            'gps_system': car.gps_system,
            'backup_camera': car.backup_camera
        })
    
    return jsonify({
        'cars': cars_data,
        'page': page,
        'has_more': len(cars) == per_page
    })

@app.route('/compare')
def compare_cars():
    """صفحة مقارنة السيارات"""
    car_ids = request.args.getlist('cars')
    cars = []
    
    for car_id in car_ids:
        try:
            car = Car.query.get(int(car_id))
            if car:
                cars.append(car)
        except ValueError:
            continue
    
    if len(cars) < 2:
        flash('يجب اختيار سيارتين على الأقل للمقارنة', 'warning')
        return redirect(url_for('search'))
    
    return render_template('compare.html', cars=cars)

@app.route('/compare-list')
def compare_list():
    """صفحة إدارة قائمة المقارنة"""
    return render_template('compare_list.html')

# ===== لوحة الإدارة =====

@app.route('/admin')
def admin_login():
    """صفحة تسجيل دخول المدير"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login_post():
    """معالجة تسجيل دخول المدير"""
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

@app.route('/admin/logout')
def admin_logout():
    """تسجيل خروج المدير"""
    session.pop('admin_logged_in', None)
    session.pop('admin_id', None)
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """لوحة تحكم المدير"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    # إحصائيات عامة
    total_cars = Car.query.count()
    available_cars = Car.query.filter_by(is_available=True).count()
    total_searches = SearchLog.query.count()
    
    # أحدث السيارات المضافة
    recent_cars = Car.query.order_by(Car.created_at.desc()).limit(5).all()
    
    # أحدث عمليات البحث
    recent_searches = SearchLog.query.order_by(SearchLog.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_cars=total_cars,
                         available_cars=available_cars,
                         total_searches=total_searches,
                         recent_cars=recent_cars,
                         recent_searches=recent_searches)

@app.route('/admin/cars')
def admin_cars():
    """إدارة السيارات"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    page = int(request.args.get('page', 1))
    cars = Car.query.order_by(Car.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/cars.html', cars=cars)

@app.route('/admin/cars/add', methods=['GET', 'POST'])
def admin_add_car():
    """إضافة سيارة جديدة"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        try:
            # معالجة رفع الصورة
            image_url = None
            image_file = request.files.get('image_file')
            
            if image_file and image_file.filename:
                # رفع صورة جديدة
                image_path, errors = ImageHandler.process_and_save_image(image_file)
                if errors:
                    for error in errors:
                        flash(error, 'error')
                    filter_options = search_engine.get_filter_options()
                    return render_template('admin/add_car.html', filter_options=filter_options)
                image_url = image_path
            elif request.form.get('image_url'):
                # استخدام رابط الصورة
                image_url = request.form.get('image_url')
            
            car_data = {
                'name': request.form.get('name'),
                'brand': request.form.get('brand'),
                'model': request.form.get('model'),
                'year': int(request.form.get('year') or 0),
                'price': float(request.form.get('price') or 0),
                'performance_level': request.form.get('performance_level'),
                'fuel_type': request.form.get('fuel_type'),
                'transmission': request.form.get('transmission'),
                'engine_size': float(request.form.get('engine_size', 0)),
                'doors': int(request.form.get('doors', 4)),
                'car_type': request.form.get('car_type'),
                'color': request.form.get('color'),
                'mileage': int(request.form.get('mileage', 0)),
                'country_origin': request.form.get('country_origin'),
                'description': request.form.get('description'),
                'image_url': image_url,
                'leather_seats': 'leather_seats' in request.form,
                'sunroof': 'sunroof' in request.form,
                'gps_system': 'gps_system' in request.form,
                'backup_camera': 'backup_camera' in request.form,
                'entertainment_system': 'entertainment_system' in request.form,
                'safety_features': 'safety_features' in request.form,
                'is_available': 'is_available' in request.form,
                'is_featured': 'is_featured' in request.form
            }
            
            car = Car(**car_data)
            car.update_normalized_fields()
            db.session.add(car)
            db.session.commit()
            
            flash('تم إضافة السيارة بنجاح', 'success')
            return redirect(url_for('admin_cars'))
            
        except Exception as e:
            flash(f'خطأ في إضافة السيارة: {str(e)}', 'error')
    
    filter_options = search_engine.get_filter_options()
    return render_template('admin/add_car.html', filter_options=filter_options)

@app.route('/admin/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def admin_edit_car(car_id):
    """تعديل سيارة"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    car = Car.query.get_or_404(car_id)
    
    if request.method == 'POST':
        try:
            # معالجة رفع الصورة
            image_file = request.files.get('image_file')
            
            if image_file and image_file.filename:
                # رفع صورة جديدة
                image_path, errors = ImageHandler.process_and_save_image(image_file)
                if errors:
                    for error in errors:
                        flash(error, 'error')
                    filter_options = search_engine.get_filter_options()
                    return render_template('admin/edit_car.html', car=car, filter_options=filter_options)
                
                # حذف الصورة القديمة إذا كانت موجودة
                if car.image_url:
                    ImageHandler.delete_image(car.image_url)
                
                car.image_url = image_path
            elif request.form.get('image_url') and request.form.get('image_url') != car.image_url:
                # تحديث رابط الصورة
                car.image_url = request.form.get('image_url')
            
            car.name = request.form.get('name')
            car.brand = request.form.get('brand')
            car.model = request.form.get('model')
            car.year = int(request.form.get('year') or 0)
            car.price = float(request.form.get('price') or 0)
            car.performance_level = request.form.get('performance_level')
            car.fuel_type = request.form.get('fuel_type')
            car.transmission = request.form.get('transmission')
            car.engine_size = float(request.form.get('engine_size', 0))
            car.doors = int(request.form.get('doors', 4))
            car.car_type = request.form.get('car_type')
            car.color = request.form.get('color')
            car.mileage = int(request.form.get('mileage', 0))
            car.country_origin = request.form.get('country_origin')
            car.description = request.form.get('description')
            car.leather_seats = 'leather_seats' in request.form
            car.sunroof = 'sunroof' in request.form
            car.gps_system = 'gps_system' in request.form
            car.backup_camera = 'backup_camera' in request.form
            car.entertainment_system = 'entertainment_system' in request.form
            car.safety_features = 'safety_features' in request.form
            car.is_available = 'is_available' in request.form
            car.is_featured = 'is_featured' in request.form
            
            car.update_normalized_fields()
            car.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('تم تحديث السيارة بنجاح', 'success')
            return redirect(url_for('admin_cars'))
            
        except Exception as e:
            flash(f'خطأ في تحديث السيارة: {str(e)}', 'error')
    
    filter_options = search_engine.get_filter_options()
    return render_template('admin/edit_car.html', car=car, filter_options=filter_options)

@app.route('/admin/cars/delete/<int:car_id>', methods=['POST'])
def admin_delete_car(car_id):
    """حذف سيارة"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    car = Car.query.get_or_404(car_id)
    
    try:
        # حذف صورة السيارة إذا كانت موجودة
        if car.image_url:
            ImageHandler.delete_image(car.image_url)
        
        db.session.delete(car)
        db.session.commit()
        flash('تم حذف السيارة بنجاح', 'success')
    except Exception as e:
        flash(f'خطأ في حذف السيارة: {str(e)}', 'error')
    
    return redirect(url_for('admin_cars'))

# ===== مرشحات القوالب =====

@app.template_filter('format_price')
def format_price_filter(price):
    """مرشح تنسيق السعر"""
    return format_price(price)

@app.template_filter('normalize_arabic')
def normalize_arabic_filter(text):
    """مرشح تطبيع النص العربي"""
    return normalize_arabic(text)

@app.template_filter('number_format')
def number_format_filter(number):
    """مرشح تنسيق الأرقام"""
    if number is None:
        return "0"
    return "{:,}".format(int(number))

@app.template_filter('from_json')
def from_json_filter(json_str):
    """مرشح تحويل JSON إلى كائن Python"""
    try:
        return json.loads(json_str) if json_str else {}
    except (json.JSONDecodeError, TypeError):
        return {}

# ===== معالجة الأخطاء =====

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

@app.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    try:
        # Simple health check that doesn't depend on database
        return jsonify({
            'status': 'healthy',
            'message': 'Car Store Application is running',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Health check failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/health/db')
def health_check_db():
    """Database health check endpoint"""
    try:
        # Test database connection
        from sqlalchemy import text
        db.session.execute(text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'message': 'Database connection is working',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Database health check failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/reset-db')
def reset_database_endpoint():
    """Reset database endpoint for fixing image paths"""
    try:
        from database import reset_database
        reset_database(app)
        return jsonify({
            'status': 'success',
            'message': 'Database reset successfully with correct image paths',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database reset failed: {str(e)}',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

# For Vercel deployment
application = app

# Make sure app is available at module level for gunicorn
app = app

if __name__ == '__main__':
    import os
    # Get port from environment, with fallback
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting application on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)