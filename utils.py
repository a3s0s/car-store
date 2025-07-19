import re
from typing import Dict, List, Any

def normalize_arabic(text: str) -> str:
    """
    تطبيع النص العربي لتحسين البحث والمقارنة
    """
    if not text:
        return ""
    
    # إزالة التشكيل
    text = re.sub(r'[ًٌٍَُِّْٰ]', '', text)
    
    # توحيد الألف
    text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
    
    # توحيد الياء
    text = text.replace('ى', 'ي')
    
    # توحيد التاء المربوطة
    text = text.replace('ة', 'ه')
    
    # إزالة المسافات الزائدة
    text = re.sub(r'\s+', ' ', text.strip())
    
    return text.lower()

def normalize_for_search(text: str) -> str:
    """
    تطبيع النص للبحث (إزالة المسافات أيضاً)
    """
    normalized = normalize_arabic(text)
    return normalized.replace(' ', '')

def create_search_terms(text: str) -> List[str]:
    """
    إنشاء مصطلحات بحث متعددة للنص
    """
    terms = []
    
    # النص الأصلي
    terms.append(text.strip())
    
    # النص المطبع
    normalized = normalize_arabic(text)
    if normalized not in terms:
        terms.append(normalized)
    
    # النص المطبع بدون مسافات
    no_spaces = normalize_for_search(text)
    if no_spaces not in terms:
        terms.append(no_spaces)
    
    # الكلمات المنفردة
    words = text.split()
    for word in words:
        normalized_word = normalize_arabic(word)
        if len(normalized_word) > 2 and normalized_word not in terms:
            terms.append(normalized_word)
    
    return [term for term in terms if term]

def format_price(price: float) -> str:
    """
    تنسيق السعر بالدينار الكويتي
    """
    return f"{price:,.0f} د.ك"

def get_performance_level_ar(level: str) -> str:
    """
    ترجمة مستوى الأداء للعربية
    """
    levels = {
        'low': 'منخفض',
        'medium': 'متوسط',
        'high': 'عالي'
    }
    return levels.get(level.lower(), level)

def get_fuel_type_ar(fuel_type: str) -> str:
    """
    ترجمة نوع الوقود للعربية
    """
    types = {
        'gasoline': 'بنزين',
        'diesel': 'ديزل',
        'hybrid': 'هجين',
        'electric': 'كهربائي'
    }
    return types.get(fuel_type.lower(), fuel_type)

def get_transmission_ar(transmission: str) -> str:
    """
    ترجمة نوع الجير للعربية
    """
    types = {
        'manual': 'عادي',
        'automatic': 'أوتوماتيك',
        'cvt': 'CVT'
    }
    return types.get(transmission.lower(), transmission)

def get_car_type_ar(car_type: str) -> str:
    """
    ترجمة نوع السيارة للعربية
    """
    types = {
        'sedan': 'سيدان',
        'suv': 'SUV',
        'hatchback': 'هاتشباك',
        'coupe': 'كوبيه',
        'convertible': 'مكشوفة',
        'pickup': 'بيك أب',
        'van': 'فان'
    }
    return types.get(car_type.lower(), car_type)

def validate_search_criteria(criteria: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    التحقق من صحة معايير البحث
    """
    errors = {}
    
    # التحقق من الميزانية
    if 'budget' in criteria:
        try:
            budget = float(criteria['budget'])
            if budget < 0:
                errors['budget'] = ['الميزانية يجب أن تكون أكبر من الصفر']
        except (ValueError, TypeError):
            errors['budget'] = ['الميزانية يجب أن تكون رقماً صحيحاً']
    
    # التحقق من سنة الصنع
    if 'year_from' in criteria or 'year_to' in criteria:
        try:
            year_from = int(criteria.get('year_from', 1900))
            year_to = int(criteria.get('year_to', 2030))
            
            if year_from > year_to:
                errors['year'] = ['سنة البداية يجب أن تكون أقل من سنة النهاية']
            
            if year_from < 1900 or year_to > 2030:
                errors['year'] = ['سنة الصنع يجب أن تكون بين 1900 و 2030']
                
        except (ValueError, TypeError):
            errors['year'] = ['سنة الصنع يجب أن تكون رقماً صحيحاً']
    
    return errors