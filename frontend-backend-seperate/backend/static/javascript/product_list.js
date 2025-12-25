// ===========================
// PRODUCTS PAGE FUNCTIONALITY WITH PAGINATION
// ===========================

// 🚫 Do NOT run product list logic on product detail page
(function () {

// 🚫 Do NOT run on product detail page
if (document.querySelector('script[src*="product_detail.js"]')) {
  console.log("⛔ product_list.js skipped on product detail page");
  return;
}






console.log("🚀 ProductsManager loaded");

const NO_SERIES_CATEGORIES = [
    "memory",
    "networking",
    "docking-station"
];


class ProductsManager {
    constructor() {
        this.allProducts = [];
        this.filteredProducts = [];
        this.activeFilters = {
            category: [],
            brand: [],
            application: [],
            cores: [],
            tech: [],
            socket: [],
            maxPrice: 5000000000
        };
        this.sortBy = 'relevance';
        this.currentPage = 1;
        this.productsPerPage = 9;
        this.pagination = null;
        
        // Parse clean URLs
        this.selectedCategory = null;
        this.selectedSubCategory = null;
        this.selectedSeries = null;
        
        this.init();
    }

    init() {
        this.parseCleanURL();
        this.cacheElements();
        this.attachEventListeners();
        this.loadProducts();
    }

    parseCleanURL() {
    const pathParts = window.location.pathname.split("/").filter(Boolean);
    
    if (pathParts[0] === "products") {
        this.selectedCategory = pathParts[1]?.toLowerCase() || null;
        this.selectedSubCategory = pathParts[2]?.toLowerCase() || null;

        if (
            pathParts.length >= 4 &&
            !NO_SERIES_CATEGORIES.includes(this.selectedCategory)
        ) {
            this.selectedSeries = pathParts[3]?.toLowerCase() || null;
        } else {
            this.selectedSeries = null;
        }
    }
    
    console.log("📍 Category:", this.selectedCategory);
    console.log("📍 SubCategory:", this.selectedSubCategory);
    console.log("📍 Series:", this.selectedSeries);
}

    cacheElements() {
    this.productsGrid = document.getElementById('products-grid');
    this.noResults = document.getElementById('no-results');
    this.resultCount = document.getElementById('result-count');
    this.sortSelect = document.getElementById('sort-select');
    this.filterCheckboxes = document.querySelectorAll('.filter-checkbox');
    this.priceRange = document.getElementById('price-range');
    this.priceValue = document.getElementById('price-value');
    this.resetBtn = document.getElementById('reset-filters-btn');
    this.filterToggleBtn = document.getElementById('filter-toggle-btn');
    this.closeFiltersBtn = document.getElementById('close-filters-btn');
    this.filtersSidebar = document.getElementById('filters-sidebar');
    this.filterTitles = document.querySelectorAll('.filter-title');
    this.paginationContainer = document.getElementById('pagination');
    this.sidebarBackdrop = document.getElementById('sidebar-backdrop');
    this.seriesFilterContainer = document.getElementById('series-filter-options'); // ✅ ADD THIS LINE
}

    attachEventListeners() {
        this.filterCheckboxes.forEach(cb => {
            cb.addEventListener('change', () => this.handleFilterChange());
        });

        if (this.priceRange) {
            this.priceRange.addEventListener('input', e => this.handlePriceChange(e));
        }

        if (this.sortSelect) {
            this.sortSelect.addEventListener('change', e => this.handleSortChange(e));
        }

        if (this.resetBtn) {
            this.resetBtn.addEventListener('click', () => this.resetAllFilters());
        }

        if (this.filterToggleBtn) {
            this.filterToggleBtn.addEventListener('click', () => this.toggleFiltersSidebar());
        }

        if (this.closeFiltersBtn) {
            this.closeFiltersBtn.addEventListener('click', () => this.toggleFiltersSidebar());
        }

        if (this.sidebarBackdrop) {
            this.sidebarBackdrop.addEventListener('click', () => this.toggleFiltersSidebar());
        }

        this.filterTitles.forEach(title => {
            title.addEventListener('click', e => {
                const group = e.currentTarget.closest('.filter-group');
                if (group) group.classList.toggle('collapsed');
            });
        });

        document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && this.filtersSidebar && this.filtersSidebar.classList.contains('open')) {
                this.toggleFiltersSidebar();
            }
        });
    }

    loadProducts() {
        if (!this.productsGrid) {
            console.error("❌ Products grid not found");
            return;
        }

        this.productsGrid.innerHTML = `<div class="loading-state"><div class="loader"></div><p>Loading products...</p></div>`;

        fetch('/api/products/all')
            .then(res => {
                if (!res.ok) throw new Error('API error');
                return res.json();
            })
            .then(data => {
                if (data.success && Array.isArray(data.products)) {
                    this.allProducts = data.products.map(p => ({
                        ...p,
                        price: parseFloat(p.price) || 0,
                        cores: parseInt(p.cores) || 0,
                        threads: parseInt(p.threads) || 0,
                        base_freq: parseFloat(p.base_freq) || 0,
                        tdp: parseInt(p.tdp) || 0,
                        category: (p.category_key || p.category || "").toLowerCase().trim(),
                        sub_category: (p.sub_category || "").toLowerCase().trim(),
                        series: (p.series || "").toLowerCase().trim(),
                        tech: (p.tech || "").toLowerCase().trim(),
                        socket: (p.socket || "").toLowerCase().trim(),
                        brand: (p.brand || "").toLowerCase().trim()
                    }));

                    console.log("✅ Loaded", this.allProducts.length, "products");
                    this.applyURLFilters();
                } else {
                    throw new Error('Invalid API response');
                }
            })
            .catch(err => {
                console.warn('⚠️ API failed:', err);
                this.showNoResults();
            });
    }

    // ===== IN applyURLFilters() method =====
