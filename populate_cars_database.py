#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مدير قاعدة بيانات السيارات الشامل
يقوم بإضافة مجموعة واسعة من السيارات من جميع الماركات العالمية
"""

import os
import sys
import requests
import uuid
from PIL import Image
from io import BytesIO
import time

# إضافة المجلد الحالي إلى المسار
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Car

def download_and_save_image(image_url, car_name):
    """
    تحميل وحفظ صورة السيارة
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # إنشاء اسم ملف فريد
        file_extension = image_url.split('.')[-1].lower()
        if file_extension not in ['jpg', 'jpeg', 'png', 'webp']:
            file_extension = 'jpg'
        
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join('static', 'images', 'cars', filename)
        
        # التأكد من وجود المجلد
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # حفظ الصورة
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ تم تحميل صورة {car_name}: {filename}")
        return filename
        
    except Exception as e:
        print(f"❌ فشل تحميل صورة {car_name}: {str(e)}")
        return None

def get_comprehensive_cars_data():
    """
    قاعدة بيانات شاملة للسيارات من جميع الماركات العالمية
    """
    cars_data = [
        # تويوتا - Toyota
        {
            'name': 'تويوتا كامري 2024',
            'brand': 'تويوتا',
            'model': 'كامري',
            'year': 2024,
            'price': 28000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': 2.5,
            'doors': 4,
            'color': 'أبيض',
            'performance_level': 'عالي',
            'car_type': 'سيدان',
            'leather_seats': True,
            'entertainment_system': True,
            'backup_camera': True,
            'gps_system': True,
            'safety_features': True,
            'sunroof': False,
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?w=800&h=600&fit=crop'
        },
        {
            'name': 'تويوتا كورولا 2024',
            'brand': 'تويوتا',
            'model': 'كورولا',
            'year': 2024,
            'price': 22000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'فضي',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop'
        },
        {
            'name': 'تويوتا RAV4 2024',
            'brand': 'تويوتا',
            'model': 'RAV4',
            'year': 2024,
            'price': 32000,
            'mileage': 0,
            'fuel_type': 'هايبرد',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.5',
            'doors': 5,
            'color': 'أزرق',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&h=600&fit=crop'
        },
        {
            'name': 'تويوتا برادو 2024',
            'brand': 'تويوتا',
            'model': 'برادو',
            'year': 2024,
            'price': 45000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '4.0',
            'doors': 5,
            'color': 'أسود',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف', 'نظام ترفيه'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # هوندا - Honda
        {
            'name': 'هوندا أكورد 2024',
            'brand': 'هوندا',
            'model': 'أكورد',
            'year': 2024,
            'price': 26000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'أحمر',
            'performance_level': 'عالي',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop'
        },
        {
            'name': 'هوندا سيفيك 2024',
            'brand': 'هوندا',
            'model': 'سيفيك',
            'year': 2024,
            'price': 24000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'أبيض',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&h=600&fit=crop'
        },
        {
            'name': 'هوندا CR-V 2024',
            'brand': 'هوندا',
            'model': 'CR-V',
            'year': 2024,
            'price': 30000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.4',
            'doors': 5,
            'color': 'فضي',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # نيسان - Nissan
        {
            'name': 'نيسان التيما 2024',
            'brand': 'نيسان',
            'model': 'التيما',
            'year': 2024,
            'price': 25000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.5',
            'doors': 4,
            'color': 'أزرق',
            'performance_level': 'عالي',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop'
        },
        {
            'name': 'نيسان باترول 2024',
            'brand': 'نيسان',
            'model': 'باترول',
            'year': 2024,
            'price': 50000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '5.6',
            'doors': 5,
            'color': 'أبيض',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف', 'نظام ترفيه'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # مرسيدس - Mercedes
        {
            'name': 'مرسيدس C200 2024',
            'brand': 'مرسيدس',
            'model': 'C200',
            'year': 2024,
            'price': 45000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'أسود',
            'performance_level': 'عالي جداً',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف', 'ميزات السلامة'],
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&h=600&fit=crop'
        },
        {
            'name': 'مرسيدس E300 2024',
            'brand': 'مرسيدس',
            'model': 'E300',
            'year': 2024,
            'price': 55000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.0',
            'doors': 4,
            'color': 'فضي',
            'performance_level': 'عالي جداً',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&h=600&fit=crop'
        },
        {
            'name': 'مرسيدس GLE 2024',
            'brand': 'مرسيدس',
            'model': 'GLE',
            'year': 2024,
            'price': 70000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.0',
            'doors': 5,
            'color': 'أبيض',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # BMW
        {
            'name': 'بي إم دبليو 320i 2024',
            'brand': 'BMW',
            'model': '320i',
            'year': 2024,
            'price': 42000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'أزرق',
            'performance_level': 'عالي جداً',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف', 'ميزات السلامة'],
            'is_featured': True,
            'image_url': 'https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&h=600&fit=crop'
        },
        {
            'name': 'بي إم دبليو X5 2024',
            'brand': 'BMW',
            'model': 'X5',
            'year': 2024,
            'price': 65000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.0',
            'doors': 5,
            'color': 'أسود',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # أودي - Audi
        {
            'name': 'أودي A4 2024',
            'brand': 'أودي',
            'model': 'A4',
            'year': 2024,
            'price': 40000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'رمادي',
            'performance_level': 'عالي جداً',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&h=600&fit=crop'
        },
        {
            'name': 'أودي Q7 2024',
            'brand': 'أودي',
            'model': 'Q7',
            'year': 2024,
            'price': 60000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.0',
            'doors': 5,
            'color': 'أبيض',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # لكزس - Lexus
        {
            'name': 'لكزس ES350 2024',
            'brand': 'لكزس',
            'model': 'ES350',
            'year': 2024,
            'price': 48000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.5',
            'doors': 4,
            'color': 'أبيض',
            'performance_level': 'عالي جداً',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop'
        },
        {
            'name': 'لكزس LX570 2024',
            'brand': 'لكزس',
            'model': 'LX570',
            'year': 2024,
            'price': 85000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '5.7',
            'doors': 5,
            'color': 'أسود',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # فولكس واجن - Volkswagen
        {
            'name': 'فولكس واجن جيتا 2024',
            'brand': 'فولكس واجن',
            'model': 'جيتا',
            'year': 2024,
            'price': 23000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '1.8',
            'doors': 4,
            'color': 'أحمر',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop'
        },
        {
            'name': 'فولكس واجن تيجوان 2024',
            'brand': 'فولكس واجن',
            'model': 'تيجوان',
            'year': 2024,
            'price': 28000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 5,
            'color': 'فضي',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # هيونداي - Hyundai
        {
            'name': 'هيونداي إلنترا 2024',
            'brand': 'هيونداي',
            'model': 'إلنترا',
            'year': 2024,
            'price': 21000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'أبيض',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop'
        },
        {
            'name': 'هيونداي توسان 2024',
            'brand': 'هيونداي',
            'model': 'توسان',
            'year': 2024,
            'price': 26000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.4',
            'doors': 5,
            'color': 'أزرق',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # كيا - Kia
        {
            'name': 'كيا أوبتيما 2024',
            'brand': 'كيا',
            'model': 'أوبتيما',
            'year': 2024,
            'price': 22000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.4',
            'doors': 4,
            'color': 'رمادي',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop'
        },
        {
            'name': 'كيا سورينتو 2024',
            'brand': 'كيا',
            'model': 'سورينتو',
            'year': 2024,
            'price': 29000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.3',
            'doors': 5,
            'color': 'أسود',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # فورد - Ford
        {
            'name': 'فورد فيوجن 2024',
            'brand': 'فورد',
            'model': 'فيوجن',
            'year': 2024,
            'price': 24000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.5',
            'doors': 4,
            'color': 'أحمر',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop'
        },
        {
            'name': 'فورد إكسبلورر 2024',
            'brand': 'فورد',
            'model': 'إكسبلورر',
            'year': 2024,
            'price': 35000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.5',
            'doors': 5,
            'color': 'أبيض',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # شيفروليه - Chevrolet
        {
            'name': 'شيفروليه ماليبو 2024',
            'brand': 'شيفروليه',
            'model': 'ماليبو',
            'year': 2024,
            'price': 25000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'أبيض',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop'
        },
        {
            'name': 'شيفروليه تاهو 2024',
            'brand': 'شيفروليه',
            'model': 'تاهو',
            'year': 2024,
            'price': 52000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '5.3',
            'doors': 5,
            'color': 'أسود',
            'performance_level': 'عالي جداً',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # جيب - Jeep
        {
            'name': 'جيب رانجلر 2024',
            'brand': 'جيب',
            'model': 'رانجلر',
            'year': 2024,
            'price': 38000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.6',
            'doors': 4,
            'color': 'أخضر',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },
        {
            'name': 'جيب جراند شيروكي 2024',
            'brand': 'جيب',
            'model': 'جراند شيروكي',
            'year': 2024,
            'price': 42000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '3.6',
            'doors': 5,
            'color': 'رمادي',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'فتحة سقف'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # مازدا - Mazda
        {
            'name': 'مازدا 6 2024',
            'brand': 'مازدا',
            'model': '6',
            'year': 2024,
            'price': 26000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.5',
            'doors': 4,
            'color': 'أحمر',
            'performance_level': 'عالي',
            'car_type': 'سيدان',
            'features': ['مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&h=600&fit=crop'
        },
        {
            'name': 'مازدا CX-5 2024',
            'brand': 'مازدا',
            'model': 'CX-5',
            'year': 2024,
            'price': 28000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.5',
            'doors': 5,
            'color': 'أزرق',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        },

        # سوبارو - Subaru
        {
            'name': 'سوبارو إمبريزا 2024',
            'brand': 'سوبارو',
            'model': 'إمبريزا',
            'year': 2024,
            'price': 23000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.0',
            'doors': 4,
            'color': 'فضي',
            'performance_level': 'متوسط',
            'car_type': 'سيدان',
            'features': ['دفع رباعي', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS', 'ميزات السلامة'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=800&h=600&fit=crop'
        },
        {
            'name': 'سوبارو فورستر 2024',
            'brand': 'سوبارو',
            'model': 'فورستر',
            'year': 2024,
            'price': 27000,
            'mileage': 0,
            'fuel_type': 'بنزين',
            'transmission': 'أوتوماتيك',
            'engine_size': '2.5',
            'doors': 5,
            'color': 'أخضر',
            'performance_level': 'عالي',
            'car_type': 'SUV',
            'features': ['دفع رباعي', 'مقاعد جلدية', 'نظام ترفيه', 'كاميرا خلفية', 'نظام GPS'],
            'is_featured': False,
            'image_url': 'https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&h=600&fit=crop'
        }
    ]
    
    return cars_data

def populate_database():
    """
    ملء قاعدة البيانات بالسيارات الشاملة
    """
    with app.app_context():
        print("🚀 بدء عملية ملء قاعدة البيانات...")
        print("🚀 Starting database population...")
        
        # حذف السيارات الموجودة
        Car.query.delete()
        db.session.commit()
        print("🗑️ تم حذف البيانات القديمة")
        
        cars_data = get_comprehensive_cars_data()
        total_cars = len(cars_data)
        successful_cars = 0
        
        print(f"📊 إجمالي السيارات للإضافة: {total_cars}")
        
        for i, car_data in enumerate(cars_data, 1):
            try:
                print(f"\n📝 [{i}/{total_cars}] معالجة: {car_data['name']}")
                
                # تحميل الصورة
                image_filename = download_and_save_image(
                    car_data['image_url'],
                    car_data['name']
                )
                
                if image_filename:
                    car_data['image'] = image_filename
                else:
                    # استخدام صورة افتراضية إذا فشل التحميل
                    car_data['image'] = 'default-car.jpg'
                
                # إزالة image_url من البيانات
                car_data.pop('image_url', None)
                
                # إنشاء السيارة
                car = Car(**car_data)
                db.session.add(car)
                db.session.commit()
                
                successful_cars += 1
                print(f"✅ تم إضافة: {car_data['name']}")
                
                # توقف قصير لتجنب الحمل الزائد
                time.sleep(0.5)
                
            except Exception as e:
                print(f"❌ خطأ في إضافة {car_data['name']}: {str(e)}")
                db.session.rollback()
                continue
        
        print(f"\n🎉 تم الانتهاء! تم إضافة {successful_cars} من أصل {total_cars} سيارة")
        print(f"🎉 Completed! Added {successful_cars} out of {total_cars} cars")

if __name__ == "__main__":
    populate_database()