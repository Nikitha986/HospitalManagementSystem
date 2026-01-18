import json
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "yourgmail@gmail.com"
SMTP_PASS = "your_app_password"   # Gmail App Password

def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, to_email, msg.as_string())
    server.quit()

def send(event, context):
    data = json.loads(event["body"])

    action = data.get("action")
    email = data.get("email")
    name = data.get("name")

    if action == "SIGNUP_WELCOME":
        subject = "Welcome to HMS"
        body = f"Hello {name},\n\nWelcome to Hospital Management System."
 
    elif action == "BOOKING_CONFIRMATION":
        subject = "Appointment Confirmed"
        body = f"Hello {name},\n\nYour appointment has been confirmed."

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid action"})
        }

    send_email(email, subject, body)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Email sent"})
    }