applyURLFilters() {
    this.filteredProducts = this.allProducts.filter(p => {
        if (this.selectedCategory && p.category !== this.selectedCategory)
            return false;

        if (this.selectedSubCategory && p.sub_category !== this.selectedSubCategory)
            return false;

        if (
            this.selectedSeries &&
            !NO_SERIES_CATEGORIES.includes(this.selectedCategory) &&
            p.series !== this.selectedSeries
        ) {
            return false;
        }

        return true;
    });

    console.log(
        "🔍 After URL filters:",
        this.filteredProducts.length,
        "products"
    );

    this.populateSeriesFilter(); // ✅ ADD THIS LINE
    
    this.currentPage = 1;
    this.initializePagination();
    this.displayProducts();
}

    handleFilterChange() {
        this.currentPage = 1;
        this.updateActiveFilters();
        this.applyFilters();
    }

    updateActiveFilters() {
        this.activeFilters = {
            category: [],
            brand: [],
            application: [],
            cores: [],
            tech: [],
            socket: [],
            maxPrice: this.priceRange ? parseInt(this.priceRange.value) : 5000000000
        };

        this.filterCheckboxes.forEach(cb => {
            if (cb.checked && cb.dataset.filter) {
                this.activeFilters[cb.dataset.filter].push(cb.value);
            }
        });
    }

    handlePriceChange(e) {
        const price = parseInt(e.target.value);
        if (this.priceValue) {
            this.priceValue.textContent = '$' + price.toLocaleString();
        }
        this.activeFilters.maxPrice = price;
        this.currentPage = 1;
        this.applyFilters();
    }

    handleSortChange(e) {
        this.sortBy = e.target.value;
        this.currentPage = 1;
        this.applySorting();
        this.initializePagination();
        this.displayProducts();
    }

    applyFilters() {
    // FIXED: Start from allProducts, not filteredProducts to avoid double-filtering
    this.filteredProducts = this.allProducts.filter(product => {
        // Apply URL category filters first
        if (this.selectedCategory && product.category !== this.selectedCategory)
            return false;

        if (this.selectedSubCategory && product.sub_category !== this.selectedSubCategory)
            return false;

        // Apply series filter only for 4-level categories
        if (
            this.selectedSeries &&
            !NO_SERIES_CATEGORIES.includes(this.selectedCategory) &&
            product.series !== this.selectedSeries
        ) {
            return false;
        }

        // Apply user-selected filters
        if (this.activeFilters.category.length && !this.activeFilters.category.includes(product.category)) return false;
        if (this.activeFilters.brand.length && !this.activeFilters.brand.includes(product.brand)) return false;
        if (this.activeFilters.application.length && !this.activeFilters.application.includes(product.application)) return false;
        if (this.activeFilters.tech.length && !this.activeFilters.tech.includes(product.tech)) return false;
        if (this.activeFilters.socket.length && !this.activeFilters.socket.includes(product.socket)) return false;

        if (this.activeFilters.cores.length) {
            const c = product.cores;
            const match = this.activeFilters.cores.some(r => {
                if (r === '0-8') return c <= 8;
                if (r === '9-16') return c >= 9 && c <= 16;
                if (r === '17-32') return c >= 17 && c <= 32;
                if (r === '33-64') return c >= 33 && c <= 64;
                if (r === '65+') return c >= 65;
                return false;
            });
            if (!match) return false;
        }

        if (product.price > this.activeFilters.maxPrice) return false;
        return true;
    });

    this.applySorting();
    this.initializePagination();
    this.displayProducts();
}

    applySorting() {
        if (this.sortBy === 'price-low-high') {
            this.filteredProducts.sort((a, b) => a.price - b.price);
        } else if (this.sortBy === 'price-high-low') {
            this.filteredProducts.sort((a, b) => b.price - a.price);
        } else if (this.sortBy === 'cores-high-low') {
            this.filteredProducts.sort((a, b) => b.cores - a.cores);
        } else if (this.sortBy === 'newest') {
            this.filteredProducts.sort((a, b) => b.id.localeCompare(a.id));
        }
    }

    initializePagination() {
        const totalPages = Math.ceil(this.filteredProducts.length / this.productsPerPage);
        
        if (this.pagination) {
            this.pagination.updateTotalPages(totalPages);
            this.pagination.currentPage = this.currentPage;
        } else {
            this.pagination = new ProductPagination(
                totalPages, 
                this.currentPage, 
                (page) => this.goToPage(page)
            );
        }
    }

    goToPage(page) {
        this.currentPage = page;
        this.displayProducts();
        
        window.scrollTo({ 
            top: 0, 
            behavior: 'smooth' 
        });
    }

    displayProducts() {
        if (!this.productsGrid) return;

        this.productsGrid.innerHTML = '';

        if (!this.filteredProducts.length) {
            this.showNoResults();
            this.updateResultCount();
            this.updateResultsInfo();
            if (this.pagination) {
                this.pagination.hide();
            }
            return;
        }

        if (this.noResults) this.noResults.style.display = 'none';

        const startIndex = (this.currentPage - 1) * this.productsPerPage;
        const endIndex = startIndex + this.productsPerPage;
        const pageProducts = this.filteredProducts.slice(startIndex, endIndex);

        pageProducts.forEach(p => {
            this.productsGrid.appendChild(this.createProductCard(p));
        });

        this.updateResultCount();
        this.updateResultsInfo();
        
        if (this.pagination) {
            this.pagination.show();
            this.pagination.render();
        }
    }

    createProductCard(product) {
    const card = document.createElement('div');
    card.className = 'product-card';

    const priceFormatted = product.price.toLocaleString('en-US');

    // ✅ IMAGE URL OR SVG FALLBACK
    const imageUrl = product.image || 
      "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='200'%3E%3Crect width='100%25' height='100%25' fill='%23e5e7eb'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' fill='%236b7280' font-size='16'%3ENo Image%3C/text%3E%3C/svg%3E";

    let productUrl;

    // ✅ For 2-level categories (memory, networking, docking-station)
    if (NO_SERIES_CATEGORIES.includes(product.category)) {
        productUrl = `/products/${product.category}/${product.sub_category}/${product.id}`;
    }
    // ✅ For 4-level categories with series
    else {
        productUrl = `/products/${product.category}/${product.sub_category}/${product.series}/${product.id}`;
    }

    // ✅ HTML TEMPLATE
    card.innerHTML = `
        <a href="${productUrl}" class="product-card-link">
            <div class="product-image">
                <img src="${imageUrl}" alt="${product.name}">
                <span class="product-badge">
                    ${(product.category || '').substring(0, 3).toUpperCase()}
                </span>
            </div>
            <div class="product-content">
                <div class="product-category">${product.category}</div>
                <div class="product-name">${product.name}</div>
            </div>
            <div class="product-footer">
                <div class="product-price">$${priceFormatted}</div>
                <span class="btn-view">View</span>
            </div>
        </a>
    `;

    return card;
}



    showNoResults() {
        if (this.noResults) this.noResults.style.display = 'block';
        this.productsGrid.innerHTML = '';
    }

    updateResultCount() {
        if (this.resultCount) {
            const count = this.filteredProducts.length;
            const text = count === 1 ? 'product' : 'products';
            this.resultCount.textContent = `${count} ${text}`;
        }
    }

    updateResultsInfo() {
        const showingStart = document.getElementById('showing-start');
        const showingEnd = document.getElementById('showing-end');
        const totalResults = document.getElementById('total-results');
        const resultsInfo = document.querySelector('.results-info');
        
        if (showingStart && showingEnd && totalResults && resultsInfo) {
            const total = this.filteredProducts.length;
            
            if (total === 0) {
                resultsInfo.style.display = 'none';
            } else {
                resultsInfo.style.display = 'block';
                
                const start = (this.currentPage - 1) * this.productsPerPage + 1;
                const end = Math.min(this.currentPage * this.productsPerPage, total);
                
                showingStart.textContent = start;
                showingEnd.textContent = end;
                totalResults.textContent = total;
            }
        }
    }

    resetAllFilters() {
        this.filterCheckboxes.forEach(cb => cb.checked = false);
        if (this.priceRange) this.priceRange.value = 50000;
        if (this.priceValue) this.priceValue.textContent = '$50,000';
        if (this.sortSelect) this.sortSelect.value = 'relevance';

        this.activeFilters = {
            category: [],
            brand: [],
            application: [],
            cores: [],
            tech: [],
            socket: [],
            maxPrice: 50000
        };

        this.sortBy = 'relevance';
        this.currentPage = 1;

        this.applyURLFilters();
    }

    toggleFiltersSidebar() {
        if (!this.filtersSidebar) return;
        this.filtersSidebar.classList.toggle('open');
        if (this.sidebarBackdrop) {
            this.sidebarBackdrop.classList.toggle('active');
        }
        document.body.style.overflow = this.filtersSidebar.classList.contains('open') ? 'hidden' : '';
    }

    // ✅ ADD THESE 3 NEW METHODS HERE ✅
    
    detectAvailableSeries() {
        if (!this.selectedCategory || !this.selectedSubCategory) return [];
        
        const seriesSet = new Set();
        this.allProducts.forEach(p => {
            if (p.category === this.selectedCategory && 
                p.sub_category === this.selectedSubCategory && 
                p.series) {
                seriesSet.add(p.series);
            }
        });
        
        return Array.from(seriesSet).sort();
    }

    populateSeriesFilter() {
        if (!this.seriesFilterContainer) return;
        
        const availableSeries = this.detectAvailableSeries();
        
        const seriesFilterGroup = document.getElementById('series-filter-group');
        if (NO_SERIES_CATEGORIES.includes(this.selectedCategory) || availableSeries.length === 0) {
            if (seriesFilterGroup) seriesFilterGroup.style.display = 'none';
            return;
        }
        
        if (seriesFilterGroup) seriesFilterGroup.style.display = 'block';
        
        this.seriesFilterContainer.innerHTML = '';
        
        availableSeries.forEach(series => {
            const isActive = this.selectedSeries === series;
            
            const label = document.createElement('label');
            label.className = 'checkbox-label series-chip';
            if (isActive) label.classList.add('active');
            
            const seriesName = series.split('-').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
            ).join(' ');
            
            label.innerHTML = `
                <input type="checkbox" 
                       class="filter-checkbox series-filter" 
                       data-filter="series" 
                       value="${series}"
                       ${isActive ? 'checked' : ''}>
                <span class="checkmark"></span>
                <span>${seriesName}</span>
            `;
            
            label.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateToSeries(series);
            });
            
            this.seriesFilterContainer.appendChild(label);
        });
    }

    navigateToSeries(series) {
        const newUrl = `/products/${this.selectedCategory}/${this.selectedSubCategory}/${series}`;
        window.location.href = newUrl;
    }
}  // ← Keep this closing brace for ProductsManager class

