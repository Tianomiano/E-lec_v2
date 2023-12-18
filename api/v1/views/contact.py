from flask import Blueprint, Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

contact_bp = Blueprint('contact', __name__)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "patti tiano"
SMTP_PASSWORD = ""
EMAIL_FROM = "pattitiano6@gmail.com"
EMAIL_TO = "pattitiano6@gmail.com"

@contact_bp.route('/contact', methods=['POST'])
def send_contact_email():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400

        # Validate email format
        if not validate_email(data['email']):
            return jsonify({"error": "Invalid email format"}), 400

        # Compose email message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        msg['Subject'] = data['subject']
        msg.attach(MIMEText(data['message'], 'plain'))

        # Connect to SMTP server and send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()

        return jsonify({"message": "Email sent successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Email validation function
def validate_email(email):
    import re
    return re.match(r'^[\w\.-]+@[\w\.-]+$', email) is not None
