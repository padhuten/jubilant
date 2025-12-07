// =============================
// READ ?id= FROM URL
// =============================
const params = new URLSearchParams(window.location.search);
const productId = params.get("id");
const API_HOST = "http://127.0.0.1:5000";

if (!productId) {
  document.getElementById("prodName").textContent = "No product selected.";
  throw new Error("Missing ?id= in URL");
}

// =============================
// LOAD PRODUCT
// =============================
async function loadProduct() {
  try {
    const res = await fetch(`${API_HOST}/api/products/all`);
    const data = await res.json();
    const allProducts = data.products || [];

    const product = allProducts.find(p => String(p.id) === String(productId));

    if (!product) {
      document.getElementById("prodName").textContent = "Product not found.";
      return;
    }

    // =============================
    // ✅ BASIC PRODUCT DATA
    // =============================
    document.getElementById("prodName").textContent = product.name;
    document.getElementById("prodPrice").textContent = `US $${product.price}`;
    document.getElementById("prodImage").src = API_HOST + product.image;

    document.getElementById("prodDescription").textContent =
      product.description || "No description available.";

    document.getElementById("tabDescription").textContent =
      product.description || "No description available.";

    document.getElementById("prodBrand").textContent = product.brand || "-";
    document.getElementById("prodCategory").textContent = product.category || "-";

    document.getElementById("prodWarranty").textContent =
      product.warranty || "Standard 1 Year Manufacturer Warranty.";

    // =============================
    // ✅ DYNAMIC ADDITIONAL INFO (NO UNDEFINED EVER)
    // =============================
    const infoTable = document.getElementById("additionalInfoTable");
    infoTable.innerHTML = "";

    const specMap = {
      // ✅ Common
      Brand: product.brand,
      Status: product.status || "New",
      Application: product.application,

      // ✅ CPU
      Socket: product.socket,
      Cores: product.cores,
      Threads: product.threads,
      "Base Frequency": product.base_freq ? `${product.base_freq} GHz` : null,
      Cache: product.cache ? `${product.cache} MB` : null,
      TDP: product.tdp ? `${product.tdp} W` : null,
      Technology: product.tech,
      "Memory Type": product.memory_type,
      "Max Memory": product.max_memory_size ? `${product.max_memory_size} GB` : null,
      Packaging: product.packaging,

      // ✅ HDD / SSD
      Capacity: product.capacity,
      RPM: product.rpm,
      Interface: product.interface,
      "Form Factor": product.form_factor,

      // ✅ Laptop / Desktop (future-ready)
      RAM: product.ram,
      Storage: product.storage,
      "Screen Size": product.screen_size,
      Processor: product.processor
    };

    Object.entries(specMap).forEach(([label, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${label}</td><td>${value}</td>`;
        infoTable.appendChild(row);
      }
    });

    // =============================
    // ✅ IMAGE GALLERY + THUMBNAILS
    // =============================
    const thumbRow = document.getElementById("thumbRow");
    thumbRow.innerHTML = "";

    const images = product.images?.length
      ? product.images
      : [product.image];

    images.forEach((img, index) => {
      const thumb = document.createElement("img");
      thumb.src = API_HOST + img;

      if (index === 0) thumb.classList.add("active");

      thumb.addEventListener("click", () => {
        document.getElementById("prodImage").src = API_HOST + img;
        document.querySelectorAll(".thumbnail-row img").forEach(t =>
          t.classList.remove("active")
        );
        thumb.classList.add("active");
      });

      thumbRow.appendChild(thumb);
    });

  } catch (err) {
    console.error("PRODUCT LOAD ERROR:", err);
    document.getElementById("prodName").textContent = "Error loading product.";
  }
}

loadProduct();
