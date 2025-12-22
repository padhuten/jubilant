import os
from flask import Blueprint, render_template, send_from_directory
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
    return send_from_directory(
        os.path.join(STATIC_DIR, "images"),
        filename
    )


# ------------------------------------------------------
# PRODUCT TAXONOMY (MASTER)
# ------------------------------------------------------
CATEGORIES = {
    "cpu": {
        "amd-server": ["turin-9005-series", "9004", "7003", "8004", "4004", "4005"],
        "amd-desktop": ["ryzen", "ryzen-pro"],
        "intel-desktop": ["i9", "i7", "i5", "i3"]
    },

    "hdd": {
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

    "monitor": {
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
        "dell": ["optiplex", "vostro", "precision"],
        "hp": ["prodesk", "elitedesk", "z-workstation"]
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

# Categories that only have 2 levels (no series)
NO_SERIES_CATEGORIES = ["memory", "networking", "docking-station"]

# ✅ LEVEL 3: SERIES WITH PRODUCT ID (4-LEVEL URL)
# /products/cpu/amd-desktop/ryzen/9700x
# /products/ssd/samsung/980-pro/ssd-samsung-980-pro-1tb
@pages_bp.route('/products/<category>/<sub_category>/<series>/<product_id>')
def product_series_detail(category, sub_category, series, product_id):
    return render_template(
        "product.html",
        product_id=product_id
    )

# ✅ LEVEL 2: SUB CATEGORY WITH PRODUCT ID (3-LEVEL URL) - FOR 2-LEVEL CATEGORIES
# /products/memory/crucial/ram-crucial-8gb-ddr4-udimm
# /products/networking/aruba/sw-aruba-12345
# /products/docking-station/dell/dock-dell-usb-c-1
@pages_bp.route('/products/<category>/<sub_category>/<product_id>')
def product_sub_category_detail(category, sub_category, product_id):
    category = category.lower()
    
    # This should only match 2-level categories
    if category in NO_SERIES_CATEGORIES:
        return render_template(
            "product.html",
            product_id=product_id
        )
    
    # If it's a 3-level category, treat sub_category as series and product_id as the actual product_id
    # But first check if this might be a series listing page
    # by checking if the CATEGORIES structure has this sub_category as a series
    if category in CATEGORIES and sub_category.lower() in CATEGORIES[category]:
        # It's a valid sub_category, so this is the series listing page
        return render_template(
            "products.html",
            category=category.lower(),
            sub_category=sub_category.lower()
        )
    
    # Otherwise, treat it as a product detail page for a 4-level URL
    return render_template(
        "product.html",
        product_id=product_id
    )


# ✅ LEVEL 2: SUB CATEGORY (LIST PAGE)
# /products/memory/crucial
# /products/cpu/amd-desktop
@pages_bp.route('/products/<category>/<sub_category>')
def product_sub_category(category, sub_category):
    return render_template(
        "products.html",
        category=category.lower(),
        sub_category=sub_category.lower()
    )


# ✅ LEVEL 1: CATEGORY (LIST PAGE)
# /products/memory
# /products/cpu
@pages_bp.route('/products/<category>')
def product_category(category):
    category = category.lower()

    if category not in CATEGORIES:
        return "Category not found", 404

    return render_template("products.html", category=category)


# ✅ LEVEL 3: SERIES (LIST PAGE) - For 4-level categories
# /products/ssd/samsung/980-pro
# /products/cpu/amd-desktop/ryzen
@pages_bp.route('/products/<category>/<sub_category>/<series>')
def product_series(category, sub_category, series):
    return render_template(
        "products.html",
        category=category.lower(),
        sub_category=sub_category.lower(),
        series=series.lower()
    )


# ✅ UNIVERSAL PRODUCT DETAIL (MUST BE LAST)
# /products/**/product-id
# This is a fallback for any product detail URL
@pages_bp.route('/products/<path:slug>')
def universal_product_detail(slug):
    parts = slug.split('/')

    # product id is ALWAYS last
    product_id = parts[-1]

    return render_template(
        "product.html",
        product_id=product_id
    )


# ✅ STATIC PRODUCT PAGES
# ✅ STATIC PRODUCT PAGES
@pages_bp.route('/productslist/<slug>')
@pages_bp.route('/productslist/<slug>.html')
def product_page(slug):
    slug = slug.lower()
    file_path = f"productslist/{slug}.html"
    full_path = os.path.join(TEMPLATES_DIR, file_path)

    if os.path.exists(full_path):
        return render_template(file_path)

    return f"<h2>Product '{slug}' not found</h2>", 404


# ✅ NORMAL PAGES (MUST REMAIN LAST)
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