from flask import Blueprint, request, jsonify
from database import cur, conn
from email_service import send_email

forms_bp = Blueprint("forms_bp", __name__)


# ----------------------------------------------------
# Helper: Convert form dict → readable email message
# ----------------------------------------------------
def format_email(data):
    return "\n".join(f"{key}: {value}" for key, value in data.items())


# ----------------------------------------------------
# Helper: Safe checkbox handling
# ----------------------------------------------------
def checkbox(value):
    return value == "on"


# ----------------------------------------------------
# CONTACT FORM
# ----------------------------------------------------
@forms_bp.route("/send-contact", methods=["POST"])
def send_contact():
    try:
        data = request.form

        cur.execute("""
            INSERT INTO contact_form 
            (product_name, quantity, company_name, email, phone, inquiry_details, get_notified)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("product_name"),
            data.get("quantity"),
            data.get("company_name"),
            data.get("email"),
            data.get("phone"),
            data.get("inquiry_details"),
            checkbox(data.get("get_notified"))
        ))
        conn.commit()

        send_email("New Contact Form Submission", format_email(data))
        return jsonify({"success": True, "message": "Contact form submitted successfully!"})

    except Exception as e:
        print("ERR send-contact:", e)
        return jsonify({"success": False, "message": "Server error occurred"}), 500



# ----------------------------------------------------
# CONSULTATION FORM
# ----------------------------------------------------
@forms_bp.route("/send-consultation", methods=["POST"])
def send_consultation():
    try:
        data = request.form

        cur.execute("""
            INSERT INTO consultations 
            (product_name, quantity, company_name, email, phone, inquiry_details, notify_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("product_name"),
            data.get("quantity"),
            data.get("company_name"),
            data.get("email"),
            data.get("phone"),
            data.get("inquiry_details"),
            checkbox(data.get("notify_price"))
        ))
        conn.commit()

        send_email("New Consultation Request", format_email(data))
        return jsonify({"success": True, "message": "Consultation request sent!"})

    except Exception as e:
        print("ERR send-consultation:", e)
        return jsonify({"success": False, "message": "Server error occurred"}), 500



# ----------------------------------------------------
# INQUIRY POPUP MODAL
# ----------------------------------------------------
@forms_bp.route("/send-inquiry", methods=["POST"])
def send_inquiry():
    try:
        data = request.form

        cur.execute("""
            INSERT INTO inquiries (name, email, phone, product, quantity)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get("name"),
            data.get("email"),
            data.get("phone"),
            data.get("product"),
            data.get("quantity")
        ))
        conn.commit()

        send_email("New Inquiry Received", format_email(data))
        return jsonify({"success": True, "message": "Inquiry received successfully!"})

    except Exception as e:
        print("ERR send-inquiry:", e)
        return jsonify({"success": False, "message": "Server error occurred"}), 500



# ----------------------------------------------------
# BIG SUBMISSION FORM (larger inquiry form)
# ----------------------------------------------------
@forms_bp.route("/send-submit", methods=["POST"])
def send_submit():
    try:
        data = request.form

        cur.execute("""
            INSERT INTO inquiry_submissions 
            (product_name, quantity, company_name, email, phone, inquiry_details, notify_prices)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get("product-name"),
            data.get("quantity"),
            data.get("company-name"),
            data.get("email-address"),
            data.get("phone"),
            data.get("inquiry-details"),
            checkbox(data.get("notify-prices"))
        ))
        conn.commit()

        send_email("New Inquiry Submission", format_email(data))
        return jsonify({"success": True, "message": "Submission received!"})

    except Exception as e:
        print("ERR send-submit:", e)
        return jsonify({"success": False, "message": "Server error occurred"}), 500
