# bulk-email-script.py
# by Corvidae Luz Dulcey Nguyen
# version 1.0

from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import csv
import os
import smtplib
import sys
import time

# SMTP Setup
SMTP_SERVER   = "smtp.gmail.com"
SMTP_PORT     = 587     # STARTTLS PORT

# Delay config
DELAY_SECONDS = 2       # pause between sends

# Fetch email details
EMAIL_BODY_TXT = "email_body.txt"   # First line = subject, then blank line, then body
RECIPIENTS_CSV = "recipients.csv"   # Columns: email    


load_dotenv()
# Fetch values from .env
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
APP_PASSWORD  = os.environ.get("GMAIL_APP_PASSWORD")

def load_email(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    subject, separator, body = content.partition("\n\n") # Separates the subject and body into two variables.
    if not separator:
        print("email_body.txt needs a blank line between the subject and the body.")
        sys.exit(1)

    return subject.strip(), body

def load_recipients(path):
    recipients = []
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get("email", "").strip()
            if email:
                recipients.append({"email": email})
    
    return recipients

def build_message(sender, to, subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    return msg

def main():
    if not GMAIL_ADDRESS or not APP_PASSWORD:
        print("GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set in .env")
        sys.exit(1)

    subject, body_template = load_email(EMAIL_BODY_TXT)
    recipients = load_recipients(RECIPIENTS_CSV)

    if not recipients:
        print(f"No recipients found in {RECIPIENTS_CSV}")
        sys.exit(1)

    print(f"Loaded {len(recipients)} recipients. Sending...")

    results = [] # Result of each email send will be stored here and then exported to send_log.csv

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(GMAIL_ADDRESS, APP_PASSWORD)

        for i, r in enumerate(recipients, start=1):
            body = body_template
            msg = build_message(GMAIL_ADDRESS, r["email"], subject, body)

            try:
                server.sendmail(GMAIL_ADDRESS, r["email"], msg.as_string())
                print(f"[{i}/{len(recipients)}] Sent to {r['email']}")
                results.append({"email": r["email"], "status": "sent"})
            except Exception as e:
                print(f"[{i}/{len(recipients)}] FAILED for {r['email']}: {e}")
                results.append({"email": r["email"], "status": f"failed: {e}"})

            time.sleep(DELAY_SECONDS)

    with open("send_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["email", "status"])
        writer.writeheader()
        writer.writerows(results)

    sent = sum(1 for r in results if r["status"] == "sent")
    print(f"\nDone. {sent}/{len(recipients)} sent successfully.")
    print("See send_log.csv for full details.")

if __name__ == "__main__":
    main()