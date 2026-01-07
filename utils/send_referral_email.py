import os
import base64
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def send_referral_email(data):
    creds = Credentials(
        None,
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN"),
        client_id=os.getenv("GMAIL_CLIENT_ID"),
        client_secret=os.getenv("GMAIL_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/gmail.send"],
    )

    service = build("gmail", "v1", credentials=creds)

    msg = EmailMessage()
    msg["From"] = os.getenv("GMAIL_SENDER_EMAIL")
    msg["To"] = "abhishek.khanna@fitelo.co"
    msg["Cc"] = data["email"]
    msg["Subject"] = "Referral Amount Discrepancy – Dietician Support Request"

    msg.set_content(
f"""Hi Abhishek,

I hope you are doing well.

This email is regarding a referral amount discrepancy raised by one of our dieticians through the Fitelo Internal Support Tool.

Dietician Details:-
Email: {data['email']}

Issue Details:-
{data['description']}

The relevant screenshots related to the payment and referral sheet have been attached for your reference.

Requesting you to please review the issue and take the necessary action at your end.

Thank you for your time and support.

Regards,
Fitelo Internal Support Tool
"""
)


    # 📎 Attach screenshots
    for path in [data["payment_screenshot"], data["referral_screenshot"]]:
        with open(path, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="image",
                subtype="png",
                filename=os.path.basename(path),
            )

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()
