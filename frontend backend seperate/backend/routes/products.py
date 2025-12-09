from flask import Blueprint, jsonify, request
from Products.cpu_products import cpu_products
from Products.hdd_products import hdd_products
from Products.ssd_products import ssd_products
from routes.shortlist import shortlist_db, get_user_id

products_bp = Blueprint("products_bp", __name__)


# --------------------------------------------------
# GET ALL PRODUCTS (CPU + any category you add later)
# --------------------------------------------------
@products_bp.route('/api/products/all', methods=['GET'])
def get_all_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_products = []

    # ✅ Add CPU products
    for product in cpu_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_products.append(item)

    # ✅ Add HDD products
    for product in hdd_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_products.append(item)
        
    # add SSD products
    
    for product in ssd_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_products.append(item)
        
        
        return jsonify({
        "success": True,
        "count": len(final_products),
        "products": final_products
    })



# --------------------------------------------------
# GET HDD PRODUCTS ONLY
# --------------------------------------------------
@products_bp.route('/api/products/hdd', methods=['GET'])
def get_hdd_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_hdd = []
    for product in hdd_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_hdd.append(item)

    return jsonify({
        "success": True,
        "count": len(final_hdd),
        "products": final_hdd
    })
