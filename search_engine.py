from typing import List, Dict, Any, Optional
from sqlalchemy import and_, or_, func
from models import Car, db
from utils import normalize_arabic, normalize_for_search, validate_search_criteria
import json

class CarSearchEngine:
    """محرك البحث المتقدم للسيارات"""
    
    def __init__(self):
        self.default_sort = 'price_asc'
        self.valid_sorts = {
            'price_asc': (Car.price, 'asc'),
            'price_desc': (Car.price, 'desc'),
            'year_desc': (Car.year, 'desc'),
            'year_asc': (Car.year, 'asc'),
            'name_asc': (Car.name, 'asc'),
            'name_desc': (Car.name, 'desc'),
            'mileage_asc': (Car.mileage, 'asc'),
            'mileage_desc': (Car.mileage, 'desc')
        }
    
    def search(self, criteria: Dict[str, Any], page: int = 1, per_page: int = 12,
               sort_by: Optional[str] = None) -> Dict[str, Any]:
        """
        البحث الرئيسي للسيارات
        """
        # التحقق من صحة المعايير
        validation_errors = validate_search_criteria(criteria)
        if validation_errors:
            return {
                'cars': [],
                'total': 0,
                'page': page,
                'per_page': per_page,
                'total_pages': 0,
                'errors': validation_errors
            }
        
        # بناء الاستعلام الأساسي
        query = Car.query.filter(Car.is_available == True)
        
        # تطبيق المرشحات
        query = self._apply_filters(query, criteria)
        
        # تطبيق الترتيب
        query = self._apply_sorting(query, sort_by or self.default_sort)
        
        # تطبيق التصفح
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return {
            'cars': [car.to_dict() for car in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'total_pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num,
            'errors': {}
        }
    
    def _apply_filters(self, query, criteria: Dict[str, Any]):
        """تطبيق المرشحات على الاستعلام"""
        
        # البحث النصي
        if criteria.get('search_text'):
            search_text = normalize_for_search(criteria['search_text'])
            text_filter = or_(
                Car.name_normalized.like(f'%{search_text}%'),  # type: ignore
                Car.brand_normalized.like(f'%{search_text}%'),  # type: ignore
                Car.model.contains(search_text)
            )
            query = query.filter(text_filter)
        
        # الميزانية
        if criteria.get('budget'):
            try:
                budget = float(criteria['budget'])
                query = query.filter(Car.price <= budget)
            except (ValueError, TypeError):
                pass
        
        # نطاق السعر
        if criteria.get('price_min'):
            try:
                price_min = float(criteria['price_min'])
                query = query.filter(Car.price >= price_min)
            except (ValueError, TypeError):
                pass
        
        if criteria.get('price_max'):
            try:
                price_max = float(criteria['price_max'])
                query = query.filter(Car.price <= price_max)
            except (ValueError, TypeError):
                pass
        
        # مستوى الأداء
        if criteria.get('performance_level'):
            query = query.filter(Car.performance_level == criteria['performance_level'])
        
        # نوع الوقود
        if criteria.get('fuel_type'):
            query = query.filter(Car.fuel_type == criteria['fuel_type'])
        
        # نوع القير
        if criteria.get('transmission'):
            query = query.filter(Car.transmission == criteria['transmission'])
        
        # نوع السيارة
        if criteria.get('car_type'):
            query = query.filter(Car.car_type == criteria['car_type'])
        
        # الماركة
        if criteria.get('brand'):
            brand_normalized = normalize_arabic(criteria['brand'])
            query = query.filter(Car.brand_normalized.like(f'%{brand_normalized}%'))  # type: ignore
        
        # سنة الصنع
        if criteria.get('year_from'):
            try:
                year_from = int(criteria['year_from'])
                query = query.filter(Car.year >= year_from)
            except (ValueError, TypeError):
                pass
        
        if criteria.get('year_to'):
            try:
                year_to = int(criteria['year_to'])
                query = query.filter(Car.year <= year_to)
            except (ValueError, TypeError):
                pass
        
        # عدد الأبواب
        if criteria.get('doors'):
            try:
                doors = int(criteria['doors'])
                query = query.filter(Car.doors == doors)
            except (ValueError, TypeError):
                pass
        
        # حجم المحرك
        if criteria.get('engine_size_min'):
            try:
                engine_min = float(criteria['engine_size_min'])
                query = query.filter(Car.engine_size >= engine_min)
            except (ValueError, TypeError):
                pass
        
        if criteria.get('engine_size_max'):
            try:
                engine_max = float(criteria['engine_size_max'])
                query = query.filter(Car.engine_size <= engine_max)
            except (ValueError, TypeError):
                pass
        
        # المسافة المقطوعة
        if criteria.get('mileage_max'):
            try:
                mileage_max = int(criteria['mileage_max'])
                query = query.filter(Car.mileage <= mileage_max)
            except (ValueError, TypeError):
                pass
        
        # اللون
        if criteria.get('color'):
            color_normalized = normalize_arabic(criteria['color'])
            query = query.filter(Car.color.contains(color_normalized))
        
        # بلد المنشأ
        if criteria.get('country_origin'):
            country_normalized = normalize_arabic(criteria['country_origin'])
            query = query.filter(Car.country_origin.contains(country_normalized))
        
        # الميزات الإضافية
        feature_filters = []
        
        if criteria.get('leather_seats'):
            feature_filters.append(Car.leather_seats == True)
        
        if criteria.get('sunroof'):
            feature_filters.append(Car.sunroof == True)
        
        if criteria.get('gps_system'):
            feature_filters.append(Car.gps_system == True)
        
        if criteria.get('backup_camera'):
            feature_filters.append(Car.backup_camera == True)
        
        if criteria.get('entertainment_system'):
            feature_filters.append(Car.entertainment_system == True)
        
        if criteria.get('safety_features'):
            feature_filters.append(Car.safety_features == True)
        
        if feature_filters:
            query = query.filter(and_(*feature_filters))
        
        return query
    
    def _apply_sorting(self, query, sort_by: str):
        """تطبيق الترتيب على الاستعلام"""
        if sort_by not in self.valid_sorts:
            sort_by = self.default_sort
        
        sort_column, sort_direction = self.valid_sorts[sort_by]
        
        if sort_direction == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        return query
    
    def get_filter_options(self) -> Dict[str, Any]:
        """الحصول على خيارات المرشحات المتاحة"""
        
        # الحصول على القيم الفريدة من قاعدة البيانات
        brands = db.session.query(Car.brand).distinct().all()
        car_types = db.session.query(Car.car_type).distinct().all()
        fuel_types = db.session.query(Car.fuel_type).distinct().all()
        transmissions = db.session.query(Car.transmission).distinct().all()
        performance_levels = db.session.query(Car.performance_level).distinct().all()
        colors = db.session.query(Car.color).distinct().all()
        countries = db.session.query(Car.country_origin).distinct().all()
        
        # الحصول على نطاقات السنوات والأسعار
        year_range = db.session.query(
            func.min(Car.year), 
            func.max(Car.year)
        ).first()
        
        price_range = db.session.query(
            func.min(Car.price), 
            func.max(Car.price)
        ).first()
        
        return {
            'brands': [brand[0] for brand in brands if brand[0]],
            'car_types': [car_type[0] for car_type in car_types if car_type[0]],
            'fuel_types': [fuel_type[0] for fuel_type in fuel_types if fuel_type[0]],
            'transmissions': [transmission[0] for transmission in transmissions if transmission[0]],
            'performance_levels': [level[0] for level in performance_levels if level[0]],
            'colors': [color[0] for color in colors if color[0]],
            'countries': [country[0] for country in countries if country[0]],
            'year_range': {
                'min': year_range[0] if year_range and year_range[0] else 2000,
                'max': year_range[1] if year_range and year_range[1] else 2024
            },
            'price_range': {
                'min': int(price_range[0]) if price_range and price_range[0] else 0,
                'max': int(price_range[1]) if price_range and price_range[1] else 50000
            },
            'doors_options': [2, 4, 5],
            'sort_options': [
                {'value': 'price_asc', 'label': 'السعر: من الأقل للأعلى'},
                {'value': 'price_desc', 'label': 'السعر: من الأعلى للأقل'},
                {'value': 'year_desc', 'label': 'السنة: الأحدث أولاً'},
                {'value': 'year_asc', 'label': 'السنة: الأقدم أولاً'},
                {'value': 'name_asc', 'label': 'الاسم: أ-ي'},
                {'value': 'name_desc', 'label': 'الاسم: ي-أ'},
                {'value': 'mileage_asc', 'label': 'المسافة: الأقل أولاً'},
                {'value': 'mileage_desc', 'label': 'المسافة: الأكثر أولاً'}
            ]
        }
    
    def get_similar_cars(self, car_id: int, limit: int = 4) -> List[Dict[str, Any]]:
        """الحصول على سيارات مشابهة"""
        car = Car.query.get(car_id)
        if not car:
            return []
        
        # البحث عن سيارات مشابهة بناءً على الماركة ونوع السيارة والسعر
        price_range = car.price * 0.3  # نطاق 30% من السعر
        
        similar_cars = Car.query.filter(
            and_(
                Car.id != car_id,
                Car.is_available == True,
                or_(
                    Car.brand == car.brand,
                    Car.car_type == car.car_type,
                    and_(
                        Car.price >= car.price - price_range,
                        Car.price <= car.price + price_range
                    )
                )
            )
        ).limit(limit).all()
        
        return [similar_car.to_dict() for similar_car in similar_cars]
    
    def get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """الحصول على اقتراحات البحث"""
        if not query or len(query) < 2:
            return []
        
        normalized_query = normalize_for_search(query)
        
        # البحث في أسماء السيارات والماركات
        suggestions = []
        
        # البحث في الماركات
        brands = db.session.query(Car.brand).filter(
            Car.brand_normalized.like(f'%{normalized_query}%')  # type: ignore
        ).distinct().limit(limit).all()
        
        suggestions.extend([brand[0] for brand in brands])
        
        # البحث في أسماء السيارات
        if len(suggestions) < limit:
            remaining = limit - len(suggestions)
            names = db.session.query(Car.name).filter(
                Car.name_normalized.like(f'%{normalized_query}%')  # type: ignore
            ).distinct().limit(remaining).all()
            
            suggestions.extend([name[0] for name in names])
        
        return suggestions[:limit]

# إنشاء مثيل عام من محرك البحث
search_engine = CarSearchEngine()