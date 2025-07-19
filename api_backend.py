from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import check_password_hash, generate_password_hash
from config import Config
from models import db, Car, Admin, SearchLog
from database import init_database
from search_engine import search_engine
from utils import normalize_arabic, format_price
from image_handler import ImageHandler
import json
from datetime import datetime
import os

def create_api_app():
    """إنشاء تطبيق Flask API للخلفية"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app, origins=['*'])
    
    # تهيئة قاعدة البيانات
    db.init_app(app)
    
    # تهيئة قاعدة البيانات عند بدء التطبيق
    with app.app_context():
        try:
            db.create_all()
            init_database(app)
            print("Database tables created successfully")
            print("Database initialized with sample data")
        except Exception as e:
            print(f"Database initialization error: {e}")
            db.create_all()
    
    return app

app = create_api_app()

# ===== API Routes =====

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Car Store API is running',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/cars')
def get_cars():
    """Get all available cars"""
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        
        cars = Car.query.filter(Car.is_available == True)\
                       .order_by(Car.created_at.desc())\
                       .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'cars': [{
                'id': car.id,
                'name': car.name,
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'price': car.price,
                'performance_level': car.performance_level,
                'fuel_type': car.fuel_type,
                'transmission': car.transmission,
                'engine_size': car.engine_size,
                'doors': car.doors,
                'car_type': car.car_type,
                'color': car.color,
                'mileage': car.mileage,
                'country_origin': car.country_origin,
                'description': car.description,
                'image_url': car.image_url,
                'leather_seats': car.leather_seats,
                'sunroof': car.sunroof,
                'gps_system': car.gps_system,
                'backup_camera': car.backup_camera,
                'entertainment_system': car.entertainment_system,
                'safety_features': car.safety_features,
                'created_at': car.created_at.isoformat() if car.created_at else None
            } for car in cars.items],
            'total': cars.total,
            'page': page,
            'pages': cars.pages,
            'has_prev': cars.has_prev,
            'has_next': cars.has_next
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cars/<int:car_id>')
def get_car(car_id):
    """Get specific car details"""
    try:
        car = Car.query.get_or_404(car_id)
        
        # Get similar cars
        similar_cars = Car.query.filter(
            Car.id != car_id,
            Car.is_available == True,
            Car.brand == car.brand
        ).limit(3).all()
        
        return jsonify({
            'car': {
                'id': car.id,
                'name': car.name,
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'price': car.price,
                'performance_level': car.performance_level,
                'fuel_type': car.fuel_type,
                'transmission': car.transmission,
                'engine_size': car.engine_size,
                'doors': car.doors,
                'car_type': car.car_type,
                'color': car.color,
                'mileage': car.mileage,
                'country_origin': car.country_origin,
                'description': car.description,
                'image_url': car.image_url,
                'leather_seats': car.leather_seats,
                'sunroof': car.sunroof,
                'gps_system': car.gps_system,
                'backup_camera': car.backup_camera,
                'entertainment_system': car.entertainment_system,
                'safety_features': car.safety_features,
                'created_at': car.created_at.isoformat() if car.created_at else None
            },
            'similar_cars': [{
                'id': similar.id,
                'name': similar.name,
                'brand': similar.brand,
                'model': similar.model,
                'year': similar.year,
                'price': similar.price,
                'image_url': similar.image_url
            } for similar in similar_cars]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search_cars():
    """Search cars with filters"""
    try:
        # Get search criteria
        criteria = {}
        
        search_text = request.args.get('search_text') or request.args.get('q')
        if search_text:
            criteria['search_text'] = search_text.strip()
        
        # Basic filters
        basic_criteria = ['performance_level', 'fuel_type', 'transmission', 'car_type', 'brand']
        for criterion in basic_criteria:
            if request.args.get(criterion):
                criteria[criterion] = request.args.get(criterion)
        
        # Price range
        if request.args.get('price_min'):
            criteria['price_min'] = request.args.get('price_min')
        if request.args.get('price_max'):
            criteria['price_max'] = request.args.get('price_max')
        
        # Year range
        if request.args.get('year_from'):
            criteria['year_from'] = request.args.get('year_from')
        if request.args.get('year_to'):
            criteria['year_to'] = request.args.get('year_to')
        
        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 12))
        sort_by = request.args.get('sort_by', 'price_asc')
        
        # Execute search
        search_results = search_engine.search(criteria, page, per_page, sort_by)
        
        # Log search
        try:
            search_log = SearchLog(
                search_criteria=json.dumps(criteria, ensure_ascii=False),
                results_count=search_results['total'],
                user_ip=request.remote_addr
            )
            db.session.add(search_log)
            db.session.commit()
        except Exception as e:
            print(f"Search logging error: {e}")
        
        return jsonify(search_results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filters')
def get_filters():
    """Get available filter options"""
    try:
        filter_options = search_engine.get_filter_options()
        return jsonify(filter_options)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        admin = Admin.query.filter_by(username=username, is_active=True).first()
        
        if admin and password and check_password_hash(admin.password_hash, password):
            admin.last_login = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'admin': {
                    'id': admin.id,
                    'username': admin.username
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/cars', methods=['GET'])
def admin_get_cars():
    """Get all cars for admin"""
    try:
        page = int(request.args.get('page', 1))
        cars = Car.query.order_by(Car.created_at.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
        
        return jsonify({
            'cars': [{
                'id': car.id,
                'name': car.name,
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'price': car.price,
                'is_available': car.is_available,
                'image_url': car.image_url,
                'created_at': car.created_at.isoformat() if car.created_at else None
            } for car in cars.items],
            'total': cars.total,
            'page': page,
            'pages': cars.pages,
            'has_prev': cars.has_prev,
            'has_next': cars.has_next
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admin/stats')
def admin_stats():
    """Get admin dashboard statistics"""
    try:
        total_cars = Car.query.count()
        available_cars = Car.query.filter_by(is_available=True).count()
        total_searches = SearchLog.query.count()
        
        recent_cars = Car.query.order_by(Car.created_at.desc()).limit(5).all()
        
        return jsonify({
            'total_cars': total_cars,
            'available_cars': available_cars,
            'total_searches': total_searches,
            'recent_cars': [{
                'id': car.id,
                'name': car.name,
                'brand': car.brand,
                'price': car.price,
                'created_at': car.created_at.isoformat() if car.created_at else None
            } for car in recent_cars]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Make sure app is available at module level for gunicorn
app = app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Car Store API on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)