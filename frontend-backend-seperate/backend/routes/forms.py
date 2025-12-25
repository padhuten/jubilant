from flask import Blueprint, request, jsonify
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
    data = request.form

    email_sent = send_email(
        "📩 New Contact Form Submission",
        build_html_email("New Contact Form Submission", data),
        is_html=True
    )

    if not email_sent:
        return jsonify({"success": False, "message": "Failed to send contact form"}), 500

    return jsonify({"success": True, "message": "Contact form submitted successfully!"})


# ----------------------------------------------------
# CONSULTATION FORM
# ----------------------------------------------------
@forms_bp.route("/send-consultation", methods=["POST"])
def send_consultation():
    data = request.form

    email_sent = send_email(
        "📩 New Consultation Request",
        build_html_email("New Consultation Request", data),
        is_html=True
    )

    if not email_sent:
        return jsonify({"success": False, "message": "Failed to send consultation request"}), 500

    return jsonify({"success": True, "message": "Consultation request sent!"})


# ----------------------------------------------------
# INQUIRY POPUP MODAL
# ----------------------------------------------------
@forms_bp.route("/send-inquiry", methods=["POST"])
def send_inquiry():
    data = request.form

    email_sent = send_email(
        "📩 New Inquiry Received",
        build_html_email("New Inquiry Received", data),
        is_html=True
    )

    if not email_sent:
        return jsonify({"success": False, "message": "Failed to send inquiry"}), 500

    return jsonify({"success": True, "message": "Inquiry received successfully!"})


# ----------------------------------------------------
# BIG SUBMISSION FORM (larger inquiry form)
# ----------------------------------------------------
@forms_bp.route("/send-submit", methods=["POST"])
def send_submit():
    data = request.form

    email_sent = send_email(
        "📩 New Inquiry Submission",
        build_html_email("New Inquiry Submission", data),
        is_html=True
    )

    if not email_sent:
        return jsonify({"success": False, "message": "Failed to send submission"}), 500

    return jsonify({"success": True, "message": "Submission received!"})
