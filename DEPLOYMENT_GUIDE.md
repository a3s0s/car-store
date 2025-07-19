# دليل التشغيل الدائم - متجر السيارات الذكي
# Permanent Deployment Guide - Smart Car Store

## 📋 المحتويات / Contents

1. [التشغيل السريع](#التشغيل-السريع)
2. [التشغيل باستخدام systemd](#التشغيل-باستخدام-systemd)
3. [إعداد nginx](#إعداد-nginx)
4. [التشغيل باستخدام Docker](#التشغيل-باستخدام-docker)
5. [المراقبة والصيانة](#المراقبة-والصيانة)
6. [استكشاف الأخطاء](#استكشاف-الأخطاء)

---

## 🚀 التشغيل السريع / Quick Start

### الطريقة الأولى: التشغيل المباشر
```bash
# الانتقال إلى مجلد المشروع
cd "/Users/abdulla/Documents/متجر الكتزوني"

# تشغيل الخادم في بيئة الإنتاج
python3 production.py
```

### الطريقة الثانية: التشغيل في الخلفية
```bash
# تشغيل الخادم في الخلفية
nohup python3 production.py > car-store.log 2>&1 &

# للتحقق من حالة التشغيل
ps aux | grep production.py

# لإيقاف الخادم
pkill -f production.py
```

---

## ⚙️ التشغيل باستخدام systemd

### 1. نسخ ملف الخدمة
```bash
# نسخ ملف الخدمة إلى مجلد systemd (يتطلب صلاحيات المدير)
sudo cp car-store.service /etc/systemd/system/

# أو للمستخدم الحالي فقط
mkdir -p ~/.config/systemd/user
cp car-store.service ~/.config/systemd/user/
```

### 2. تفعيل وتشغيل الخدمة
```bash
# إعادة تحميل إعدادات systemd
sudo systemctl daemon-reload

# تفعيل الخدمة للتشغيل التلقائي عند بدء النظام
sudo systemctl enable car-store.service

# تشغيل الخدمة
sudo systemctl start car-store.service

# التحقق من حالة الخدمة
sudo systemctl status car-store.service
```

### 3. أوامر إدارة الخدمة
```bash
# إيقاف الخدمة
sudo systemctl stop car-store.service

# إعادة تشغيل الخدمة
sudo systemctl restart car-store.service

# إعادة تحميل الإعدادات
sudo systemctl reload car-store.service

# عرض سجلات الخدمة
sudo journalctl -u car-store.service -f
```

---

## 🌐 إعداد nginx

### 1. تثبيت nginx (إذا لم يكن مثبتاً)
```bash
# على macOS باستخدام Homebrew
brew install nginx

# على Ubuntu/Debian
sudo apt update && sudo apt install nginx

# على CentOS/RHEL
sudo yum install nginx
```

### 2. إعداد التكوين
```bash
# نسخ ملف التكوين
sudo cp nginx-car-store.conf /etc/nginx/sites-available/car-store

# تفعيل الموقع (على Ubuntu/Debian)
sudo ln -s /etc/nginx/sites-available/car-store /etc/nginx/sites-enabled/

# على macOS مع Homebrew
sudo cp nginx-car-store.conf /usr/local/etc/nginx/servers/
```

### 3. اختبار وتشغيل nginx
```bash
# اختبار صحة التكوين
sudo nginx -t

# إعادة تحميل nginx
sudo nginx -s reload

# أو إعادة تشغيل nginx
sudo systemctl restart nginx
```

---

## 🐳 التشغيل باستخدام Docker

### 1. إنشاء Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "production.py"]
```

### 2. بناء وتشغيل الحاوية
```bash
# بناء الصورة
docker build -t car-store .

# تشغيل الحاوية
docker run -d -p 5000:5000 --name car-store-app car-store

# أو باستخدام docker-compose
docker-compose up -d
```

---

## 📊 المراقبة والصيانة

### 1. مراقبة الأداء
```bash
# مراقبة استخدام الموارد
htop

# مراقبة حركة الشبكة
netstat -tulpn | grep :5000

# مراقبة مساحة القرص
df -h

# مراقبة سجلات التطبيق
tail -f car-store.log
```

### 2. النسخ الاحتياطي
```bash
# نسخ احتياطي لقاعدة البيانات
cp car_store.db backup/car_store_$(date +%Y%m%d_%H%M%S).db

# نسخ احتياطي للصور
tar -czf backup/images_$(date +%Y%m%d_%H%M%S).tar.gz static/images/
```

### 3. التحديثات
```bash
# إيقاف الخدمة
sudo systemctl stop car-store.service

# تحديث الكود
git pull origin main

# تثبيت التحديثات
pip install -r requirements.txt

# إعادة تشغيل الخدمة
sudo systemctl start car-store.service
```

---

## 🔧 استكشاف الأخطاء

### المشاكل الشائعة وحلولها

#### 1. الخادم لا يبدأ
```bash
# التحقق من السجلات
sudo journalctl -u car-store.service -n 50

# التحقق من المنفذ
lsof -i :5000

# التحقق من الصلاحيات
ls -la production.py
chmod +x production.py
```

#### 2. مشاكل قاعدة البيانات
```bash
# التحقق من وجود قاعدة البيانات
ls -la car_store.db

# إعادة إنشاء قاعدة البيانات
python3 -c "from database import init_database; from app import create_app; app = create_app(); init_database(app)"
```

#### 3. مشاكل الصور
```bash
# التحقق من مجلد الصور
ls -la static/images/cars/

# إعادة إنشاء الصورة البديلة
python3 -c "
from PIL import Image, ImageDraw
import os
os.makedirs('static/images/cars', exist_ok=True)
img = Image.new('RGB', (400, 300), color='#f0f0f0')
draw = ImageDraw.Draw(img)
draw.rectangle([10, 10, 390, 290], outline='#cccccc', width=2)
img.save('static/images/cars/placeholder.jpg', 'JPEG', quality=85)
print('تم إنشاء placeholder.jpg')
"
```

#### 4. مشاكل nginx
```bash
# التحقق من حالة nginx
sudo systemctl status nginx

# التحقق من سجلات nginx
sudo tail -f /var/log/nginx/error.log

# اختبار التكوين
sudo nginx -t
```

---

## 🔒 الأمان

### 1. تغيير كلمة مرور المدير
```bash
python3 -c "
from app import create_app
from models import Admin, db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = Admin.query.filter_by(username='admin').first()
    if admin:
        admin.password_hash = generate_password_hash('كلمة_مرور_جديدة_قوية')
        db.session.commit()
        print('تم تغيير كلمة المرور بنجاح')
"
```

### 2. إعداد جدار الحماية
```bash
# السماح بالمنفذ 80 و 443 فقط
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. تحديثات الأمان
```bash
# تحديث النظام
sudo apt update && sudo apt upgrade

# تحديث Python packages
pip install --upgrade -r requirements.txt
```

---

## 📞 الدعم الفني

### معلومات الاتصال
- **المطور**: عبدالله
- **البريد الإلكتروني**: [البريد الإلكتروني]
- **الهاتف**: [رقم الهاتف]

### الملفات المهمة
- `production.py` - ملف تشغيل الإنتاج
- `car-store.service` - ملف خدمة systemd
- `nginx-car-store.conf` - إعداد nginx
- `car_store.db` - قاعدة البيانات
- `static/images/cars/` - مجلد الصور

### الروابط المفيدة
- الصفحة الرئيسية: http://localhost:5000
- لوحة الإدارة: http://localhost:5000/admin
- البحث المتقدم: http://localhost:5000/search

---

## 📝 ملاحظات إضافية

1. **النسخ الاحتياطي**: قم بعمل نسخ احتياطية دورية لقاعدة البيانات والصور
2. **المراقبة**: راقب استخدام الموارد والأداء بانتظام
3. **التحديثات**: حافظ على تحديث النظام والتطبيق
4. **الأمان**: غيّر كلمات المرور الافتراضية واستخدم HTTPS في الإنتاج
5. **السجلات**: راجع السجلات بانتظام لاكتشاف أي مشاكل مبكراً

---

*تم إنشاء هذا الدليل في: $(date)*
*آخر تحديث: $(date)*