// ===========================
// PAGINATION CLASS
// ===========================

class ProductPagination {
    constructor(totalPages, currentPage = 1, onPageChange) {
        this.totalPages = totalPages;
        this.currentPage = currentPage;
        this.onPageChange = onPageChange;
        this.container = document.getElementById('pagination');
        this.paginationSection = document.getElementById('pagination-section');
        this.render();
    }

    updateTotalPages(totalPages) {
        this.totalPages = totalPages;
        if (this.currentPage > totalPages && totalPages > 0) {
            this.currentPage = 1;
        }
        this.render();
    }

    show() {
        if (this.paginationSection) {
            this.paginationSection.style.display = 'block';
        }
    }

    hide() {
        if (this.paginationSection) {
            this.paginationSection.style.display = 'none';
        }
    }

    render() {
        if (!this.container) return;
        
        if (this.totalPages <= 1) {
            this.hide();
            return;
        }

        this.show();
        this.container.innerHTML = '';
        
        this.container.appendChild(
            this.createButton('←', 'nav-btn', this.currentPage === 1, 
            () => this.goToPage(this.currentPage - 1))
        );

        const pages = this.calculatePageNumbers();
        pages.forEach(page => {
            if (page === '...') {
                this.container.appendChild(this.createDots());
            } else {
                this.container.appendChild(
                    this.createButton(
                        page,
                        page === this.currentPage ? 'active' : '',
                        false,
                        () => this.goToPage(page)
                    )
                );
            }
        });

        this.container.appendChild(
            this.createButton('→', 'nav-btn', this.currentPage === this.totalPages, 
            () => this.goToPage(this.currentPage + 1))
        );

        const currentPageDisplay = document.getElementById('current-page-display');
        const totalPagesDisplay = document.getElementById('total-pages-display');
        
        if (currentPageDisplay) currentPageDisplay.textContent = this.currentPage;
        if (totalPagesDisplay) totalPagesDisplay.textContent = this.totalPages;
    }

