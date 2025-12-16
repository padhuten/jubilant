document.addEventListener("DOMContentLoaded", () => {

  console.log("🔥 MASTER PRODUCT ENGINE LOADED — CLEAN URL MODE ENABLED");

  const API_HOST = "http://127.0.0.1:5000";
  const API_ALL_PRODUCTS_URL = `${API_HOST}/api/products/all`;
  const PRODUCTS_PER_PAGE = 10;

  const productGrid = document.getElementById("shortlist-grid");
  const filterSidebar = document.querySelector(".filter-sidebar");
  const priceRange = document.getElementById("price-max");
  const priceValueSpan = document.getElementById("price-value");
  const productContent = document.querySelector(".product-content");

  const seriesGrid = document.createElement("div");
  seriesGrid.id = "series-grid";
  productContent.prepend(seriesGrid);

  const paginationContainer = document.createElement("div");
  paginationContainer.id = "pagination-container";
  productContent.appendChild(paginationContainer);

  let allProducts = [];
  let filteredProducts = [];
  let currentPage = 1;

  if (priceRange && priceValueSpan) {
    priceValueSpan.textContent = `$${priceRange.value}`;
  }

  // --------------------------------------------------
  // READ CLEAN URL (3 LEVEL SUPPORT)
  // --------------------------------------------------
  const pathParts = window.location.pathname.split("/").filter(Boolean);

  let selectedCategory = null;
  let selectedSubCategory = null;
  let selectedSeries = null;

  if (pathParts[0] === "products") {
    selectedCategory = pathParts[1]?.toLowerCase() || null;
    selectedSubCategory = pathParts[2]?.toLowerCase() || null;
    selectedSeries = pathParts[3]?.toLowerCase() || null;
  }

  console.log("🎯 CATEGORY:", selectedCategory);
  console.log("🎯 SUB CATEGORY:", selectedSubCategory);
  console.log("🎯 SERIES:", selectedSeries);

  // --------------------------------------------------
  // FETCH ALL PRODUCTS
  // --------------------------------------------------
  async function fetchAllProducts() {
    productGrid.innerHTML = `<p class="loading">Loading products...</p>`;
    seriesGrid.innerHTML = "";
    if (filterSidebar) filterSidebar.style.opacity = "0.5";

    try {
      const res = await fetch(API_ALL_PRODUCTS_URL);
      const data = await res.json();

      allProducts = (data.products || []).map(p => ({
        ...p,
        price: parseFloat(p.price) || 0,
        cores: parseInt(p.cores) || 0,
        threads: parseInt(p.threads) || 0,
        base_freq: parseFloat(p.base_freq) || 0,
        description: p.description || "No description available.",
        category: (p.category_key || "").toLowerCase().trim(),
        sub_category: (p.sub_category || "").toLowerCase().trim(),
        series: (p.series || "").toLowerCase().trim()
      }));

      console.log("📦 TOTAL PRODUCTS:", allProducts.length);

      applySeriesFilter();

      if (filterSidebar) filterSidebar.style.opacity = "1";

    } catch (err) {
      console.error("❌ API ERROR:", err);
      productGrid.innerHTML = `<p class="error">Failed to load products</p>`;
    }
  }

  // --------------------------------------------------
  // APPLY FILTER (3 LEVEL LOGIC)
  // --------------------------------------------------
  function applySeriesFilter() {

    // LEVEL 1 → /products/cpu
    if (selectedCategory && !selectedSubCategory && !selectedSeries) {
      currentPage = 1;
      filteredProducts = allProducts.filter(
        p => p.category === selectedCategory
      );
      renderProducts(filteredProducts);
      return;
    }

    // LEVEL 2 → /products/cpu/amd-desktop
    if (selectedCategory && selectedSubCategory && !selectedSeries) {
      currentPage = 1;
      filteredProducts = allProducts.filter(
        p =>
          p.category === selectedCategory &&
          p.sub_category === selectedSubCategory
      );
      renderProducts(filteredProducts);
      return;
    }

    // LEVEL 3 → /products/cpu/amd-desktop/ryzen
    if (selectedCategory && selectedSubCategory && selectedSeries) {
      currentPage = 1;
      filteredProducts = allProducts.filter(
        p =>
          p.category === selectedCategory &&
          p.sub_category === selectedSubCategory &&
          p.series === selectedSeries
      );
      renderProducts(filteredProducts);
      return;
    }

    filteredProducts = [...allProducts];
    renderProducts(filteredProducts);
  }

  // --------------------------------------------------
  // PRICE FILTER
  // --------------------------------------------------
  if (priceRange) {
    priceRange.addEventListener("input", () => {
      priceValueSpan.textContent = `$${priceRange.value}`;
      const maxPrice = parseFloat(priceRange.value);
      renderProducts(filteredProducts.filter(p => p.price <= maxPrice));
    });
  }

  // --------------------------------------------------
  // RENDER PRODUCT CARDS
  // --------------------------------------------------
  function renderProducts(products) {
    productGrid.innerHTML = "";
    seriesGrid.innerHTML = "";

    if (!products.length) {
      productGrid.innerHTML = `<p>No products found.</p>`;
      paginationContainer.innerHTML = "";
      return;
    }

    const start = (currentPage - 1) * PRODUCTS_PER_PAGE;
    const end = start + PRODUCTS_PER_PAGE;

    products.slice(start, end).forEach(p => {
      const slug = p.name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/(^-|-$)/g, "");

      productGrid.insertAdjacentHTML("beforeend", `
        <div class="product-card" onclick="openProduct('${p.series}', '${slug}')">
          <div class="product-image">
            <img src="${API_HOST}${p.image}" onerror="this.src='https://placehold.co/200x200'">
          </div>
          <h4>${p.name}</h4>
          <p class="small">${p.brand} • ${p.cores}C/${p.threads}T • ${p.base_freq}GHz</p>
          <p class="desc">${p.description}</p>
          <p class="price">US $${p.price}</p>
        </div>
      `);
    });

    renderPagination(products.length);
  }

  // --------------------------------------------------
  // PRODUCT PAGE NAV (CLEAN URL)
  // --------------------------------------------------
  window.openProduct = function (series, slug) {
    if (selectedCategory && selectedSubCategory) {
      window.location.href = `/products/${selectedCategory}/${selectedSubCategory}/${series}/${slug}`;
    } else if (selectedCategory) {
      window.location.href = `/products/${selectedCategory}/${series}/${slug}`;
    } else {
      window.location.href = `/product/${slug}`;
    }
  };

  // --------------------------------------------------
  // PAGINATION
  // --------------------------------------------------
  function renderPagination(total) {
    paginationContainer.innerHTML = "";
    const totalPages = Math.ceil(total / PRODUCTS_PER_PAGE);
    if (totalPages <= 1) return;

    for (let i = 1; i <= totalPages; i++) {
      const btn = document.createElement("button");
      btn.textContent = i;
      btn.classList.add("pagination-btn");
      if (i === currentPage) btn.classList.add("active");

      btn.onclick = () => {
        currentPage = i;
        renderProducts(filteredProducts);
      };

      paginationContainer.appendChild(btn);
    }
  }

  fetchAllProducts();

});
