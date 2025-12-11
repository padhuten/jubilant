from flask import Blueprint, jsonify, request

from Products.cpu_products import cpu_products
from Products.hdd_products import hdd_products
from Products.ssd_products import ssd_products
from Products.memory_products import memory_products
from Products.monitor_products import monitor_products
from Products.laptop_products import laptop_products
from Products.desktop_products import desktop_products
from Products.networking import networking_products
from Products.server_storage import server_storage_products
from Products.docking_station import docking_station_products

from routes.shortlist import shortlist_db, get_user_id


products_bp = Blueprint("products_bp", __name__)


# --------------------------------------------------
# Helper: combine all products
# --------------------------------------------------
def all_products():
    return (
        cpu_products +
        hdd_products +
        ssd_products +
        memory_products +
        monitor_products +
        laptop_products +
        desktop_products +
        networking_products +
        server_storage_products +
        docking_station_products
    )


# --------------------------------------------------
# GET ALL PRODUCTS
# --------------------------------------------------
@products_bp.route('/api/products/all', methods=['GET'])
def get_all_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_products = []
    for product in all_products():
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_products.append(item)

    return jsonify({
        "success": True,
        "count": len(final_products),
        "products": final_products
    })


# --------------------------------------------------
# CATEGORY ENDPOINTS
# --------------------------------------------------
@products_bp.route('/api/products/cpu', methods=['GET'])
def get_cpu_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_cpu = []
    for product in cpu_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_cpu.append(item)

    return jsonify({"success": True, "count": len(final_cpu), "products": final_cpu})


@products_bp.route('/api/products/hdd', methods=['GET'])
def get_hdd_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_hdd = []
    for product in hdd_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_hdd.append(item)

    return jsonify({"success": True, "count": len(final_hdd), "products": final_hdd})


@products_bp.route('/api/products/ssd', methods=['GET'])
def get_ssd_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_ssd = []
    for product in ssd_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_ssd.append(item)

    return jsonify({"success": True, "count": len(final_ssd), "products": final_ssd})


@products_bp.route('/api/products/memory', methods=['GET'])
def get_memory_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_memory = []
    for product in memory_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_memory.append(item)

    return jsonify({"success": True, "count": len(final_memory), "products": final_memory})


@products_bp.route('/api/products/monitors', methods=['GET'])
def get_monitor_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_monitors = []
    for product in monitor_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_monitors.append(item)

    return jsonify({"success": True, "count": len(final_monitors), "products": final_monitors})


@products_bp.route('/api/products/laptops', methods=['GET'])
def get_laptop_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_laptops = []
    for product in laptop_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_laptops.append(item)

    return jsonify({"success": True, "count": len(final_laptops), "products": final_laptops})


@products_bp.route('/api/products/desktops', methods=['GET'])
def get_desktop_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_desktops = []
    for product in desktop_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_desktops.append(item)

    return jsonify({"success": True, "count": len(final_desktops), "products": final_desktops})


@products_bp.route('/api/products/networking', methods=['GET'])
def get_networking_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_networking = []
    for product in networking_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_networking.append(item)

    return jsonify({"success": True, "count": len(final_networking), "products": final_networking})


@products_bp.route('/api/products/server-storage', methods=['GET'])
def get_server_storage_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_server_storage = []
    for product in server_storage_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_server_storage.append(item)

    return jsonify({"success": True, "count": len(final_server_storage), "products": final_server_storage})


@products_bp.route('/api/products/docking', methods=['GET'])
def get_docking_products():
    user_id = get_user_id()
    user_shortlist = shortlist_db.get(user_id, [])

    final_docking = []
    for product in docking_station_products:
        item = product.copy()
        item["isShortlisted"] = item["id"] in user_shortlist
        final_docking.append(item)

    return jsonify({"success": True, "count": len(final_docking), "products": final_docking})


# --------------------------------------------------
# NEW CLEAN PRODUCT LOOKUP BY ID
# --------------------------------------------------
@products_bp.route('/api/products/<product_id>', methods=['GET'])
def get_single_product(product_id):
    product_id = product_id.lower()
    for product in all_products():
        if product["id"].lower() == product_id:
            return jsonify({"success": True, "product": product})
    return jsonify({"success": False, "error": "Product not found"}), 404


# --------------------------------------------------
# NEW CLEAN PRODUCT LOOKUP WITH CATEGORY + SERIES
# Example: /api/products/cpu/9005/AMD-EPYC-7313
# --------------------------------------------------
@products_bp.route('/api/products/cpu/<series>/<product_id>', methods=['GET'])
def get_cpu_product_details(series, product_id):
    series = series.lower()
    product_id = product_id.lower()

    for product in cpu_products:
        if product["id"].lower() == product_id:
            return jsonify({
                "success": True,
                "series": series,
                "product": product
            })

    return jsonify({"success": False, "error": "Product not found"}), 404
