# دليل تثبيت وتشغيل متجر السيارات الذكي
# Smart Car Store Installation Guide

## متطلبات النظام / System Requirements

### Python
- Python 3.8 أو أحدث / Python 3.8 or newer
- pip (مدير الحزم) / pip (package manager)

### قواعد البيانات / Database
- SQLite (مدمج مع Python) / SQLite (included with Python)

## خطوات التثبيت / Installation Steps

### 1. تحميل المشروع / Download Project
```bash
# إذا كان لديك Git
# If you have Git
git clone <repository-url>
cd متجر-السيارات-الذكي

# أو قم بتحميل الملفات مباشرة
# Or download files directly
```

### 2. إنشاء بيئة افتراضية / Create Virtual Environment
```bash
# إنشاء البيئة الافتراضية
# Create virtual environment
python -m venv venv

# تفعيل البيئة الافتراضية (Windows)
# Activate virtual environment (Windows)
venv\Scripts\activate

# تفعيل البيئة الافتراضية (macOS/Linux)
# Activate virtual environment (macOS/Linux)
source venv/bin/activate
```

### 3. تثبيت المتطلبات / Install Requirements
```bash
# تثبيت جميع المكتبات المطلوبة
# Install all required packages
pip install -r requirements.txt
```

### 4. تهيئة قاعدة البيانات / Initialize Database
```bash
# تشغيل سكريبت تهيئة قاعدة البيانات
# Run database initialization script
python database.py
```

### 5. تشغيل التطبيق / Run Application
```bash
# تشغيل الخادم
# Start the server
python run.py

# أو استخدم
# Or use
python app.py
```

## الوصول للتطبيق / Accessing the Application

بعد تشغيل الخادم، يمكنك الوصول للتطبيق عبر:
After starting the server, you can access the application at:

- **الصفحة الرئيسية / Home Page**: http://localhost:5000
- **البحث المتقدم / Advanced Search**: http://localhost:5000/search
- **لوحة الإدارة / Admin Panel**: http://localhost:5000/admin

## بيانات تسجيل الدخول الافتراضية / Default Login Credentials

### المدير / Administrator
- **اسم المستخدم / Username**: `admin`
- **كلمة المرور / Password**: `admin123`

⚠️ **تحذير / Warning**: تأكد من تغيير كلمة المرور في بيئة الإنتاج!
Make sure to change the password in production environment!

## هيكل المشروع / Project Structure

```
متجر-السيارات-الذكي/
├── app.py                 # التطبيق الرئيسي / Main application
├── run.py                 # ملف التشغيل / Run file
├── config.py              # إعدادات التطبيق / App configuration
├── models.py              # نماذج قاعدة البيانات / Database models
├── database.py            # تهيئة قاعدة البيانات / Database initialization
├── search_engine.py       # محرك البحث / Search engine
├── utils.py               # وظائف مساعدة / Utility functions
├── requirements.txt       # متطلبات Python / Python requirements
├── README.md              # دليل المستخدم / User guide
├── INSTALL.md             # دليل التثبيت / Installation guide
├── .gitignore             # ملفات Git المتجاهلة / Git ignore file
├── static/                # الملفات الثابتة / Static files
│   ├── css/
│   │   └── style.css      # ملف الأنماط المخصص / Custom styles
│   ├── js/
│   │   └── main.js        # ملف JavaScript الرئيسي / Main JavaScript
│   └── favicon.ico        # أيقونة الموقع / Site icon
├── templates/             # قوالب HTML / HTML templates
│   ├── base.html          # القالب الأساسي / Base template
│   ├── index.html         # الصفحة الرئيسية / Home page
│   ├── search.html        # صفحة البحث / Search page
│   ├── car_details.html   # تفاصيل السيارة / Car details
│   ├── compare.html       # مقارنة السيارات / Car comparison
│   ├── admin/             # قوالب لوحة الإدارة / Admin templates
│   │   ├── login.html     # تسجيل دخول المدير / Admin login
│   │   ├── dashboard.html # لوحة التحكم / Dashboard
│   │   ├── cars.html      # إدارة السيارات / Car management
│   │   ├── add_car.html   # إضافة سيارة / Add car
│   │   └── edit_car.html  # تعديل سيارة / Edit car
│   └── errors/            # صفحات الأخطاء / Error pages
│       ├── 404.html       # صفحة غير موجودة / Page not found
│       └── 500.html       # خطأ خادم / Server error
└── instance/              # ملفات قاعدة البيانات / Database files
    └── car_store.db       # قاعدة بيانات SQLite / SQLite database
```

