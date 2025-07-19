from flask import Flask
from models import db, Car, Admin, SearchLog
from werkzeug.security import generate_password_hash
import json

def init_database(app: Flask):
    """تهيئة قاعدة البيانات"""
    with app.app_context():
        # إنشاء الجداول
        db.create_all()
        
        # إضافة بيانات تجريبية إذا لم تكن موجودة
        if Car.query.count() == 0:
            add_sample_cars()
        
        # إضافة مدير افتراضي إذا لم يكن موجوداً
        if Admin.query.count() == 0:
            add_default_admin()

def add_sample_cars():
    """إضافة سيارات تجريبية"""
    sample_cars = [
        {
            'name': 'تويوتا كورولا 2022',
            'brand': 'تويوتا',
            'model': 'كورولا',
            'year': 2022,
            'price': 8000,
            'performance_level': 'medium',
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'engine_size': 1.8,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'أبيض',
            'mileage': 25000,
            'country_origin': 'اليابان',
            'leather_seats': False,
            'sunroof': False,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة اقتصادية موثوقة مع استهلاك وقود ممتاز',
            'image_url': '/static/images/cars/toyota-corolla.jpg',
            'is_available': True
        },
        {
            'name': 'هيونداي النترا 2021',
            'brand': 'هيونداي',
            'model': 'النترا',
            'year': 2021,
            'price': 7500,
            'performance_level': 'medium',
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'engine_size': 2.0,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'فضي',
            'mileage': 30000,
            'country_origin': 'كوريا الجنوبية',
            'leather_seats': True,
            'sunroof': True,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة عملية بتصميم عصري وميزات متقدمة',
            'image_url': '/static/images/cars/hyundai-elantra.jpg',
            'is_available': True
        },
        {
            'name': 'مرسيدس C200 2023',
            'brand': 'مرسيدس',
            'model': 'C200',
            'year': 2023,
            'price': 20000,
            'performance_level': 'high',
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'engine_size': 2.0,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'أسود',
            'mileage': 15000,
            'country_origin': 'ألمانيا',
            'leather_seats': True,
            'sunroof': True,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة فاخرة بأداء عالي وتقنيات متطورة',
            'image_url': '/static/images/cars/mercedes-c200.jpg',
            'is_available': True
        },
        {
            'name': 'كيا بيكانتو 2020',
            'brand': 'كيا',
            'model': 'بيكانتو',
            'year': 2020,
            'price': 5000,
            'performance_level': 'low',
            'fuel_type': 'gasoline',
            'transmission': 'manual',
            'engine_size': 1.2,
            'doors': 4,
            'car_type': 'hatchback',
            'color': 'أحمر',
            'mileage': 45000,
            'country_origin': 'كوريا الجنوبية',
            'leather_seats': False,
            'sunroof': False,
            'gps_system': False,
            'backup_camera': False,
            'entertainment_system': True,
            'safety_features': False,
            'description': 'سيارة اقتصادية مثالية للاستخدام اليومي في المدينة',
            'image_url': '/static/images/cars/kia-picanto.jpg',
            'is_available': True
        },
        {
            'name': 'بي إم دبليو 320i 2022',
            'brand': 'بي إم دبليو',
            'model': '320i',
            'year': 2022,
            'price': 18000,
            'performance_level': 'high',
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'engine_size': 2.0,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'أزرق',
            'mileage': 20000,
            'country_origin': 'ألمانيا',
            'leather_seats': True,
            'sunroof': True,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة رياضية فاخرة بأداء استثنائي',
            'image_url': '/static/images/cars/bmw-x5.jpg',
            'is_available': True
        },
        {
            'name': 'تويوتا كامري هايبرد 2023',
            'brand': 'تويوتا',
            'model': 'كامري',
            'year': 2023,
            'price': 12000,
            'performance_level': 'high',
            'fuel_type': 'hybrid',
            'transmission': 'automatic',
            'engine_size': 2.5,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'رمادي',
            'mileage': 10000,
            'country_origin': 'اليابان',
            'leather_seats': True,
            'sunroof': True,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة هجين صديقة للبيئة مع توفير ممتاز في الوقود',
            'image_url': '/static/images/cars/toyota-camry.jpg',
            'is_available': True
        },
        {
            'name': 'نيسان التيما 2021',
            'brand': 'نيسان',
            'model': 'التيما',
            'year': 2021,
            'price': 9000,
            'performance_level': 'medium',
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'engine_size': 2.5,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'ذهبي',
            'mileage': 35000,
            'country_origin': 'اليابان',
            'leather_seats': True,
            'sunroof': False,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة متوسطة الحجم مريحة ومناسبة للعائلات',
            'image_url': '/static/images/cars/nissan-altima.jpg',
            'is_available': True
        },
        {
            'name': 'هوندا سيفيك 2022',
            'brand': 'هوندا',
            'model': 'سيفيك',
            'year': 2022,
            'price': 10500,
            'performance_level': 'medium',
            'fuel_type': 'gasoline',
            'transmission': 'automatic',
            'engine_size': 1.5,
            'doors': 4,
            'car_type': 'sedan',
            'color': 'أبيض',
            'mileage': 18000,
            'country_origin': 'اليابان',
            'leather_seats': False,
            'sunroof': True,
            'gps_system': True,
            'backup_camera': True,
            'entertainment_system': True,
            'safety_features': True,
            'description': 'سيارة رياضية أنيقة بتقنيات حديثة',
            'image_url': '/static/images/cars/honda-civic.jpg',
            'is_available': True
        }
    ]
    
    for car_data in sample_cars:
        car = Car(**car_data)
        car.update_normalized_fields()
        db.session.add(car)
    
    db.session.commit()
    print(f"تم إضافة {len(sample_cars)} سيارة تجريبية")

def add_default_admin():
    """إضافة مدير افتراضي"""
    admin = Admin(
        username='admin',
        password_hash=generate_password_hash('admin123'),
        is_active=True
    )
    db.session.add(admin)
    db.session.commit()
    print("تم إضافة المدير الافتراضي: admin / admin123")

def reset_database(app: Flask):
    """إعادة تعيين قاعدة البيانات"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        add_sample_cars()
        add_default_admin()
        print("تم إعادة تعيين قاعدة البيانات بنجاح")

def backup_database(app: Flask, backup_file: str):
    """نسخ احتياطي لقاعدة البيانات"""
    with app.app_context():
        cars = Car.query.all()
        admins = Admin.query.all()
        
        backup_data = {
            'cars': [car.to_dict() for car in cars],
            'admins': [{'username': admin.username, 'is_active': admin.is_active} for admin in admins],
            'backup_date': str(db.func.now())
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        print(f"تم إنشاء نسخة احتياطية في: {backup_file}")