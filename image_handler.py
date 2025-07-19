import os
import uuid
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app

class ImageHandler:
    """معالج رفع وتحسين الصور"""
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    IMAGE_QUALITY = 85
    MAX_WIDTH = 1200
    MAX_HEIGHT = 800
    
    @staticmethod
    def allowed_file(filename):
        """التحقق من امتداد الملف المسموح"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ImageHandler.ALLOWED_EXTENSIONS
    
    @staticmethod
    def generate_unique_filename(original_filename):
        """إنشاء اسم ملف فريد"""
        ext = original_filename.rsplit('.', 1)[1].lower()
        unique_id = str(uuid.uuid4())
        return f"{unique_id}.{ext}"
    
    @staticmethod
    def validate_image_file(file):
        """التحقق من صحة ملف الصورة"""
        errors = []
        
        # التحقق من وجود الملف
        if not file or file.filename == '':
            errors.append('لم يتم اختيار ملف')
            return errors
        
        # التحقق من امتداد الملف
        if not ImageHandler.allowed_file(file.filename):
            errors.append(f'امتداد الملف غير مدعوم. الامتدادات المدعومة: {", ".join(ImageHandler.ALLOWED_EXTENSIONS)}')
        
        # التحقق من حجم الملف
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > ImageHandler.MAX_FILE_SIZE:
            errors.append(f'حجم الملف كبير جداً. الحد الأقصى: {ImageHandler.MAX_FILE_SIZE // (1024*1024)}MB')
        
        return errors
    
    @staticmethod
    def process_and_save_image(file, upload_folder='static/images/cars'):
        """معالجة وحفظ الصورة"""
        try:
            # التحقق من صحة الملف
            errors = ImageHandler.validate_image_file(file)
            if errors:
                return None, errors
            
            # إنشاء مجلد الرفع إذا لم يكن موجوداً
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            # إنشاء اسم ملف فريد
            filename = ImageHandler.generate_unique_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            
            # فتح الصورة باستخدام Pillow
            image = Image.open(file)
            
            # تحويل الصورة إلى RGB إذا كانت RGBA
            if image.mode in ('RGBA', 'LA', 'P'):
                # إنشاء خلفية بيضاء
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # تغيير حجم الصورة إذا كانت كبيرة
            if image.width > ImageHandler.MAX_WIDTH or image.height > ImageHandler.MAX_HEIGHT:
                image.thumbnail((ImageHandler.MAX_WIDTH, ImageHandler.MAX_HEIGHT), Image.Resampling.LANCZOS)
            
            # حفظ الصورة بجودة محسنة
            image.save(filepath, 'JPEG', quality=ImageHandler.IMAGE_QUALITY, optimize=True)
            
            # إرجاع المسار النسبي للصورة
            relative_path = f"/{filepath.replace(os.sep, '/')}"
            return relative_path, []
            
        except Exception as e:
            return None, [f'خطأ في معالجة الصورة: {str(e)}']
    
    @staticmethod
    def delete_image(image_path):
        """حذف صورة من الخادم"""
        try:
            if image_path and image_path.startswith('/static/'):
                # إزالة الشرطة المائلة الأولى
                file_path = image_path[1:]
                if os.path.exists(file_path):
                    os.remove(file_path)
                    return True
        except Exception as e:
            print(f"خطأ في حذف الصورة: {e}")
        return False
    
    @staticmethod
    def get_image_info(image_path):
        """الحصول على معلومات الصورة"""
        try:
            if image_path and image_path.startswith('/static/'):
                file_path = image_path[1:]
                if os.path.exists(file_path):
                    with Image.open(file_path) as img:
                        return {
                            'width': img.width,
                            'height': img.height,
                            'format': img.format,
                            'mode': img.mode,
                            'size': os.path.getsize(file_path)
                        }
        except Exception as e:
            print(f"خطأ في قراءة معلومات الصورة: {e}")
        return None