## الميزات المتاحة / Available Features

### للمستخدمين / For Users
- ✅ البحث السريع والمتقدم / Quick and advanced search
- ✅ تصفية السيارات حسب معايير متعددة / Filter cars by multiple criteria
- ✅ مقارنة السيارات / Car comparison
- ✅ عرض تفاصيل السيارة / View car details
- ✅ واجهة عربية متجاوبة / Responsive Arabic interface

### للمدراء / For Administrators
- ✅ لوحة تحكم شاملة / Comprehensive dashboard
- ✅ إضافة وتعديل السيارات / Add and edit cars
- ✅ إدارة قاعدة البيانات / Database management
- ✅ عرض الإحصائيات / View statistics
- ✅ تسجيل عمليات البحث / Search logging

## استكشاف الأخطاء / Troubleshooting

### مشكلة: خطأ في تثبيت المتطلبات
### Issue: Requirements installation error
```bash
# تحديث pip
# Update pip
python -m pip install --upgrade pip

# إعادة تثبيت المتطلبات
# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### مشكلة: خطأ في قاعدة البيانات
### Issue: Database error
```bash
# حذف قاعدة البيانات وإعادة إنشائها
# Delete database and recreate
rm instance/car_store.db
python database.py
```

### مشكلة: المنفذ مستخدم
### Issue: Port already in use
```bash
# تغيير المنفذ في run.py أو app.py
# Change port in run.py or app.py
# من port=5000 إلى port=8000
# From port=5000 to port=8000
```

### مشكلة: خطأ في الترميز العربي
### Issue: Arabic encoding error
```bash
# تأكد من أن terminal يدعم UTF-8
# Make sure terminal supports UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

## التطوير / Development

### إضافة ميزات جديدة / Adding New Features
1. قم بتعديل `models.py` لإضافة جداول جديدة / Modify `models.py` to add new tables
2. أضف routes جديدة في `app.py` / Add new routes in `app.py`
3. أنشئ قوالب HTML في مجلد `templates/` / Create HTML templates in `templates/` folder
4. أضف أنماط CSS في `static/css/style.css` / Add CSS styles in `static/css/style.css`

### اختبار التطبيق / Testing the Application
```bash
# تشغيل في وضع التطوير
# Run in development mode
export FLASK_ENV=development
python run.py
```

## النشر / Deployment

### للنشر على خادم إنتاج / For Production Deployment
1. قم بتغيير `DEBUG = False` في `config.py` / Change `DEBUG = False` in `config.py`
2. قم بتغيير كلمة مرور المدير / Change admin password
3. استخدم خادم WSGI مثل Gunicorn / Use WSGI server like Gunicorn
4. قم بإعداد خادم ويب مثل Nginx / Setup web server like Nginx

```bash
# تثبيت Gunicorn
# Install Gunicorn
pip install gunicorn

# تشغيل التطبيق
# Run application
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## الدعم / Support

إذا واجهت أي مشاكل، يرجى:
If you encounter any issues, please:

1. تحقق من ملف `README.md` للمزيد من المعلومات / Check `README.md` for more information
2. تأكد من تثبيت جميع المتطلبات بشكل صحيح / Ensure all requirements are installed correctly
3. تحقق من سجلات الأخطاء في terminal / Check error logs in terminal

## الترخيص / License

هذا المشروع مفتوح المصدر ومتاح للاستخدام التعليمي والتجاري.
This project is open source and available for educational and commercial use.

---

**تم تطوير هذا المشروع بواسطة فريق متجر السيارات الذكي**
**Developed by Smart Car Store Team**