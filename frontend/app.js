// Configuration
const API_BASE_URL = 'https://your-railway-app.up.railway.app'; // Replace with your Railway API URL
let currentPage = 1;
let currentFilters = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadCars();
    loadFilters();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Search on Enter key
    document.getElementById('searchText').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchCars();
        }
    });
    
    // Filter change events
    ['brandFilter', 'fuelTypeFilter', 'transmissionFilter', 'carTypeFilter'].forEach(id => {
        document.getElementById(id).addEventListener('change', searchCars);
    });
}

// API Helper function
async function apiCall(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        showError('فشل في الاتصال بالخادم. يرجى المحاولة مرة أخرى.');
        throw error;
    }
}

// Load cars from API
async function loadCars(page = 1, filters = {}) {
    showLoading();
    hideError();
    
    try {
        // Build query parameters
        const params = new URLSearchParams({
            page: page,
            per_page: 12,
            ...filters
        });
        
        const data = await apiCall(`/api/cars?${params}`);
        displayCars(data.cars);
        displayPagination(data);
        currentPage = page;
        currentFilters = filters;
    } catch (error) {
        showError('فشل في تحميل السيارات');
    } finally {
        hideLoading();
    }
}

// Search cars
async function searchCars() {
    const filters = {
        search_text: document.getElementById('searchText').value,
        brand: document.getElementById('brandFilter').value,
        fuel_type: document.getElementById('fuelTypeFilter').value,
        transmission: document.getElementById('transmissionFilter').value,
        car_type: document.getElementById('carTypeFilter').value
    };
    
    // Remove empty filters
    Object.keys(filters).forEach(key => {
        if (!filters[key]) delete filters[key];
    });
    
    try {
        showLoading();
        hideError();
        
        const params = new URLSearchParams({
            page: 1,
            per_page: 12,
            ...filters
        });
        
        const data = await apiCall(`/api/search?${params}`);
        displayCars(data.cars);
        displayPagination(data);
        currentPage = 1;
        currentFilters = filters;
    } catch (error) {
        showError('فشل في البحث عن السيارات');
    } finally {
        hideLoading();
    }
}

