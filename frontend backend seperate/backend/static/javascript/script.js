// document.addEventListener("DOMContentLoaded", () => {

//     // ============================
//     // CONFIG
//     // ============================
//     const API_HOST = "http://127.0.0.1:5000";
//     const API_ALL_PRODUCTS_URL = `${API_HOST}/api/products/all`;
//     const PRODUCTS_PER_PAGE = 10;

//     // ============================
//     // DOM REFERENCES
//     // ============================
//     const shortlistGrid = document.getElementById("shortlist-grid");
//     const priceRange = document.getElementById("price-max");
//     const priceValueSpan = document.getElementById("price-value");
//     const filterSidebar = document.querySelector(".filter-sidebar");
//     const productContent = document.querySelector(".product-content");

//     const paginationContainer = document.createElement("div");
//     paginationContainer.id = "pagination-container";
//     productContent.appendChild(paginationContainer);

//     // ============================
//     // STATE
//     // ============================
//     let allProducts = [];
//     let filteredProducts = [];
//     let currentPage = 1;

//     priceValueSpan.textContent = `$${priceRange.value}`;

//     // ============================
//     // COLLECT FILTERS
//     // ============================
//     function collectFilters() {
//         const filters = {
//             brands: [],
//             categories: [],
//             applications: [],
//             sockets: [],
//             cores: [],
//             tdp: [],
//             threads: [],
//             cache: [],
//             base_freq: [],
//             tech: [],
//             memory_type: [],
//             max_memory_size: [],
//             packaging: [],
//             maxPrice: parseFloat(priceRange.value),
//         };

//         document.querySelectorAll(".filter-checkbox:checked").forEach((checkbox) => {
//             const group = checkbox.name;
//             let value = checkbox.value;

//             if (["cores", "tdp", "threads", "cache", "max_memory_size"].includes(group)) {
//                 value = parseInt(value);
//             }

//             if (group === "base_freq") value = parseFloat(value);

//             if (group === "category") {
//                 filters.categories.push(value);
//             } else {
//                 filters[group + "s"]?.push(value);
//             }
//         });

//         return filters;
//     }

//     // ============================
//     // APPLY URL CATEGORY FILTER (MAIN FIX)
//     // ============================
//     function applyFilters() {
//         const params = new URLSearchParams(window.location.search);
//         let selectedCategory = params.get("category");

//         // If no category param, show all
//         if (!selectedCategory) {
//             filteredProducts = [...allProducts];
//             renderProducts(filteredProducts);
//             return;
//         }

//         // Normalize category in URL
//         selectedCategory = selectedCategory
//             .toLowerCase()
//             .trim()
//             .replace(/\s+/g, " ");

//         // Filter products
//         filteredProducts = allProducts.filter(p => {
//             if (!p.category) return false;

//             let cat = p.category
//                 .toLowerCase()
//                 .trim()
//                 .replace(/\s+/g, " ");

//             // remove junk like "Whole CPU Processors"
//             const firstPart = cat.split("whole")[0].trim();

//             return firstPart.includes(selectedCategory);
//         });

//         currentPage = 1;
//         renderProducts(filteredProducts);
//     }

//     // ============================
//     // CLIENT FILTERS (sidebar filters)
//     // ============================
//     function applyClientFilters() {
//         const filters = collectFilters();

//         filteredProducts = allProducts.filter((product) => {
//             if (product.price > filters.maxPrice) return false;

//             if (filters.brands.length && !filters.brands.includes(product.brand)) return false;

//             if (filters.categories.length &&
//                 !filters.categories.some(cat =>
//                     product.category?.toLowerCase().includes(cat.toLowerCase())
//                 )
//             ) return false;

//             if (filters.applications.length && !filters.applications.includes(product.application)) return false;
//             if (filters.sockets.length && !filters.sockets.includes(product.socket)) return false;

//             if (filters.cores.length && !filters.cores.includes(product.cores)) return false;
//             if (filters.threads.length && !filters.threads.includes(product.threads)) return false;
//             if (filters.cache.length && !filters.cache.includes(product.cache)) return false;
//             if (filters.tdp.length && !filters.tdp.includes(product.tdp)) return false;

