// ===========================
// PRODUCTS PAGE FUNCTIONALITY
// ===========================

console.log("🚀 ProductsManager loaded");

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
            maxPrice: 50000
        };
        this.sortBy = 'relevance';
        this.currentPage = 1;
        this.productsPerPage = 12;
        
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
            this.selectedSeries = pathParts[3]?.toLowerCase() || null;
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

        this.filterTitles.forEach(title => {
            title.addEventListener('click', e => {
                const group = e.currentTarget.closest('.filter-group');
                if (group) group.classList.toggle('collapsed');
            });
        });

        document.addEventListener('click', e => {
            if (
                this.filtersSidebar &&
                this.filtersSidebar.classList.contains('open') &&
                !e.target.closest('.filters-sidebar') &&
                !e.target.closest('.filter-toggle')
            ) {
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

    applyURLFilters() {
        this.filteredProducts = this.allProducts.filter(p => {
            if (this.selectedCategory && p.category !== this.selectedCategory) return false;
            if (this.selectedSubCategory && p.sub_category !== this.selectedSubCategory) return false;
            if (this.selectedSeries && p.series !== this.selectedSeries) return false;
            return true;
        });

        console.log("🔍 After URL filters:", this.filteredProducts.length, "products");
        this.applyFilters();
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
            maxPrice: this.priceRange ? parseInt(this.priceRange.value) : 50000
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
        this.applySorting();
        this.displayProducts();
    }

    applyFilters() {
        this.filteredProducts = this.allProducts.filter(product => {
            if (this.selectedCategory && product.category !== this.selectedCategory) return false;
            if (this.selectedSubCategory && product.sub_category !== this.selectedSubCategory) return false;
            if (this.selectedSeries && product.series !== this.selectedSeries) return false;

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

    displayProducts() {
        if (!this.productsGrid) return;

        this.productsGrid.innerHTML = '';

        if (!this.filteredProducts.length) {
            this.showNoResults();
            this.updateResultCount();
            return;
        }

        if (this.noResults) this.noResults.style.display = 'none';

        this.filteredProducts.forEach(p => {
            this.productsGrid.appendChild(this.createProductCard(p));
        });

        this.updateResultCount();
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';

        const priceFormatted = product.price.toLocaleString('en-US');
        const imageUrl = product.image || '/static/images/placeholder.jpg';

        card.innerHTML = `
            <div class="product-image">
                <img src="${imageUrl}" alt="${product.name}" onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 200%22%3E%3Crect fill=%22%23e0e0e0%22 width=%22200%22 height=%22200%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 fill=%22%23999%22 font-size=%2214%22%3E${product.brand}%3C/text%3E%3C/svg%3E'">
                <span class="product-badge">${(product.category || '').substring(0, 3).toUpperCase()}</span>
            </div>
            <div class="product-content">
                <div class="product-category">${product.category || 'Product'}</div>
                <div class="product-name">${product.name}</div>
                <div class="product-specs">
                    ${product.cores ? `<div class="spec-item"><span class="spec-label">Cores:</span><span class="spec-value">${product.cores}</span></div>` : ''}
                    ${product.tdp ? `<div class="spec-item"><span class="spec-label">TDP:</span><span class="spec-value">${product.tdp}W</span></div>` : ''}
                    ${product.tech ? `<div class="spec-item"><span class="spec-label">Tech:</span><span class="spec-value">${product.tech}</span></div>` : ''}
                    ${product.socket ? `<div class="spec-item"><span class="spec-label">Socket:</span><span class="spec-value">${product.socket}</span></div>` : ''}
                </div>
            </div>
            <div class="product-footer">
                <div>
                    <div class="product-price">$${priceFormatted}</div>
                </div>
                <button class="btn-view"
  onclick="window.location.href='/products/${product.category}/${product.series}/${product.id}'">
  View
</button>

            </div>
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
        document.body.style.overflow = this.filtersSidebar.classList.contains('open') ? 'hidden' : '';
    }
}

// INIT
document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 ProductsManager initialized");
    new ProductsManager();
});
