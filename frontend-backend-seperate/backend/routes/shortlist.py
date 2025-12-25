from flask import Blueprint, request, jsonify
from Products.cpu_products import cpu_products

# ------------------------------------------------------------
# BLUEPRINT
# ------------------------------------------------------------
shortlist_bp = Blueprint("shortlist_bp", __name__)

# ------------------------------------------------------------
# TEMPORARY IN-MEMORY SHORTLIST STORAGE
# (Replace with MySQL later)
# ------------------------------------------------------------
shortlist_db = {
    "user-123": ["cpu-101", "cpu-106", "cpu-109"]
}

def get_user_id():
    """Simulated logged-in user."""
    return "user-123"


# ------------------------------------------------------------
# 1. TOGGLE SHORTLIST (ADD / REMOVE)
# ------------------------------------------------------------
@shortlist_bp.route('/api/shortlist/toggle', methods=['POST'])
def toggle_shortlist():
    user_id = get_user_id()
    data = request.json or {}

    product_id = data.get("productId")
    action = data.get("action")

    if not product_id or action not in ("add", "remove"):
        return jsonify({"success": False, "message": "Invalid request"}), 400

    # Always ensure user list exists
    user_list = shortlist_db.setdefault(user_id, [])

    if action == "add":
        if product_id not in user_list:
            user_list.append(product_id)
            return jsonify({"success": True, "message": "Added to shortlist"})
        return jsonify({"success": True, "message": "Already in shortlist"})

    # Remove item
    if product_id in user_list:
        user_list.remove(product_id)

    return jsonify({"success": True, "message": "Removed from shortlist"})


# ------------------------------------------------------------
# 2. FILTER SHORTLISTED PRODUCTS
# ------------------------------------------------------------
@shortlist_bp.route('/api/shortlist/filter', methods=['POST'])
def filter_shortlist():
    user_id = get_user_id()
    filters = request.json or {}

    # Fetch user's saved shortlist
    user_ids = shortlist_db.get(user_id, [])

    # Get matching products from CPU list
    shortlisted_items = [p.copy() for p in cpu_products if p["id"] in user_ids]

    final = []
    for p in shortlisted_items:
        # Apply brand filter
        brands_filter = filters.get("brands", [])
        if brands_filter and p.get("brand") not in brands_filter:
            continue

        p["isShortlisted"] = True
        final.append(p)

    return jsonify({"success": True, "products": final})