    createButton(text, className = '', disabled = false, onClick = null) {
        const btn = document.createElement('button');
        btn.className = `page-btn ${className}`;
        btn.innerHTML = `<span>${text}</span>`;
        btn.disabled = disabled;
        if (onClick) btn.onclick = onClick;
        return btn;
    }

    createDots() {
        const dots = document.createElement('div');
        dots.className = 'dots';
        dots.textContent = '⋯';
        return dots;
    }

    calculatePageNumbers() {
        const pages = [];
        const showPages = 7;
        
        if (this.totalPages <= showPages) {
            for (let i = 1; i <= this.totalPages; i++) {
                pages.push(i);
            }
        } else {
            pages.push(1);

            let start = Math.max(2, this.currentPage - 1);
            let end = Math.min(this.totalPages - 1, this.currentPage + 1);

            if (this.currentPage <= 3) {
                end = 4;
            }

            if (this.currentPage >= this.totalPages - 2) {
                start = this.totalPages - 3;
            }

            if (start > 2) {
                pages.push('...');
            }

            for (let i = start; i <= end; i++) {
                pages.push(i);
            }

            if (end < this.totalPages - 1) {
                pages.push('...');
            }

            pages.push(this.totalPages);
        }

        return pages;
    }

    goToPage(page) {
        if (page < 1 || page > this.totalPages || page === this.currentPage) return;
        this.currentPage = page;
        this.render();
        
        if (this.onPageChange) {
            this.onPageChange(page);
        }
    }
}
    // Add this to the cacheElements() method
// ===========================
// INITIALIZE
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 ProductsManager initialized");
    new ProductsManager();
});
})();
