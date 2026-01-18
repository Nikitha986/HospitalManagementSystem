

import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def get_doctor_token_path(doctor):
    # Store each doctor's token as token_{doctor_id}.json
    return os.path.join(os.path.dirname(__file__), f'token_{doctor.id}.json')

def get_google_service_for_doctor(doctor):
    raise Exception("GOOGLE CALENDAR DEBUG: This code is running.")
    creds = None
    token_path = get_doctor_token_path(doctor)
    creds_path = os.path.join(os.path.dirname(__file__), 'client_secret.json')
    if not os.path.exists(creds_path):
        print(f"[ERROR] client_secret.json NOT FOUND at: {creds_path}")
        raise FileNotFoundError(f"client_secret.json not found at {creds_path}")
    if os.path.exists(token_path):
        print(f"[DEBUG] Found token file for doctor: {token_path}")
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        print(f"[DEBUG] No valid token for doctor {doctor.id}, starting OAuth flow...")
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print(f"[DEBUG] Saved new token for doctor: {token_path}")
    service = build('calendar', 'v3', credentials=creds)
    print(f"[DEBUG] Google Calendar service built for doctor {doctor.id}")
    return service

def sync_event_to_google(slot):
    """
    Create a Google Calendar event for the given slot (booking).
    Each doctor has their own Google Calendar (per-doctor account).
    """
    try:
        print("[DEBUG] sync_event_to_google called for slot:", slot)
        doctor = slot.doctor
        print(f"[DEBUG] Doctor: {doctor} (ID: {doctor.id})")
        service = get_google_service_for_doctor(doctor)
        print("[DEBUG] Google service obtained.")
        calendar_id = 'primary'  # Each doctor uses their own primary calendar
        start_dt = datetime.datetime.combine(slot.date, slot.start_time)
        end_dt = datetime.datetime.combine(slot.date, slot.end_time)
        patient_name = slot.is_booked and slot.booking_set.first().patient.username or ''
        event = {
            'summary': f"Appointment: Dr. {doctor.username} & {patient_name}",
            'description': f"Doctor: Dr. {doctor.username}\nPatient: {patient_name}",
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': 'UTC',
            },
        }
        print("[DEBUG] Creating event:", event)
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print("[DEBUG] Google Calendar event created:", created_event)
        # Optionally store event ID in slot or booking
        # slot.google_event_id = created_event['id']
        # slot.save()
    except Exception as e:
        print("[ERROR] Google Calendar sync failed:", e)
