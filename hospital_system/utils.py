import requests

EMAIL_SERVICE_URL = "http://localhost:3000/send-email"

def trigger_email(action, email, name):
    payload = {
        "action": action,
        "email": email,
        "name": name
    }

    try:
        requests.post(EMAIL_SERVICE_URL, json=payload, timeout=2)
    except Exception:
        pass
