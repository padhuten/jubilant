import os
from flask import Blueprint, render_template, send_from_directory, request, redirect
from config import STATIC_DIR, TEMPLATES_DIR

pages_bp = Blueprint("pages_bp", __name__)


# ------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------
@pages_bp.route('/')
def home():
    return render_template("index.html")


# ------------------------------------------------------
# STATIC IMAGES
# ------------------------------------------------------
@pages_bp.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(STATIC_DIR, "images"), filename)


# ------------------------------------------------------
# PRODUCT TAXONOMY (MASTER)
# ------------------------------------------------------
CATEGORIES = {
    "cpu": {
        "amd-server": ["9005", "9004", "7003", "8004", "4004", "4005"],
        "amd-desktop": ["ryzen", "ryzen-pro"],
        "intel-desktop": ["i9", "i7", "i5", "i3"]
    },

    "hard-drive": {
        "seagate": ["barracuda", "ironwolf", "skyhawk", "exos", "firecuda"],
        "western-digital": ["wd-blue", "wd-black", "wd-red", "wd-purple", "wd-gold"],
        "toshiba": ["p300", "n300", "s300", "mg"]
    },

    "ssd": {
        "samsung": ["870-evo", "870-qvo", "980", "980-pro", "990-pro", "pm9a3", "983", "893"],
        "crucial": ["mx500", "p3", "p3-plus", "p5", "p5-plus", "t500", "t700"],
        "micron": ["2400", "2450", "3400", "3500", "5400", "6500-ion", "7500-pro", "7500-max"]
    },

    "memory": {
        "samsung": ["ddr3", "ddr4", "ddr5"],
        "crucial": ["ddr3", "ddr4", "ddr5"],
        "micron": ["ddr3", "ddr4", "ddr5"]
    },

    "monitors": {
        "samsung": ["business", "curved", "gaming"],
        "aoc-philips": ["professional", "value"],
        "dell": ["ultrasharp", "p-series"],
        "hp": ["business", "consumer", "ergonomic"]
    },

    "laptop": {
        "consumer": {
            "acer": ["aspire", "swift", "nitro"],
            "lenovo": ["ideapad", "yoga", "legion"],
            "dell": ["inspiron", "xps", "g-series"],
            "hp": ["pavilion", "envy", "victus"]
        },
        "business": {
            "asus": ["expertbook", "proart"],
            "acer": ["travelmate", "veriton"],
            "lenovo": ["thinkpad", "thinkbook"],
            "dell": ["latitude", "precision"],
            "hp": ["probook", "elitebook"]
        }
    },

    "desktop": {
        "asus": ["expertcenter", "mini-pc"],
        "lenovo": ["thinkcentre", "tiny-pc"],
        "dell": ["optiplex", "vostro", "precision"]
    },

    "networking": {
        "aruba": ["switches", "poe-switches"],
        "aruba-instanton": ["cloud-managed"]
    },

    "server-storage": {
        "supermicro": ["motherboards", "barebones", "gpu-servers"],
        "asus": ["server-barebone", "workstations", "gpu-systems"],
        "lenovo": ["thinksystem", "enterprise-storage"]
    },

    "docking-station": {
        "dell": ["usb-c", "thunderbolt"],
        "lenovo": ["thinkpad-dock"],
        "hp": ["universal", "thunderbolt"]
    }
}


# ------------------------------------------------------
# LEVEL 1: CATEGORY
# /products/cpu
# ------------------------------------------------------
@pages_bp.route('/products/<category>')
def product_category(category):
    category = category.lower()

    if category not in CATEGORIES:
        return "Category not found", 404

    return render_template(
        "products.html",
        category=category
    )


# ------------------------------------------------------
# LEVEL 2: SUB CATEGORY
# /products/cpu/amd-desktop
# ------------------------------------------------------
@pages_bp.route('/products/<category>/<sub_category>')
def product_sub_category(category, sub_category):
    category = category.lower()
    sub_category = sub_category.lower()

    if category not in CATEGORIES:
        return "Category not found", 404

    if sub_category not in CATEGORIES[category]:
        return "Sub-category not found", 404

    return render_template(
        "products.html",
        category=category,
        sub_category=sub_category
    )


# ------------------------------------------------------
# LEVEL 3: SERIES
# /products/cpu/amd-desktop/ryzen
# ------------------------------------------------------
@pages_bp.route('/products/<category>/<sub_category>/<series>')
def product_series(category, sub_category, series):
    category = category.lower()
    sub_category = sub_category.lower()
    series = series.lower()

    if category not in CATEGORIES:
        return "Category not found", 404

    if sub_category not in CATEGORIES[category]:
        return "Sub-category not found", 404

    if series not in CATEGORIES[category][sub_category]:
        return "Series not found", 404

    return render_template(
        "products.html",
        category=category,
        sub_category=sub_category,
        series=series
    )


# ------------------------------------------------------
# CLEAN PRODUCT PAGE
# /cpu/ryzen/AMD-Ryzen-7-5800X
# ------------------------------------------------------
@pages_bp.route('/cpu/<series>/<name_slug>')
def clean_cpu_product(series, name_slug):
    return render_template(
        "product.html",
        series=series.lower(),
        name_slug=name_slug
    )


# ------------------------------------------------------
# STATIC PRODUCT PAGES
# ------------------------------------------------------
@pages_bp.route('/productslist/<slug>')
@pages_bp.route('/productslist/<slug>.html')
def product_page(slug):
    slug = slug.lower()
    file_path = f"productslist/{slug}.html"
    full_path = os.path.join(TEMPLATES_DIR, file_path)

    if os.path.exists(full_path):
        return render_template(file_path)

    return f"<h2>Product '{slug}' not found</h2>", 404


# ------------------------------------------------------
# NORMAL PAGES (MUST REMAIN LAST)
# ------------------------------------------------------
@pages_bp.route('/<page>')
@pages_bp.route('/<page>.html')
def load_page(page):
    if page == "productslist":
        return "Invalid page", 404

    file_path = f"{page}.html"
    full_path = os.path.join(TEMPLATES_DIR, file_path)

    if os.path.exists(full_path):
        return render_template(file_path)

    return "Page Not Found", 404
