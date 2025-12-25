from flask import Blueprint, request, redirect, url_for, render_template

search_bp = Blueprint("search_bp", __name__)

@search_bp.route('/search')
def search():
    q = request.args.get("q", "").lower().strip()

    keywords = {
        "intel": "intel",
        "i9": "intel",
        "amd": "amd",
        "ryzen": "amd",
        "epyc": "epyc",
        "xeon": "intel",
    }

    for k, slug in keywords.items():
        if k in q:
            return redirect(f"/productslist/{slug}")

    return render_template("index.html", message="Product not found")
