from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json
from datetime import datetime

# Simple Flask app for Vercel
app = Flask(__name__)

# Basic configuration for Vercel
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'car-store-secret-key-2024')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///car_store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Simple Car model for demonstration
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

# Simple Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    try:
        # Try to get cars from database
        latest_cars = Car.query.filter(Car.is_available == True).limit(6).all()
    except Exception as e:
        # If database fails, show empty list
        latest_cars = []
        print(f"Database error: {e}")
    
    return render_template('index.html', latest_cars=latest_cars)

@app.route('/search')
def search():
    """صفحة البحث والنتائج"""
    try:
        # Simple search implementation
        search_text = request.args.get('search_text', '')
        cars = Car.query.filter(Car.is_available == True)
        
        if search_text:
            cars = cars.filter(Car.name.contains(search_text) | Car.brand.contains(search_text))
        
        cars = cars.all()
        
        search_results = {
            'cars': cars,
            'total': len(cars),
            'page': 1,
            'pages': 1
        }
    except Exception as e:
        search_results = {'cars': [], 'total': 0, 'page': 1, 'pages': 1}
        print(f"Search error: {e}")
    
    return render_template('search.html', search_results=search_results)

@app.route('/car/<int:car_id>')
def car_details(car_id):
    """صفحة تفاصيل السيارة"""
    try:
        car = Car.query.get_or_404(car_id)
        similar_cars = Car.query.filter(Car.id != car_id, Car.is_available == True).limit(3).all()
    except Exception as e:
        return f"Error loading car details: {e}", 500
    
    return render_template('car_details.html', car=car, similar_cars=similar_cars)

@app.route('/admin')
def admin_login():
    """صفحة تسجيل دخول المدير"""
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    """لوحة تحكم المدير"""
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    try:
        total_cars = Car.query.count()
        available_cars = Car.query.filter_by(is_available=True).count()
        recent_cars = Car.query.order_by(Car.created_at.desc()).limit(5).all()
    except Exception as e:
        total_cars = 0
        available_cars = 0
        recent_cars = []
        print(f"Dashboard error: {e}")
    
    return render_template('admin/dashboard.html',
                         total_cars=total_cars,
                         available_cars=available_cars,
                         recent_cars=recent_cars)

@app.route('/test')
def test():
    """Test route to check if the app is working"""
    return jsonify({
        'status': 'success',
        'message': 'Car Store API is working!',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database tables (only if not in serverless environment)
try:
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            
        # Add sample car if no cars exist
        if Car.query.count() == 0:
            sample_car = Car(
                name='تويوتا كامري 2023',
                brand='تويوتا',
                model='كامري',
                year=2023,
                price=85000,
                description='سيارة عائلية ممتازة بحالة جيدة جداً',
                image_url='/static/images/cars/placeholder.jpg'
            )
            db.session.add(sample_car)
            db.session.commit()
            
except Exception as e:
    print(f"Database initialization error: {e}")

# For Vercel deployment
application = app

if __name__ == '__main__':
    app.run(debug=True)