// متجر السيارات الذكي - ملف JavaScript الرئيسي

document.addEventListener('DOMContentLoaded', function() {
    
    // تهيئة التطبيق
    initializeApp();
    
    // تهيئة البحث التلقائي
    initializeSearch();
    
    // تهيئة المرشحات
    initializeFilters();
    
    // تهيئة المقارنة
    initializeComparison();
    
    // تهيئة لوحة الإدارة
    initializeAdmin();
    
    // تهيئة الرسوم المتحركة
    initializeAnimations();
});

// تهيئة التطبيق
function initializeApp() {
    // إخفاء التنبيهات تلقائياً
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('alert-success')) {
                fadeOut(alert);
            }
        });
    }, 3000);
    
    // تحسين تجربة المستخدم
    addLoadingStates();
    
    // تهيئة التلميحات
    initializeTooltips();
}

// تهيئة البحث التلقائي
function initializeSearch() {
    const searchInput = document.getElementById('search_text');
    const suggestionsContainer = document.getElementById('search-suggestions');
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length >= 2) {
                searchTimeout = setTimeout(() => {
                    fetchSearchSuggestions(query, suggestionsContainer);
                }, 300);
            } else {
                hideSuggestions(suggestionsContainer);
            }
        });
        
        // إخفاء الاقتراحات عند النقر خارجها
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !suggestionsContainer?.contains(e.target)) {
                hideSuggestions(suggestionsContainer);
            }
        });
    }
}

// جلب اقتراحات البحث
async function fetchSearchSuggestions(query, container) {
    if (!container) return;
    
    try {
        const response = await fetch(`/api/search_suggestions?q=${encodeURIComponent(query)}`);
        const suggestions = await response.json();
        
        displaySuggestions(suggestions, container, query);
    } catch (error) {
        console.error('خطأ في جلب الاقتراحات:', error);
    }
}

// عرض اقتراحات البحث
function displaySuggestions(suggestions, container, query) {
    if (!container || !suggestions.length) {
        hideSuggestions(container);
        return;
    }
    
    const html = suggestions.map(suggestion => `
        <div class="suggestion-item" onclick="selectSuggestion('${suggestion}')">
            <i class="bi bi-search me-2"></i>
            ${highlightMatch(suggestion, query)}
        </div>
    `).join('');
    
    container.innerHTML = html;
    container.style.display = 'block';
}

// إخفاء الاقتراحات
function hideSuggestions(container) {
    if (container) {
        container.style.display = 'none';
    }
}

// اختيار اقتراح
function selectSuggestion(suggestion) {
    const searchInput = document.getElementById('search_text');
    if (searchInput) {
        searchInput.value = suggestion;
        hideSuggestions(document.getElementById('search-suggestions'));
        // تشغيل البحث تلقائياً
        searchInput.closest('form')?.submit();
    }
}

// تمييز النص المطابق
function highlightMatch(text, query) {
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<strong>$1</strong>');
}

// تهيئة المرشحات
function initializeFilters() {
    // تحديث المرشحات التفاعلية
    const priceRange = document.getElementById('price-range');
    const priceDisplay = document.getElementById('price-display');
    
    if (priceRange && priceDisplay) {
        priceRange.addEventListener('input', function() {
            priceDisplay.textContent = formatPrice(this.value);
        });
    }
    
    // مرشح السنة
    const yearRange = document.getElementById('year-range');
    const yearDisplay = document.getElementById('year-display');
    
    if (yearRange && yearDisplay) {
        yearRange.addEventListener('input', function() {
            yearDisplay.textContent = this.value;
        });
    }
    
    // إعادة تعيين المرشحات
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', function() {
            resetAllFilters();
        });
    }
}

// إعادة تعيين جميع المرشحات
function resetAllFilters() {
    const form = document.querySelector('.search-form');
    if (form) {
        form.reset();
        // إعادة تحميل الصفحة بدون معايير البحث
        window.location.href = window.location.pathname;
    }
}

// تهيئة المقارنة
function initializeComparison() {
    const compareButtons = document.querySelectorAll('.compare-btn');
    const compareList = getCompareList();
    
    // تحديث حالة الأزرار
    updateCompareButtons(compareList);
    
    compareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const carId = this.dataset.carId;
            toggleCompare(carId);
        });
    });
    
    // زر عرض المقارنة
    const viewCompareBtn = document.getElementById('view-compare');
    if (viewCompareBtn) {
        viewCompareBtn.addEventListener('click', function() {
            const compareList = getCompareList();
            if (compareList.length >= 2) {
                window.location.href = `/compare?cars=${compareList.join('&cars=')}`;
            } else {
                showAlert('يجب اختيار سيارتين على الأقل للمقارنة', 'warning');
            }
        });
    }
}

// إضافة/إزالة سيارة من المقارنة
function toggleCompare(carId) {
    let compareList = getCompareList();
    const index = compareList.indexOf(carId);
    
    if (index > -1) {
        compareList.splice(index, 1);
        showAlert('تم إزالة السيارة من المقارنة', 'info');
    } else {
        if (compareList.length >= 4) {
            showAlert('يمكن مقارنة 4 سيارات كحد أقصى', 'warning');
            return;
        }
        compareList.push(carId);
        showAlert('تم إضافة السيارة للمقارنة', 'success');
    }
    
    setCompareList(compareList);
    updateCompareButtons(compareList);
    updateCompareCounter(compareList.length);
}

// الحصول على قائمة المقارنة
function getCompareList() {
    const stored = localStorage.getItem('compareList');
    return stored ? JSON.parse(stored) : [];
}

