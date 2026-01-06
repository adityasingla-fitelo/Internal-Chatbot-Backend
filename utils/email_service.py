import os
import smtplib
from email.message import EmailMessage
from typing import Dict


def send_sales_email(data: Dict):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not smtp_email or not smtp_pass:
        raise RuntimeError("SMTP_EMAIL or SMTP_PASSWORD not set in environment")

    dietician_email = data["email"]
    description = data["description"]
    payment_path = data["payment_screenshot"]
    dashboard_path = data["dashboard_screenshot"]

    msg = EmailMessage()

    msg["Subject"] = "Sales Amount Discrepancy – Dietician Support Request"
    msg["From"] = smtp_email
    msg["To"] = "aditya.s@fitelo.co"
    msg["Cc"] = dietician_email

    html_body = f"""
<html>
  <body style="
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    color: #222;
    line-height: 1.6;
  ">

    <p>Hi Abhishek,</p>

    <p>
      I hope you are doing well.
    </p>

    <p>
      This email is regarding a <strong>sales amount discrepancy</strong> raised by one of our dieticians through the
      Fitelo Internal Support Tool.
    </p>

    <p>
      <strong>Dietician Email:</strong><br/>
      {dietician_email}
    </p>

    <p>
      <strong>Issue Details:</strong><br/>
      {description}
    </p>

    <p>
      The relevant screenshots related to the payment and sales dashboard have been attached
      for your reference.
    </p>

    <p>
      Requesting you to please review the issue and take the necessary action at your end.
    </p>

    <p>
      Thank you for your time and support.
    </p>

    <br/>

    <p>
      Regards,<br/>
      Fitelo Internal Support Tool
    </p>

  </body>
</html>
"""


    msg.set_content(
        "This email contains HTML content. Please view it in an email client that supports HTML."
    )
    msg.add_alternative(html_body, subtype="html")

    # 📎 Attach files
    for label, path in [
        ("Payment Screenshot", payment_path),
        ("Dashboard Screenshot", dashboard_path),
    ]:
        with open(path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(path)

        msg.add_attachment(
            file_data,
            maintype="image",
            subtype="png",
            filename=file_name
        )

    # 🚀 Send email
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_pass)
        server.send_message(msg)
