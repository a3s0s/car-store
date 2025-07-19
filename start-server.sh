#!/bin/bash

# سكريبت تشغيل متجر السيارات الذكي
# Smart Car Store Startup Script

echo "============================================================"
echo "🚗 متجر السيارات الذكي - Smart Car Store"
echo "============================================================"

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت / Python 3 is not installed"
    exit 1
fi

# التحقق من وجود pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 غير مثبت / pip3 is not installed"
    exit 1
fi

# الانتقال إلى مجلد المشروع
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 مجلد المشروع / Project Directory: $SCRIPT_DIR"

# التحقق من وجود الملفات المطلوبة
if [ ! -f "production.py" ]; then
    echo "❌ ملف production.py غير موجود / production.py file not found"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ ملف requirements.txt غير موجود / requirements.txt file not found"
    exit 1
fi

# تثبيت المتطلبات
echo "📦 تثبيت المتطلبات / Installing requirements..."
pip3 install -r requirements.txt

# التحقق من وجود قاعدة البيانات
if [ ! -f "car_store.db" ]; then
    echo "🗄️  إنشاء قاعدة البيانات / Creating database..."
    python3 -c "from database import init_database; from app import create_app; app = create_app(); init_database(app)"
fi

# التحقق من وجود مجلد الصور
if [ ! -d "static/images/cars" ]; then
    echo "📁 إنشاء مجلد الصور / Creating images directory..."
    mkdir -p static/images/cars
fi

# التحقق من وجود الصورة البديلة
if [ ! -f "static/images/cars/placeholder.jpg" ]; then
    echo "🖼️  إنشاء الصورة البديلة / Creating placeholder image..."
    python3 -c "
from PIL import Image, ImageDraw
import os
os.makedirs('static/images/cars', exist_ok=True)
img = Image.new('RGB', (400, 300), color='#f0f0f0')
draw = ImageDraw.Draw(img)
draw.rectangle([10, 10, 390, 290], outline='#cccccc', width=2)
img.save('static/images/cars/placeholder.jpg', 'JPEG', quality=85)
print('✅ تم إنشاء placeholder.jpg')
"
fi

# التحقق من المنفذ
PORT=${PORT:-5000}
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  المنفذ $PORT مستخدم / Port $PORT is already in use"
    echo "🔄 محاولة إيقاف العملية السابقة / Trying to stop previous process..."
    pkill -f "production.py" || true
    sleep 2
fi

echo "============================================================"
echo "🚀 بدء تشغيل الخادم / Starting server..."
echo "📍 العنوان / Address: http://localhost:$PORT"
echo "⚙️  لوحة الإدارة / Admin Panel: http://localhost:$PORT/admin"
echo "🔑 بيانات المدير / Admin Credentials: admin / admin123"
echo "============================================================"
echo "💡 لإيقاف الخادم اضغط Ctrl+C / To stop server press Ctrl+C"
echo "============================================================"

# تشغيل الخادم
python3 production.py