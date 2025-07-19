#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لتطبيق متجر السيارات الذكي
"""

import sys
import os
import requests
import json
from urllib.parse import quote

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_homepage():
    """اختبار الصفحة الرئيسية"""
    print("🏠 اختبار الصفحة الرئيسية...")
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ الصفحة الرئيسية تعمل بشكل صحيح")
            return True
        else:
            print(f"❌ خطأ في الصفحة الرئيسية: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالصفحة الرئيسية: {e}")
        return False

def test_search_page():
    """اختبار صفحة البحث"""
    print("🔍 اختبار صفحة البحث...")
    try:
        response = requests.get("http://localhost:5000/search")
        if response.status_code == 200:
            if "تم العثور على" in response.text:
                print("✅ صفحة البحث تعمل بشكل صحيح")
                return True
            else:
                print("❌ صفحة البحث لا تعرض النتائج")
                return False
        else:
            print(f"❌ خطأ في صفحة البحث: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال بصفحة البحث: {e}")
        return False

def test_search_with_criteria():
    """اختبار البحث مع معايير"""
    print("🔍 اختبار البحث مع معايير...")
    try:
        # اختبار البحث بالماركة
        response = requests.get("http://localhost:5000/search?brand=تويوتا")
        if response.status_code == 200:
            print("✅ البحث بالماركة يعمل")
        
        # اختبار البحث بالسعر
        response = requests.get("http://localhost:5000/search?price_max=10000")
        if response.status_code == 200:
            print("✅ البحث بالسعر يعمل")
        
        # اختبار البحث بنوع الوقود
        response = requests.get("http://localhost:5000/search?fuel_type=gasoline")
        if response.status_code == 200:
            print("✅ البحث بنوع الوقود يعمل")
            
        return True
    except Exception as e:
        print(f"❌ خطأ في البحث مع المعايير: {e}")
        return False

def test_admin_login_page():
    """اختبار صفحة تسجيل دخول المدير"""
    print("👤 اختبار صفحة تسجيل دخول المدير...")
    try:
        response = requests.get("http://localhost:5000/admin")
        if response.status_code == 200:
            if "تسجيل دخول المدير" in response.text:
                print("✅ صفحة تسجيل دخول المدير تعمل")
                return True
            else:
                print("❌ صفحة تسجيل دخول المدير لا تحتوي على المحتوى المطلوب")
                return False
        else:
            print(f"❌ خطأ في صفحة تسجيل دخول المدير: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطأ في الاتصال بصفحة تسجيل دخول المدير: {e}")
        return False

def test_static_files():
    """اختبار الملفات الثابتة"""
    print("📁 اختبار الملفات الثابتة...")
    static_files = [
        "/static/css/style.css",
        "/static/js/main.js",
        "/static/favicon.ico",
        "/static/images/cars/placeholder.jpg"
    ]
    
    success_count = 0
    for file_path in static_files:
        try:
            response = requests.get(f"http://localhost:5000{file_path}")
            if response.status_code == 200:
                print(f"✅ {file_path} متاح")
                success_count += 1
            else:
                print(f"❌ {file_path} غير متاح ({response.status_code})")
        except Exception as e:
            print(f"❌ خطأ في الوصول إلى {file_path}: {e}")
    
    return success_count == len(static_files)

def test_database_connection():
    """اختبار الاتصال بقاعدة البيانات"""
    print("🗄️ اختبار الاتصال بقاعدة البيانات...")
    try:
        from app import app
        from models import Car, Admin
        
        with app.app_context():
            car_count = Car.query.count()
            admin_count = Admin.query.count()
            
            print(f"✅ قاعدة البيانات متصلة - {car_count} سيارة، {admin_count} مدير")
            return car_count > 0 and admin_count > 0
    except Exception as e:
        print(f"❌ خطأ في الاتصال بقاعدة البيانات: {e}")
        return False

def test_search_engine():
    """اختبار محرك البحث"""
    print("🔍 اختبار محرك البحث...")
    try:
        from app import app
        from search_engine import search_engine
        
        with app.app_context():
            # اختبار البحث بدون معايير
            results = search_engine.search({})
            print(f"✅ البحث بدون معايير: {results['total']} نتيجة")
            
            # اختبار البحث بالنص
            results = search_engine.search({'search_text': 'تويوتا'})
            print(f"✅ البحث بالنص 'تويوتا': {results['total']} نتيجة")
            
            # اختبار البحث بالماركة
            results = search_engine.search({'brand': 'تويوتا'})
            print(f"✅ البحث بالماركة 'تويوتا': {results['total']} نتيجة")
            
            return True
    except Exception as e:
        print(f"❌ خطأ في محرك البحث: {e}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("=" * 60)
    print("🚗 اختبار شامل لمتجر السيارات الذكي")
    print("=" * 60)
    
    tests = [
        ("الصفحة الرئيسية", test_homepage),
        ("صفحة البحث", test_search_page),
        ("البحث مع معايير", test_search_with_criteria),
        ("صفحة تسجيل دخول المدير", test_admin_login_page),
        ("الملفات الثابتة", test_static_files),
        ("قاعدة البيانات", test_database_connection),
        ("محرك البحث", test_search_engine)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        if test_func():
            passed += 1
        print("-" * 40)
    
    print("\n" + "=" * 60)
    print(f"📊 نتائج الاختبار: {passed}/{total} اختبار نجح")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! التطبيق يعمل بشكل مثالي")
        return True
    else:
        print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء أعلاه")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)