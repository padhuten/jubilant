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
  // READ SERIES FROM CLEAN URL
  // SUPPORTS:
  //   /products/<series>
  //   /cpu/<series>
  //   /cpu/<series>/<product-slug>
  // --------------------------------------------------

  const pathParts = window.location.pathname.split("/").filter(Boolean);
  let selectedSeries = null;

  console.log("📌 URL PATH PARTS:", pathParts);

  // Case 1: /cpu/<series>/...
  if (pathParts[0] === "cpu" && pathParts[1]) {
    selectedSeries = pathParts[1].toLowerCase();
  }

  // Case 2: /products/<series>
  if (pathParts[0] === "products" && pathParts[1]) {
    selectedSeries = pathParts[1].toLowerCase();
  }

  console.log("🎯 CLEAN URL SERIES DETECTED:", selectedSeries);


  // --------------------------------------------------
  // FETCH ALL PRODUCTS
  // --------------------------------------------------
  async function fetchAllProducts() {
    productGrid.innerHTML = `<p class="loading">Loading products...</p>`;
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
        series: (p.series || "").toString().toLowerCase().trim()
      }));

      console.log("📦 TOTAL PRODUCTS:", allProducts.length);
      console.log("📌 AVAILABLE SERIES:", [...new Set(allProducts.map(p => p.series))]);

      applySeriesFilter();

      if (filterSidebar) filterSidebar.style.opacity = "1";

    } catch (err) {
      console.error("❌ API ERROR:", err);
      productGrid.innerHTML = `<p class="error">Failed to load products</p>`;
    }
  }

  // --------------------------------------------------
  // APPLY SERIES FILTER FROM URL
  // --------------------------------------------------
  function applySeriesFilter() {

    if (!selectedSeries) {
      console.warn("⚠️ No series detected — Showing ALL products");
      filteredProducts = [...allProducts];
      renderProducts(filteredProducts);
      return;
    }

    filteredProducts = allProducts.filter(p => p.series === selectedSeries);

    console.log("🎯 FILTERING BY SERIES:", selectedSeries);
    console.log("📌 MATCHED PRODUCTS:", filteredProducts.length);

    currentPage = 1;
    renderProducts(filteredProducts);
  }

  // --------------------------------------------------
  // PRICE FILTER
  // --------------------------------------------------
  if (priceRange) {
    priceRange.addEventListener("input", () => {
      priceValueSpan.textContent = `$${priceRange.value}`;
      const maxPrice = parseFloat(priceRange.value);

      const priceFiltered = filteredProducts.filter(p => p.price <= maxPrice);
      currentPage = 1;
      renderProducts(priceFiltered);
    });
  }

  // --------------------------------------------------
  // RENDER PRODUCT CARDS
  // --------------------------------------------------
  function renderProducts(products) {
    productGrid.innerHTML = "";

    if (!products.length) {
      productGrid.innerHTML = `<p>No products found for this series.</p>`;
      paginationContainer.innerHTML = "";
      return;
    }

    const start = (currentPage - 1) * PRODUCTS_PER_PAGE;
    const end = start + PRODUCTS_PER_PAGE;
    const display = products.slice(start, end);

    display.forEach(p => {
      const slug = p.name.replace(/\s+/g, "-"); // create product slug

      const card = `
        <div class="product-card" onclick="openProduct('${p.series}', '${slug}')">
          <div class="product-image">
            <img src="${API_HOST}${p.image}"
              onerror="this.src='https://placehold.co/200x200'">
          </div>
          <h4>${p.name}</h4>
          <p class="small">${p.brand} • ${p.cores}C/${p.threads}T • ${p.base_freq}GHz</p>
          <p class="desc">${p.description}</p>
          <p class="price">US $${p.price}</p>
        </div>
      `;

      productGrid.insertAdjacentHTML("beforeend", card);
    });

    renderPagination(products.length);
  }

  // --------------------------------------------------
  // CLEAN PRODUCT URL HANDLER
  // --------------------------------------------------
  window.openProduct = function (series, slug) {
    window.location.href = `/cpu/${series}/${slug}`;
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

  // --------------------------------------------------
  // INIT
  // --------------------------------------------------
  fetchAllProducts();

});