//             if (filters.base_freq.length && !filters.base_freq.includes(product.base_freq)) return false;
//             if (filters.tech.length && !filters.tech.includes(product.tech)) return false;

//             return true;
//         });

//         currentPage = 1;
//         renderProducts(filteredProducts);
//     }

//     // ============================
//     // FETCH ALL PRODUCTS
//     // ============================
//     async function fetchAllProducts() {
//         shortlistGrid.innerHTML = `<p class="loading-message">Loading products...</p>`;
//         filterSidebar.style.opacity = "0.5";

//         try {
//             const response = await fetch(API_ALL_PRODUCTS_URL);
//             if (!response.ok) throw new Error("Backend is unreachable");

//             const data = await response.json();

//             allProducts = (data.products || []).map((p) => ({
//                 ...p,
//                 price: parseFloat(p.price),
//                 cores: parseInt(p.cores),
//                 tdp: parseInt(p.tdp),
//                 threads: parseInt(p.threads),
//                 cache: parseInt(p.cache),
//                 base_freq: parseFloat(p.base_freq),
//                 max_memory_size: parseInt(p.max_memory_size),
//                 description: p.description || "No description available.",
//             }));

//             // Default: Apply URL category filter first
//             applyFilters();

//             filterSidebar.style.opacity = "1";

//         } catch (err) {
//             shortlistGrid.innerHTML = `<p class="error-message">${err.message}</p>`;
//         }
//     }

//     // ============================
//     // RENDER PRODUCTS
//     // ============================
//     function renderProducts(products) {
//         shortlistGrid.innerHTML = "";

//         const start = (currentPage - 1) * PRODUCTS_PER_PAGE;
//         const end = start + PRODUCTS_PER_PAGE;
//         const items = products.slice(start, end);

//         if (items.length === 0) {
//             shortlistGrid.innerHTML = `<p>No products match your criteria.</p>`;
//             return;
//         }

//         items.forEach((product) => {
//             const html = `
//                 <div class="product-card">
//                     <div class="product-image-container"
//                         onclick="window.location.href='/product.html?id=${product.id}'">
//                         <img src="${API_HOST}${product.image}"
//                             onerror="this.src='https://placehold.co/200x200?text=No+Image'">
//                     </div>
//                     <h4>${product.name}</h4>
//                     <p class="product-spec-snippet">${product.description}</p>
//                     <p class="price-value">US $${product.price}/pcs</p>
//                 </div>
//             `;

//             shortlistGrid.insertAdjacentHTML("beforeend", html);
//         });

//         renderPagination(products.length);
//     }

//     // ============================
//     // PAGINATION
//     // ============================
//     function renderPagination(total) {
//         paginationContainer.innerHTML = "";

//         const totalPages = Math.ceil(total / PRODUCTS_PER_PAGE);
//         if (totalPages <= 1) return;

//         for (let i = 1; i <= totalPages; i++) {
//             const btn = document.createElement("button");
//             btn.textContent = i;

//             btn.classList.add("pagination-btn");
//             if (i === currentPage) btn.classList.add("active");

//             btn.addEventListener("click", () => {
//                 currentPage = i;
//                 renderProducts(filteredProducts);
//             });

//             paginationContainer.appendChild(btn);
//         }
//     }

//     // ============================
//     // EVENT LISTENERS
//     // ============================
//     priceRange.addEventListener("input", () => {
//         priceValueSpan.textContent = `$${priceRange.value}`;
//         applyClientFilters();
//     });

//     document.querySelectorAll(".filter-checkbox").forEach((cb) => {
//         cb.addEventListener("change", applyClientFilters);
//     });

//     document.querySelectorAll(".filter-header").forEach((header) => {
//         header.addEventListener("click", () => {
//             header.parentElement.classList.toggle("active");
//         });
//     });

//     // ============================
//     // INITIAL LOAD
//     // ============================
//     fetchAllProducts();

// });
