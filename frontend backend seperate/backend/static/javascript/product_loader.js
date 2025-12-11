import { cpu_products } from "./cpu_data.js";

const params = new URLSearchParams(window.location.search);
const cpuParam = params.get("cpu");

if (!cpuParam) {
    document.getElementById("prodName").textContent = "No product selected.";
    throw new Error("Missing ?cpu= in URL");
}

// try multiple match methods
const product = cpu_products.find(p =>
    p.id.toLowerCase() === cpuParam.toLowerCase() ||
    p.name.toLowerCase().replace(/\s+/g, "_") === cpuParam.toLowerCase() ||
    p.name.toLowerCase() === cpuParam.toLowerCase()
);

if (!product) {
    document.getElementById("prodName").textContent = "Product not found.";
    throw new Error("Invalid CPU name: " + cpuParam);
}
