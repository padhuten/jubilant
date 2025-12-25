# app.py
from flask import Flask
from flask_cors import CORS
from config import TEMPLATES_DIR, STATIC_DIR

# === IMPORT BLUEPRINTS ===
from routes.pages import pages_bp
from routes.products import products_bp
from routes.shortlist import shortlist_bp
from routes.forms import forms_bp
from routes.search import search_bp
from routes.fallback import fallback_bp

# ======================================================
# ✅ CREATE FLASK APP
# ======================================================
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

CORS(app)

# ======================================================
# ✅ REGISTER BLUEPRINTS (ORDER MATTERS)
# ======================================================
# Main pages
app.register_blueprint(pages_bp)

# Product APIs (CPU + HDD)
app.register_blueprint(products_bp)

# Shortlist APIs
app.register_blueprint(shortlist_bp)

# Form submissions (Contact, Inquiry, Consultation)
app.register_blueprint(forms_bp)

# Search
app.register_blueprint(search_bp)

# Fallback route (MUST stay last)
app.register_blueprint(fallback_bp)

# ======================================================
# ✅ GLOBAL ERROR HANDLERS
# ======================================================
@app.errorhandler(404)
def not_found(e):
    return (
        "<h2 style='text-align:center;color:red;margin-top:50px;'>Page Not Found (404)</h2>",
        404
    )

@app.errorhandler(500)
def server_error(e):
    return (
        "<h2 style='text-align:center;color:red;margin-top:50px;'>Server Error (500)</h2>",
        500
    )

# ======================================================
# ✅ RUN SERVER
# ======================================================
if __name__ == "__main__":
    print("🔥 Flask server running at: http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
