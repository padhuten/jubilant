// =============================
// READ PRODUCT FROM CLEAN URL
// Supports ALL formats:
// /products/cpu/amd-desktop/cpu-9700x
// /products/memory/samsung/ram-samsung-8gb-ddr4-udimm
// /products/hdd/seagate/exos-x18
// =============================

const pathParts = window.location.pathname.split("/").filter(Boolean);

// ✅ ALWAYS TAKE LAST PART AS PRODUCT ID
const productId = pathParts[pathParts.length - 1];

const API_HOST = "http://127.0.0.1:5000";

if (!productId) {
  document.getElementById("prodName").textContent = "Invalid product URL.";
  throw new Error("Missing product id in URL");
}

// =============================
// LOAD PRODUCT (SINGLE PRODUCT API)
// =============================
async function loadProduct() {
  try {
    const res = await fetch(`${API_HOST}/api/products/${productId}`);

    if (!res.ok) throw new Error("API error");

    const data = await res.json();

    if (!data.success || !data.product) {
      document.getElementById("prodName").textContent = "Product not found.";
      return;
    }

    const product = data.product;

    // =============================
    // BASIC PRODUCT INFO
    // =============================
    document.getElementById("prodName").textContent =
      product.name || "Unnamed Product";

    document.getElementById("prodPrice").textContent =
      product.price !== undefined ? `US $${product.price}` : "Price on request";

    document.getElementById("prodImage").src =
      API_HOST + (product.image || "/static/images/no-image.png");

    document.getElementById("prodDescription").textContent =
      product.description || "No description available.";

    document.getElementById("tabDescription").textContent =
      product.description || "No description available.";

    document.getElementById("prodBrand").textContent = product.brand || "-";
    document.getElementById("prodCategory").textContent =
      product.category || "-";

    document.getElementById("prodWarranty").textContent =
      product.warranty || "Standard 1 Year Manufacturer Warranty.";

    // =============================
    // UNIVERSAL SPEC TABLE
    // =============================
    const infoTable = document.getElementById("additionalInfoTable");
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

      Packaging: product.packaging
    };

    Object.entries(specMap).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${key}</td><td>${value}</td>`;
        infoTable.appendChild(row);
      }
    });

    // =============================
    // IMAGE GALLERY
    // =============================
    const thumbRow = document.getElementById("thumbRow");
    thumbRow.innerHTML = "";

    const images = product.images?.length
      ? product.images
      : [product.image];

    images.forEach((img, index) => {
      if (!img) return;

      const thumb = document.createElement("img");
      thumb.src = API_HOST + img;

      if (index === 0) thumb.classList.add("active");

      thumb.addEventListener("click", () => {
        document.getElementById("prodImage").src = API_HOST + img;
        document
          .querySelectorAll(".thumbnail-row img")
          .forEach(t => t.classList.remove("active"));
        thumb.classList.add("active");
      });

      thumbRow.appendChild(thumb);
    });

  } catch (err) {
    console.error("PRODUCT LOAD ERROR:", err);
    document.getElementById("prodName").textContent =
      "Error loading product.";
  }
}

loadProduct();
