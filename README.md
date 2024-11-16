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
