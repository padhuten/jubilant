from flask import Blueprint, request, jsonify
from database import cur, conn
from email_service import send_email

forms_bp = Blueprint("forms_bp", __name__)

# ----------------------------------------------------
# Helper: Build premium HTML table email
# ----------------------------------------------------
def build_html_email(title: str, data):
    rows = ""
    for key, value in data.items():
        if not value:
            continue
        label = key.replace("_", " ").title()
        rows += f"""
        <tr>
            <td style="padding:10px; background:#f8fafc; font-weight:600; width:40%;">
                {label}
            </td>
            <td style="padding:10px;">
                {value}
            </td>
        </tr>
        """

    return f"""
<!DOCTYPE html>
<html>
<body style="margin:0; padding:0; background:#f4f6fb; font-family:Arial, Helvetica, sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="padding:20px;">
  <tr>
    <td align="center">
      <table width="600" cellpadding="0" cellspacing="0"
        style="background:#ffffff; border-radius:12px; box-shadow:0 10px 30px rgba(0,0,0,0.08);">

        <tr>
          <td style="background:#0b6efd; color:#ffffff; padding:18px 22px;">
            <h2 style="margin:0; font-size:18px;">{title}</h2>
          </td>
        </tr>

        <tr>
          <td style="padding:22px;">
            <table width="100%" cellpadding="0" cellspacing="0"
              style="border-collapse:collapse; font-size:14px;">
              {rows}
            </table>
          </td>
        </tr>

        <tr>
          <td style="background:#f1f5f9; padding:12px 22px; font-size:12px; color:#64748b;">
            📧 Submitted via Jubilant Tech Website
          </td>
        </tr>

      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""


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

        send_email(
    "📩 New Contact Form Submission",
    build_html_email("New Contact Form Submission", data),
    is_html=True
)

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

        send_email(
    "📩 New Consultation Request",
    build_html_email("New Consultation Request", data),
    is_html=True
)

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

        send_email(
    "📩 New Inquiry Received",
    build_html_email("New Inquiry Received", data),
    is_html=True
)

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

        send_email(
    "📩 New Inquiry Submission",
    build_html_email("New Inquiry Submission", data),
    is_html=True
)

        return jsonify({"success": True, "message": "Submission received!"})

    except Exception as e:
        print("ERR send-submit:", e)
        return jsonify({"success": False, "message": "Server error occurred"}), 500