// Load filter options
async function loadFilters() {
    try {
        const data = await apiCall('/api/filters');
        
        // Populate brand filter
        const brandSelect = document.getElementById('brandFilter');
        if (data.brands) {
            data.brands.forEach(brand => {
                const option = document.createElement('option');
                option.value = brand;
                option.textContent = brand;
                brandSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Failed to load filters:', error);
    }
}

// Display cars in grid
function displayCars(cars) {
    const grid = document.getElementById('carsGrid');
    
    if (!cars || cars.length === 0) {
        grid.innerHTML = `
            <div class="col-12 text-center text-white">
                <i class="fas fa-car fa-3x mb-3"></i>
                <h4>لا توجد سيارات متاحة</h4>
                <p>جرب تغيير معايير البحث</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = cars.map(car => `
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card car-card h-100">
                <img src="${car.image_url || '/static/images/cars/placeholder.jpg'}" 
                     class="card-img-top car-image" 
                     alt="${car.name}"
                     onerror="this.src='/static/images/cars/placeholder.jpg'">
                <div class="card-body d-flex flex-column">
                    <h5 class="card-title">${car.name}</h5>
                    <p class="card-text text-muted">
                        <i class="fas fa-calendar"></i> ${car.year} |
                        <i class="fas fa-gas-pump"></i> ${car.fuel_type} |
                        <i class="fas fa-cogs"></i> ${car.transmission}
                    </p>
                    <p class="card-text flex-grow-1">${car.description || 'وصف غير متوفر'}</p>
                    <div class="d-flex justify-content-between align-items-center mt-auto">
                        <span class="price-tag">${formatPrice(car.price)} ريال</span>
                        <button class="btn btn-primary btn-sm" onclick="showCarDetails(${car.id})">
                            <i class="fas fa-eye"></i> التفاصيل
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Display pagination
function displayPagination(data) {
    const pagination = document.getElementById('pagination');
    
    if (data.pages <= 1) {
        pagination.innerHTML = '';
        return;
    }
    
    let paginationHTML = '<nav><ul class="pagination">';
    
    // Previous button
    if (data.has_prev) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="loadCars(${data.page - 1}, currentFilters)">السابق</a>
            </li>
        `;
    }
    
    // Page numbers
    const startPage = Math.max(1, data.page - 2);
    const endPage = Math.min(data.pages, data.page + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <li class="page-item ${i === data.page ? 'active' : ''}">
                <a class="page-link" href="#" onclick="loadCars(${i}, currentFilters)">${i}</a>
            </li>
        `;
    }
    
    // Next button
    if (data.has_next) {
        paginationHTML += `
            <li class="page-item">
                <a class="page-link" href="#" onclick="loadCars(${data.page + 1}, currentFilters)">التالي</a>
            </li>
        `;
    }
    
    paginationHTML += '</ul></nav>';
    pagination.innerHTML = paginationHTML;
}

// Show car details in modal
async function showCarDetails(carId) {
    try {
        const data = await apiCall(`/api/cars/${carId}`);
        const car = data.car;
        
        document.getElementById('carModalTitle').textContent = car.name;
        document.getElementById('carModalBody').innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <img src="${car.image_url || '/static/images/cars/placeholder.jpg'}" 
                         class="img-fluid rounded" 
                         alt="${car.name}"
                         onerror="this.src='/static/images/cars/placeholder.jpg'">
                </div>
                <div class="col-md-6">
                    <h4>${car.name}</h4>
                    <p class="text-muted">${car.brand} ${car.model} - ${car.year}</p>
                    <h5 class="text-primary">${formatPrice(car.price)} ريال</h5>
                    
                    <hr>
                    
                    <div class="row">
                        <div class="col-6 mb-2">
                            <strong>نوع الوقود:</strong><br>
                            <span class="text-muted">${car.fuel_type}</span>
                        </div>
                        <div class="col-6 mb-2">
                            <strong>ناقل الحركة:</strong><br>
                            <span class="text-muted">${car.transmission}</span>
                        </div>
                        <div class="col-6 mb-2">
                            <strong>حجم المحرك:</strong><br>
                            <span class="text-muted">${car.engine_size} لتر</span>
                        </div>
                        <div class="col-6 mb-2">
                            <strong>عدد الأبواب:</strong><br>
                            <span class="text-muted">${car.doors}</span>
                        </div>
                        <div class="col-6 mb-2">
                            <strong>المسافة المقطوعة:</strong><br>
                            <span class="text-muted">${formatNumber(car.mileage)} كم</span>
                        </div>
                        <div class="col-6 mb-2">
                            <strong>اللون:</strong><br>
                            <span class="text-muted">${car.color}</span>
                        </div>
                    </div>
                    
                    <hr>
                    
                    <h6>الميزات:</h6>
                    <div class="row">
                        ${car.leather_seats ? '<div class="col-6"><i class="fas fa-check text-success"></i> مقاعد جلدية</div>' : ''}
                        ${car.sunroof ? '<div class="col-6"><i class="fas fa-check text-success"></i> فتحة سقف</div>' : ''}
                        ${car.gps_system ? '<div class="col-6"><i class="fas fa-check text-success"></i> نظام GPS</div>' : ''}
                        ${car.backup_camera ? '<div class="col-6"><i class="fas fa-check text-success"></i> كاميرا خلفية</div>' : ''}
                        ${car.entertainment_system ? '<div class="col-6"><i class="fas fa-check text-success"></i> نظام ترفيه</div>' : ''}
                        ${car.safety_features ? '<div class="col-6"><i class="fas fa-check text-success"></i> ميزات أمان</div>' : ''}
                    </div>
                    
                    ${car.description ? `<hr><p><strong>الوصف:</strong><br>${car.description}</p>` : ''}
                </div>
            </div>
            
            ${data.similar_cars && data.similar_cars.length > 0 ? `
                <hr>
                <h6>سيارات مشابهة:</h6>
                <div class="row">
                    ${data.similar_cars.map(similar => `
                        <div class="col-md-4 mb-3">
                            <div class="card">
                                <img src="${similar.image_url || '/static/images/cars/placeholder.jpg'}" 
                                     class="card-img-top" 
                                     style="height: 150px; object-fit: cover;"
                                     alt="${similar.name}">
                                <div class="card-body p-2">
                                    <h6 class="card-title">${similar.name}</h6>
                                    <p class="card-text small">${formatPrice(similar.price)} ريال</p>
                                    <button class="btn btn-sm btn-outline-primary" onclick="showCarDetails(${similar.id})">
                                        عرض التفاصيل
                                    </button>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('carModal'));
        modal.show();
    } catch (error) {
        showError('فشل في تحميل تفاصيل السيارة');
    }
}

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('ar-SA').format(price);
}

function formatNumber(number) {
    return new Intl.NumberFormat('ar-SA').format(number);
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('carsGrid').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('carsGrid').style.display = 'flex';
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').style.display = 'block';
}

function hideError() {
    document.getElementById('error').style.display = 'none';
}

function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({
        behavior: 'smooth'
    });
}

// Update API URL when Railway deployment is ready
function updateApiUrl(newUrl) {
    API_BASE_URL = newUrl;
    console.log('API URL updated to:', API_BASE_URL);
}