// =============================
// READ PRODUCT SLUG FROM CLEAN URL
// Supports URL format: /cpu/<series>/<product-slug>
// =============================

// Get parts of the URL path
const pathParts = window.location.pathname.split("/").filter(Boolean);

// pattern: /cpu/<series>/<slug>
let productSlug = pathParts[2] || null;

const API_HOST = "http://127.0.0.1:5000";

if (!productSlug) {
  document.getElementById("prodName").textContent = "Invalid product URL.";
  throw new Error("Missing product slug in URL");
}

// Convert slug → readable string for matching
// "AMD-Ryzen-9-PRO-3900" -> "amd ryzen 9 pro 3900"
const productNameNormalized = productSlug.replace(/-/g, " ").toLowerCase();


// =============================
// LOAD PRODUCT
// =============================
async function loadProduct() {
  try {
    const res = await fetch(`${API_HOST}/api/products/all`);
    const data = await res.json();
    const allProducts = data.products || [];

    // =============================
    // FIND PRODUCT USING NAME SLUG
    // =============================
    const product = allProducts.find(p =>
      p.name.toLowerCase().replace(/\s+/g, " ") === productNameNormalized
    );

    if (!product) {
      document.getElementById("prodName").textContent = "Product not found.";
      console.error("No match for slug:", productSlug);
      return;
    }

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
    document.getElementById("prodCategory").textContent = product.category || "-";

    document.getElementById("prodWarranty").textContent =
      product.warranty || "Standard 1 Year Manufacturer Warranty.";

    // =============================
    // UNIVERSAL SPEC TABLE (NO UNDEFINED)
    // =============================
    const infoTable = document.getElementById("additionalInfoTable");
    infoTable.innerHTML = "";

    const specMap = {
      // Common
      Brand: product.brand,
      Series: product.series,
      Category: product.category,
      Application: product.application,
      Status: product.status || "New",

      // CPU
      Socket: product.socket,
      Cores: product.cores,
      Threads: product.threads,
      "Base Frequency": product.base_freq ? `${product.base_freq} GHz` : null,
      Cache: product.cache ? `${product.cache} MB` : null,
      TDP: product.tdp ? `${product.tdp} W` : null,
      Technology: product.tech,
      "Memory Type": product.memory_type,
      "Max Memory": product.max_memory_size
        ? `${product.max_memory_size} GB`
        : null,
      Packaging: product.packaging,

      // HDD / SSD
      Capacity: product.capacity,
      RPM: product.rpm,
      Interface: product.interface,
      "Form Factor": product.form_factor,

      // RAM
      Speed: product.speed,
      Voltage: product.voltage,
      Pins: product.pins,
      "ECC Support":
        typeof product.ecc === "boolean" ? (product.ecc ? "Yes" : "No") : null,
      Registered:
        typeof product.registered === "boolean"
          ? (product.registered ? "Yes" : "No")
          : null,
      Model: product.model,

      // Monitors
      "Screen Size": product.screen_size,
      Resolution: product.resolution,
      "Aspect Ratio": product.aspect_ratio,
      "Panel Type": product.panel_type,
      Curvature: product.curvature,
      "Max Refresh Rate": product.refresh_rate_max,
      "Response Time": product.response_time,
      HDR: product.hdr,
      "Color Depth": product.color_depth,
      "Brightness (cd/m²)": product.brightness_typical_cd_m2,
      "Contrast Ratio": product.contrast_ratio_static,
      "Viewing Angles": product.viewing_angles,
      Dimensions: product.dimensions_mm,
      Weight: product.weight_kg ? `${product.weight_kg} kg` : null,

      // Laptops / Desktops
      RAM: product.ram,
      Storage: product.storage,
      Processor: product.processor_name,

      // Server basics
      Chipset: product.chipset,
      "Server Form Factor": product.form_factor
    };

    // Render simple fields
    Object.entries(specMap).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${key}</td><td>${value}</td>`;
        infoTable.appendChild(row);
      }
    });

    // =============================
    // NESTED OBJECT FIELDS (Dynamic)
    // =============================
    const nestedGroups = {
      Processor: product.processor,
      Storage: product.storage,
      Network: product.network,
      Ports: product.ports,
      Expansion: product.expansion,
      "Power Supply": product.power_supply
    };

    Object.entries(nestedGroups).forEach(([groupName, groupObj]) => {
      if (groupObj && typeof groupObj === "object") {
        const nestedHTML = Object.entries(groupObj)
          .map(([k, v]) => `<b>${k.replace(/_/g, " ").toUpperCase()}</b>: ${v}`)
          .join("<br>");

        const row = document.createElement("tr");
        row.innerHTML = `<td>${groupName}</td><td>${nestedHTML}</td>`;
        infoTable.appendChild(row);
      }
    });

    // =============================
    // FEATURES ARRAY
    // =============================
    if (Array.isArray(product.features) && product.features.length > 0) {
      const row = document.createElement("tr");
      row.innerHTML = `<td>Features</td><td>${product.features.join("<br>")}</td>`;
      infoTable.appendChild(row);
    }

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
        document.querySelectorAll(".thumbnail-row img")
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