// حفظ قائمة المقارنة
function setCompareList(list) {
    localStorage.setItem('compareList', JSON.stringify(list));
}

// تحديث أزرار المقارنة
function updateCompareButtons(compareList) {
    const compareButtons = document.querySelectorAll('.compare-btn');
    compareButtons.forEach(button => {
        const carId = button.dataset.carId;
        const isInCompare = compareList.includes(carId);
        
        button.classList.toggle('btn-success', isInCompare);
        button.classList.toggle('btn-outline-primary', !isInCompare);
        button.innerHTML = isInCompare ? 
            '<i class="bi bi-check-circle me-1"></i> مضافة للمقارنة' : 
            '<i class="bi bi-plus-circle me-1"></i> أضف للمقارنة';
    });
}

// تحديث عداد المقارنة
function updateCompareCounter(count) {
    const counter = document.getElementById('compare-counter');
    if (counter) {
        counter.textContent = count;
        counter.style.display = count > 0 ? 'inline' : 'none';
    }
}

// تهيئة لوحة الإدارة
function initializeAdmin() {
    // تأكيد الحذف
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('هل أنت متأكد من حذف هذا العنصر؟')) {
                e.preventDefault();
            }
        });
    });
    
    // معاينة الصورة
    const imageInputs = document.querySelectorAll('input[type="url"][name="image_url"]');
    imageInputs.forEach(input => {
        input.addEventListener('blur', function() {
            previewImage(this.value, this);
        });
    });
    
    // التحقق من صحة النموذج
    const adminForms = document.querySelectorAll('.admin-form');
    adminForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateAdminForm(this)) {
                e.preventDefault();
            }
        });
    });
}

// معاينة الصورة
function previewImage(url, input) {
    if (!url) return;
    
    const preview = document.getElementById('image-preview') || createImagePreview(input);
    const img = preview.querySelector('img');
    
    img.src = url;
    img.onload = function() {
        preview.style.display = 'block';
    };
    img.onerror = function() {
        preview.style.display = 'none';
        showAlert('رابط الصورة غير صحيح', 'warning');
    };
}

// إنشاء معاينة الصورة
function createImagePreview(input) {
    const preview = document.createElement('div');
    preview.id = 'image-preview';
    preview.className = 'mt-2';
    preview.style.display = 'none';
    preview.innerHTML = `
        <img src="" alt="معاينة الصورة" class="img-thumbnail" style="max-width: 200px; max-height: 150px;">
    `;
    input.parentNode.appendChild(preview);
    return preview;
}

// التحقق من صحة نموذج الإدارة
function validateAdminForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        showAlert('يرجى ملء جميع الحقول المطلوبة', 'danger');
    }
    
    return isValid;
}

// تهيئة الرسوم المتحركة
function initializeAnimations() {
    // رسوم متحركة عند التمرير
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // مراقبة العناصر
    const animatedElements = document.querySelectorAll('.card, .stat-card, .car-card');
    animatedElements.forEach(el => observer.observe(el));
}

// إضافة حالات التحميل
function addLoadingStates() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>جاري التحميل...';
            }
        });
    });
}

// تهيئة التلميحات
function initializeTooltips() {
    // تهيئة Bootstrap tooltips إذا كانت متوفرة
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// عرض تنبيه
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container') || createAlertContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alert);
    
    // إزالة التنبيه تلقائياً
    setTimeout(() => {
        fadeOut(alert);
    }, 5000);
}

// إنشاء حاوية التنبيهات
function createAlertContainer() {
    const container = document.createElement('div');
    container.id = 'alert-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '9999';
    document.body.appendChild(container);
    return container;
}

// تأثير الاختفاء التدريجي
function fadeOut(element) {
    element.style.transition = 'opacity 0.5s';
    element.style.opacity = '0';
    setTimeout(() => {
        element.remove();
    }, 500);
}

// تنسيق السعر
function formatPrice(price) {
    return new Intl.NumberFormat('ar-KW', {
        style: 'currency',
        currency: 'KWD'
    }).format(price);
}

// تنسيق الأرقام
function formatNumber(number) {
    return new Intl.NumberFormat('ar-KW').format(number);
}

// البحث المتقدم
function toggleAdvancedSearch() {
    const advancedSection = document.getElementById('advanced-search');
    if (advancedSection) {
        advancedSection.style.display = 
            advancedSection.style.display === 'none' ? 'block' : 'none';
    }
}

// تصدير البيانات (للإدارة)
function exportData(format) {
    const url = `/admin/export?format=${format}`;
    window.open(url, '_blank');
}

// طباعة التقرير
function printReport() {
    window.print();
}

// تحديث الإحصائيات في الوقت الفعلي
function updateStats() {
    fetch('/admin/api/stats')
        .then(response => response.json())
        .then(data => {
            updateStatCards(data);
        })
        .catch(error => {
            console.error('خطأ في تحديث الإحصائيات:', error);
        });
}

// تحديث بطاقات الإحصائيات
function updateStatCards(data) {
    Object.keys(data).forEach(key => {
        const element = document.getElementById(`stat-${key}`);
        if (element) {
            animateNumber(element, data[key]);
        }
    });
}

// تحريك الأرقام
function animateNumber(element, targetValue) {
    const startValue = parseInt(element.textContent) || 0;
    const duration = 1000;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = Math.floor(startValue + (targetValue - startValue) * progress);
        element.textContent = formatNumber(currentValue);
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// تحديث الإحصائيات كل 30 ثانية في لوحة الإدارة
if (window.location.pathname.includes('/admin/dashboard')) {
    setInterval(updateStats, 30000);
}