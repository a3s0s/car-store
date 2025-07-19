from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils import normalize_arabic, create_search_terms

db = SQLAlchemy()

class Car(db.Model):
    """نموذج بيانات السيارة"""
    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # المعلومات الأساسية
    name = db.Column(db.String(200), nullable=False)
    name_normalized = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    brand_normalized = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # مواصفات السيارة
    performance_level = db.Column(db.String(20), nullable=False)  # low, medium, high
    fuel_type = db.Column(db.String(20), nullable=False)  # gasoline, diesel, hybrid, electric
    transmission = db.Column(db.String(20), nullable=False)  # manual, automatic, cvt
    engine_size = db.Column(db.Float)  # حجم المحرك باللتر
    doors = db.Column(db.Integer, default=4)  # عدد الأبواب
    car_type = db.Column(db.String(30), nullable=False)  # sedan, suv, hatchback, etc.
    color = db.Column(db.String(50))
    mileage = db.Column(db.Integer, default=0)  # المسافة المقطوعة بالكيلومتر
    country_origin = db.Column(db.String(50))  # بلد المنشأ
    
    # ميزات إضافية (Boolean fields)
    leather_seats = db.Column(db.Boolean, default=False)
    sunroof = db.Column(db.Boolean, default=False)
    gps_system = db.Column(db.Boolean, default=False)
    backup_camera = db.Column(db.Boolean, default=False)
    entertainment_system = db.Column(db.Boolean, default=False)
    safety_features = db.Column(db.Boolean, default=False)
    
    # معلومات إضافية
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)  # السيارات المميزة
    
    # تواريخ
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Car, self).__init__(**kwargs)
        # تطبيع النصوص عند الإنشاء
        if self.name:
            self.name_normalized = normalize_arabic(self.name)
        if self.brand:
            self.brand_normalized = normalize_arabic(self.brand)
    
    def update_normalized_fields(self):
        """تحديث الحقول المطبعة"""
        if self.name:
            self.name_normalized = normalize_arabic(self.name)
        if self.brand:
            self.brand_normalized = normalize_arabic(self.brand)
    
    def get_search_terms(self):
        """الحصول على مصطلحات البحث للسيارة"""
        terms = []
        
        if self.name:
            terms.extend(create_search_terms(self.name))
        if self.brand:
            terms.extend(create_search_terms(self.brand))
        if self.model:
            terms.extend(create_search_terms(self.model))
        
        return list(set(terms))  # إزالة التكرار
    
    def matches_criteria(self, criteria):
        """فحص ما إذا كانت السيارة تطابق المعايير المحددة"""
        
        # فحص الميزانية
        if 'budget' in criteria and criteria['budget']:
            if self.price > float(criteria['budget']):
                return False
        
        # فحص مستوى الأداء
        if 'performance_level' in criteria and criteria['performance_level']:
            if self.performance_level != criteria['performance_level']:
                return False
        
        # فحص نوع الوقود
        if 'fuel_type' in criteria and criteria['fuel_type']:
            if self.fuel_type != criteria['fuel_type']:
                return False
        
        # فحص نوع الجير
        if 'transmission' in criteria and criteria['transmission']:
            if self.transmission != criteria['transmission']:
                return False
        
        # فحص نوع السيارة
        if 'car_type' in criteria and criteria['car_type']:
            if self.car_type != criteria['car_type']:
                return False
        
        # فحص سنة الصنع
        if 'year_from' in criteria and criteria['year_from']:
            if self.year < int(criteria['year_from']):
                return False
        
        if 'year_to' in criteria and criteria['year_to']:
            if self.year > int(criteria['year_to']):
                return False
        
        # فحص الماركة
        if 'brand' in criteria and criteria['brand']:
            brand_normalized = normalize_arabic(criteria['brand'])
            if brand_normalized not in self.brand_normalized:
                return False
        
        # فحص اللون
        if 'color' in criteria and criteria['color']:
            color_normalized = normalize_arabic(criteria['color'])
            car_color_normalized = normalize_arabic(self.color or '')
            if color_normalized not in car_color_normalized:
                return False
        
        # فحص عدد الأبواب
        if 'doors' in criteria and criteria['doors']:
            if self.doors != int(criteria['doors']):
                return False
        
        # فحص الميزات الإضافية
        feature_mapping = {
            'leather_seats': self.leather_seats,
            'sunroof': self.sunroof,
            'gps_system': self.gps_system,
            'backup_camera': self.backup_camera,
            'entertainment_system': self.entertainment_system,
            'safety_features': self.safety_features
        }
        
        for feature, required in criteria.items():
            if feature in feature_mapping and required:
                if not feature_mapping[feature]:
                    return False
        
        return True
    
    def to_dict(self):
        """تحويل السيارة إلى قاموس"""
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'performance_level': self.performance_level,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'engine_size': self.engine_size,
            'doors': self.doors,
            'car_type': self.car_type,
            'color': self.color,
            'mileage': self.mileage,
            'country_origin': self.country_origin,
            'leather_seats': self.leather_seats,
            'sunroof': self.sunroof,
            'gps_system': self.gps_system,
            'backup_camera': self.backup_camera,
            'entertainment_system': self.entertainment_system,
            'safety_features': self.safety_features,
            'description': self.description,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Car {self.name} - {self.year}>'

class Admin(db.Model):
    """نموذج بيانات المدير"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class SearchLog(db.Model):
    """سجل عمليات البحث لتحليل سلوك المستخدمين"""
    __tablename__ = 'search_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    search_criteria = db.Column(db.Text)  # JSON string
    results_count = db.Column(db.Integer)
    user_ip = db.Column(db.String(45))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SearchLog {self.id} - {self.results_count} results>'