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
# CLEAN PRODUCT SERIES URL
# Example: /products/ironwolf
# ------------------------------------------------------
@pages_bp.route('/products/<series>')
def product_series(series):
    return render_template("products.html", series=series.lower())


# ------------------------------------------------------
# BACKWARD COMPATIBILITY
# Redirect /products?series=ironwolf → /products/ironwolf
# ------------------------------------------------------
@pages_bp.route('/products')
def products_redirect():
    series = request.args.get("series")
    if series:
        return redirect(f"/products/{series.lower()}", code=301)
    return "No series specified", 400


# ------------------------------------------------------
# CLEAN CPU PRODUCT URL (PRODUCT NAME SLUG)
# Example:
#   /cpu/5000/AMD-Ryzen-5-5600
#   /cpu/9005/AMD-EPYC-7313
# ------------------------------------------------------
@pages_bp.route('/cpu/<series>/<name_slug>')
def clean_cpu_product(series, name_slug):
    """
    Loads the product.html page using a human-readable product slug
    instead of old ?id= URLs.
    """
    return render_template(
        "product.html",
        series=series.lower(),
        name_slug=name_slug
    )


# ------------------------------------------------------
# PRODUCT PAGES (Clean URL + .html)
# Priority BEFORE normal pages
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
# NORMAL PAGES (aboutus, suppliers, inquiry...)
# Supports: /aboutus  AND  /aboutus.html
#
# ⚠ IMPORTANT:
# This catch-all MUST remain LAST.
# ------------------------------------------------------
@pages_bp.route('/<page>')
@pages_bp.route('/<page>.html')
def load_page(page):
    # Safety: do not conflict with /productslist/
    if page == "productslist":
        return "Invalid page", 404

    file_path = f"{page}.html"
    full_path = os.path.join(TEMPLATES_DIR, file_path)

    if os.path.exists(full_path):
        return render_template(file_path)

    return "Page Not Found", 404
