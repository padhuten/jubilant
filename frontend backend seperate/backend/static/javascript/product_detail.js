// =============================
// READ PRODUCT FROM CLEAN URL
// Supports ALL formats:
// /products/cpu/amd-desktop/cpu-9700x
// /products/memory/samsung/ram-samsung-8gb-ddr4-udimm
// /products/hdd/seagate/exos-x18
// =============================

document.addEventListener("DOMContentLoaded", () => {

  const pathParts = window.location.pathname.split("/").filter(Boolean);

  // ✅ ALWAYS TAKE LAST PART AS PRODUCT ID
  const productId = pathParts[pathParts.length - 1];

  const prodNameEl = document.getElementById("prodName");
  if (!productId) {
    if (prodNameEl) prodNameEl.textContent = "Invalid product URL.";
    return;
  }

  // =============================
  // LOAD PRODUCT (SINGLE PRODUCT API)
  // =============================
  async function loadProduct() {
    try {
      const res = await fetch(`/api/products/${productId}`);
      if (!res.ok) throw new Error("API error");

      const data = await res.json();

      if (!data.success || !data.product) {
        if (prodNameEl) prodNameEl.textContent = "Product not found.";
        return;
      }

      const product = data.product;

      // =============================
      // BASIC PRODUCT INFO
      // =============================
      if (prodNameEl)
        prodNameEl.textContent = product.name || "Unnamed Product";

      const prodPriceEl = document.getElementById("prodPrice");
      if (prodPriceEl)
        prodPriceEl.textContent =
          product.price !== undefined
            ? `US $${product.price}`
            : "Price on request";

      const prodImageEl = document.getElementById("prodImage");
      if (prodImageEl)
        prodImageEl.src = product.image || "/static/images/no-image.png";

      const prodDescEl = document.getElementById("prodDescription");
      if (prodDescEl)
        prodDescEl.textContent =
          product.description || "No description available.";

      const tabDescEl = document.getElementById("tabDescription");
      if (tabDescEl)
        tabDescEl.textContent =
          product.description || "No description available.";

      const prodBrandEl = document.getElementById("prodBrand");
      if (prodBrandEl) prodBrandEl.textContent = product.brand || "-";

      const prodCategoryEl = document.getElementById("prodCategory");
      if (prodCategoryEl)
        prodCategoryEl.textContent = product.category || "-";

      const prodWarrantyEl = document.getElementById("prodWarranty");
      if (prodWarrantyEl)
        prodWarrantyEl.textContent =
          product.warranty || "Standard 1 Year Manufacturer Warranty.";

      // =============================
      // UNIVERSAL SPEC TABLE
      // =============================
      const infoTable = document.getElementById("additionalInfoTable");
      if (infoTable) {
        infoTable.innerHTML = "";

        const specMap = {
          Brand: product.brand,
          Series: product.series,
          Category: product.category,
          Application: product.application,
          Status: product.status || "New",

          Socket: product.socket,
          Cores: product.cores,
          Threads: product.threads,
          "Base Frequency": product.base_freq
            ? `${product.base_freq} GHz`
            : null,
          Cache: product.cache ? `${product.cache} MB` : null,
          TDP: product.tdp ? `${product.tdp} W` : null,
          Technology: product.tech,

          "Memory Type": product.memory_type,
          Capacity: product.capacity,
          Speed: product.speed,
          Voltage: product.voltage,
          "Form Factor": product.form_factor,
          ECC: product.ecc,

          Packaging: product.packaging,

          // ===== MONITOR SPECS =====
          "Screen Size": product.screen_size,
          Resolution: product.resolution,
          "Aspect Ratio": product.aspect_ratio,
          "Panel Type": product.panel_type,
          Curvature: product.curvature,
          "HDR Support": product.hdr,
          "Max Refresh Rate": product.refresh_rate_max,
          "Response Time": product.response_time,
          "Color Depth": product.color_depth,
          "Viewing Angles": product.viewing_angles,
          Dimensions: product.dimensions_mm,
          Weight: product.weight_kg
            ? `${product.weight_kg} kg`
            : null,

          // ===== LAPTOP SPECS =====
          Processor: product.processor,
          Memory: product.memory,
          Storage: product.storage,
          Graphics: product.graphics,
          Display: product.display,
          Network: product.network,
          "Operating System": product.operating_system,
          Color: product.color,
          Warranty: product.warranty,

          // ===== MOTHERBOARD =====
          Chipset: product.chipset
        };

        Object.entries(specMap).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== "") {
            const row = document.createElement("tr");
            row.innerHTML = `<td>${key}</td><td>${value}</td>`;
            infoTable.appendChild(row);
          }
        });
      }

      // =============================
      // IMAGE GALLERY
      // =============================
      const thumbRow = document.getElementById("thumbRow");
      if (thumbRow) {
        thumbRow.innerHTML = "";

        const images = product.images?.length
          ? product.images
          : [product.image];

        images.forEach((img, index) => {
          if (!img) return;

          const thumb = document.createElement("img");
          thumb.src = img;

          if (index === 0) thumb.classList.add("active");

          thumb.addEventListener("click", () => {
            if (prodImageEl) prodImageEl.src = img;
            document
              .querySelectorAll(".thumbnail-row img")
              .forEach(t => t.classList.remove("active"));
            thumb.classList.add("active");
          });

          thumbRow.appendChild(thumb);
        });
      }
    } catch (err) {
      console.error("PRODUCT LOAD ERROR:", err);
      if (prodNameEl)
        prodNameEl.textContent = "Error loading product.";
    }
  }

  loadProduct();
});
