from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import sib_api_v3_sdk
from flask_socketio import SocketIO
import threading
import time

# Initialize Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Global variables for email analytics
total_emails_sent = 0
emails_pending = 0
emails_scheduled = 0
emails_failed = 0
email_status = []

# Google Sheets API credentials
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
GOOGLE_SHEETS_CREDENTIALS = 'your json file'

# Sendinblue API initialization
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = 'sendinblue api key'  # Replace with your API key
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Authenticate Google Sheets
def authenticate_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_SHEETS_CREDENTIALS, SCOPES
    )
    client = gspread.authorize(creds)
    return client

# Function to send email using Sendinblue
def send_email(to_email, subject, body):
    global total_emails_sent, emails_failed, email_status

    # Email data for Sendinblue
    email_data = {
        "sender": {"email": "your email"},  # Replace with your email
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": f"<html><body>{body}</body></html>"
    }

    try:
        # Send email via Sendinblue API
        api_instance.send_transac_email(email_data)
        total_emails_sent += 1

        # Update email status
        for email in email_status:
            if email['email'] == to_email:
                email['status'] = 'Sent'
                email['delivery'] = 'Delivered'

        # Notify frontend
        socketio.emit('update_status', {'email': to_email, 'status': 'Sent', 'delivery': 'Delivered'})

    except sib_api_v3_sdk.rest.ApiException:
        emails_failed += 1
        for email in email_status:
            if email['email'] == to_email:
                email['status'] = 'Failed'
        socketio.emit('update_status', {'email': to_email, 'status': 'Failed', 'delivery': 'N/A'})

# Fetch Google Sheet data
def get_google_sheet_data(sheet_id, sheet_name):
    client = authenticate_google_sheets()
    spreadsheet = client.open_by_key(sheet_id)
    worksheet = spreadsheet.worksheet(sheet_name)
    return worksheet.get_all_records()

# Schedule emails with throttling
def schedule_emails(sheet_data, delay_minutes, throttle_rate):
    global emails_scheduled, email_status

    scheduler = BackgroundScheduler()

    for index, row in enumerate(sheet_data):
        email = row['email']
        subject = row['subject']
        body = row['body']

        # Add email to status list
        email_status.append({"email": email, "status": "Scheduled", "delivery": "N/A"})
        emails_scheduled += 1

        # Schedule email sending with throttling delay
        time_to_send = datetime.now() + timedelta(minutes=delay_minutes) + timedelta(seconds=(index // throttle_rate) * 60)

        scheduler.add_job(
            send_email,
            'date',
            run_date=time_to_send,
            args=[email, subject, body]
        )

    scheduler.start()

# Route: Display Input Form (First Page)
@app.route('/')
def index():
    return render_template('input_form.html')  # This shows the input form for email scheduling

# Route: Handle form submission and redirect to Dashboard
@app.route('/schedule_email', methods=['POST'])
def schedule_email():
    sheet_id = request.form['spreadsheet_id']
    sheet_name = request.form['sheet_name']
    delay_minutes = int(request.form['delay_minutes'])
    throttle_rate = int(request.form['throttle_rate'])

    sheet_data = get_google_sheet_data(sheet_id, sheet_name)
    schedule_emails(sheet_data, delay_minutes, throttle_rate)
    
    # Redirect to the dashboard after scheduling emails
    return redirect(url_for('dashboard'))

# Route: Display Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('index.html', 
                           total_sent=total_emails_sent, 
                           pending=emails_pending, 
                           scheduled=emails_scheduled, 
                           failed=emails_failed)

# Real-time analytics update
@socketio.on('connect')
def handle_connect():
    socketio.emit('initial_data', {
        "email_status": email_status,
        "total_sent": total_emails_sent,
        "pending": emails_pending,
        "scheduled": emails_scheduled,
        "failed": emails_failed
    })

if __name__ == '__main__':
    socketio.run(app, debug=True)