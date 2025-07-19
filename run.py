#!/usr/bin/env python3
"""
ملف تشغيل متجر السيارات الذكي
Smart Car Store - Main Application Runner
"""

import os
import sys
from app import app

def main():
    """تشغيل التطبيق الرئيسي"""
    
    # التحقق من متطلبات Python
    if sys.version_info < (3, 7):
        print("خطأ: يتطلب Python 3.7 أو أحدث")
        print("Error: Python 3.7 or newer is required")
        sys.exit(1)
    
    # إعداد متغيرات البيئة
    os.environ.setdefault('FLASK_APP', 'app.py')
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # طباعة معلومات التشغيل
    print("=" * 60)
    print("🚗 متجر السيارات الذكي - Smart Car Store")
    print("=" * 60)
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🌐 Flask Environment: {os.environ.get('FLASK_ENV', 'production')}")
    print("=" * 60)
    print("🚀 بدء تشغيل الخادم...")
    print("🚀 Starting server...")
    print("=" * 60)
    print("📱 يمكنك الوصول للتطبيق عبر:")
    print("📱 You can access the application at:")
    print("   🏠 الصفحة الرئيسية: http://localhost:5000")
    print("   🏠 Home Page: http://localhost:5000")
    print("   🔍 البحث المتقدم: http://localhost:5000/search")
    print("   🔍 Advanced Search: http://localhost:5000/search")
    print("   ⚙️  لوحة الإدارة: http://localhost:5000/admin")
    print("   ⚙️  Admin Panel: http://localhost:5000/admin")
    print("=" * 60)
    print("🔑 بيانات تسجيل دخول المدير الافتراضية:")
    print("🔑 Default Admin Login Credentials:")
    print("   👤 اسم المستخدم / Username: admin")
    print("   🔒 كلمة المرور / Password: admin123")
    print("=" * 60)
    print("⚠️  ملاحظة: تأكد من تغيير كلمة مرور المدير في الإنتاج")
    print("⚠️  Note: Make sure to change admin password in production")
    print("=" * 60)
    
    try:
        # تشغيل التطبيق
        app.run(
            host='0.0.0.0',  # السماح بالوصول من جميع العناوين
            port=5000,       # المنفذ الافتراضي
            debug=True,      # وضع التطوير
            threaded=True    # دعم الخيوط المتعددة
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("🛑 تم إيقاف الخادم بواسطة المستخدم")
        print("🛑 Server stopped by user")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ خطأ في تشغيل الخادم: {e}")
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()