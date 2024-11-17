# CustomEmailSender
A Flask-based application to schedule and send emails using Google Sheets as the data source. 
This project supports email throttling, analytics, and real-time updates via a dashboard.
# Features
Schedule emails using data from Google Sheets.

Real-time analytics: View total emails sent, failed, pending, and scheduled.

Throttling support: Limit the number of emails sent per minute.

Integration with Sendinblue as the Email Service Provider (ESP).

# Setup and Configuration Instructions
# 1. Prerequisites
   
Install Python (version 3.7+).

Install pip for package management.

A Sendinblue account (to obtain an API key).

A Google Cloud account with access to the Google Sheets API.
# 2. Install Dependencies
Create and activate a virtual environment:
python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

Install required Python packages:

pip install -r requirements.txt
# 3. Obtain API Keys
Sendinblue API Key:

Log in to your Sendinblue account.

Navigate to SMTP & API under the settings.

Generate an API key and copy it.

Google Sheets API Key:

Go to the Google Cloud Console.

Create a new project or use an existing one.

Enable the Google Sheets API and Google Drive API.

Create credentials for a service account and download the JSON key file.

Save the JSON key file in the project directory
# 4.Configuartion
create .env file for storing secutity keys
# Usage Instructions
# 1. Configure Email Scheduling
Start the application

open the application in http://127.0.0.1:5000 browser
# Input Form Fields:
1.Spreadsheet ID: The unique ID of your Google Sheet (found in the URL).

2.Sheet Name: The specific sheet name containing email data.

3.Delay (Minutes): The time delay before emails start sending.

4.Throttle Rate: Maximum emails to send per minute.

Click "Schedule Emails" to start the email scheduling process.
# 2. Monitor Emails
Navigate to the dashboard to view:

Total emails sent.

Pending emails.

Emails scheduled.

Failed emails.
# How Email Scheduling Works
1.The app fetches email details from the provided Google Sheet.

2.Emails are scheduled with throttling to control the send rate.

3.Real-time analytics updates are sent to the dashboard using Socket.IO.
# Email Throttling
Throttle Rate: Specifies the number of emails to send per minute.

Delays between batches ensure compliance with ESP limits.

Video Link:

https://github.com/user-attachments/assets/afaf80de-579b-4780-9545-8b09b118c674
