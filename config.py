import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'car-store-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///car_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات التطبيق
    CARS_PER_PAGE = 12
    ADMIN_USERNAME = 'admin'
    ADMIN_PASSWORD = 'admin123'  # يجب تغييرها في الإنتاج
    
    # إعدادات اللغة
    DEFAULT_LANGUAGE = 'ar'
    SUPPORTED_LANGUAGES = ['ar', 'en']