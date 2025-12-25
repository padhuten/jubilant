import os
from flask import Blueprint, render_template, send_from_directory, request
from config import STATIC_DIR, TEMPLATES_DIR

fallback_bp = Blueprint("fallback_bp", __name__)


@fallback_bp.route('/<path:path>')
def fallback(path):

    # --- 1. NEVER fallback APIs ---
    if path.startswith("api/"):
        return "API endpoint not found", 404
    
    # --- 2. NEVER fallback static files ---
    if path.startswith("static/") or path.startswith("images/"):
        return send_from_directory(STATIC_DIR, path.replace("static/", ""))

    # --- 3. NEVER fallback product pages ---
    if path.startswith("productslist/"):
        return "Product page not found", 404

    # --- 4. Template path checking ---
    template_path = os.path.join(TEMPLATES_DIR, f"{path}.html")

    if os.path.exists(template_path):
        return render_template(f"{path}.html")

    # --- 5. Default to homepage ---
    return render_template("index.html")
