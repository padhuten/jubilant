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
    return send_from_directory(os.path.join(STATIC_DIR, "images"), filename)


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
# ------------------------------------------------------
@pages_bp.route('/<page>')
@pages_bp.route('/<page>.html')
def load_page(page):
    # Safety: avoid catching /productslist/
    if page == "productslist":
        return "Invalid page", 404

    file_path = f"{page}.html"
    full_path = os.path.join(TEMPLATES_DIR, file_path)

    if os.path.exists(full_path):
        return render_template(file_path)

    return "Page Not Found", 404
