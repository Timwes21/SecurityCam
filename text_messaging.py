import smtplib
from email.mime.text import MIMEText

def send_sms_via_email(phone_number, carrier_gateway, message):
    sender_email = "secureitycam@yahoo.com"
    sender_password = "thisisapassword"
    recipient_email = f"{phone_number}@{carrier_gateway}"

    msg = MIMEText(message)
    msg["From"] = "Security Camera"
    msg["To"] = recipient_email
    msg["Subject"] = "SMS Message"

    with smtplib.SMTP_SSL("smtp.mail.yahoo.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Message sent to {recipient_email}")

# Example usage
send_sms_via_email("7726210972", "tmomail.net", "Hello from Python!")


# Verizon: <number>@vtext.com
# AT&T: <number>@txt.att.net
# T-Mobile: <number>@tmomail.net