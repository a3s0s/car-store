#!/usr/bin/env python3
"""
ملف تشغيل التطبيق في بيئة الإنتاج
Production server for the Smart Car Store application
"""

import os
import sys
from app import create_app

def main():
    """تشغيل التطبيق في بيئة الإنتاج"""
    
    # إنشاء التطبيق
    app = create_app()
    
    # إعدادات الإنتاج
    app.config['DEBUG'] = False
    app.config['ENV'] = 'production'
    
    # الحصول على المنفذ من متغيرات البيئة أو استخدام 5000 كافتراضي
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 بدء تشغيل متجر السيارات الذكي في بيئة الإنتاج...")
    print(f"📍 العنوان: http://{host}:{port}")
    print(f"🔧 البيئة: {app.config['ENV']}")
    print(f"🐛 وضع التطوير: {app.config['DEBUG']}")
    print("=" * 50)
    
    try:
        # تشغيل التطبيق
        app.run(
            host=host,
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n⏹️  تم إيقاف الخادم بواسطة المستخدم")
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()