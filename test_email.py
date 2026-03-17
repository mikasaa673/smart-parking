"""
test_email.py  --  run this to diagnose email sending issues.
Usage: python test_email.py your@email.com
"""
import os, sys, ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAIL_USER     = os.getenv('MAIL_USER', '')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')

if not MAIL_USER:
    MAIL_USER     = 'spamlol439@gmail.com'
    MAIL_PASSWORD = 'hixpxubhbcqklind'
    print(f"[INFO] Env vars not set, using hardcoded credentials: {MAIL_USER}")
else:
    print(f"[INFO] Using env-var credentials: {MAIL_USER}")

recipient = sys.argv[1] if len(sys.argv) > 1 else MAIL_USER
print(f"[INFO] Sending test email to: {recipient}")

try:
    msg = MIMEMultipart()
    msg['From']    = f'SmartPark <{MAIL_USER}>'
    msg['To']      = recipient
    msg['Subject'] = '[SmartPark] SMTP Test'
    msg.attach(MIMEText(
        'If you receive this, email is working correctly!\n\n-- SmartPark Team',
        'plain', 'utf-8'
    ))

    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587, timeout=20) as smtp:
        smtp.ehlo()
        smtp.starttls(context=context)
        smtp.login(MAIL_USER, MAIL_PASSWORD)
        smtp.send_message(msg)

    print("[OK] Email sent successfully!")
except smtplib.SMTPAuthenticationError as e:
    print(f"[FAIL] Authentication error: {e}")
    print("       Check your Gmail App Password and that 2FA is enabled.")
except Exception as e:
    print(f"[FAIL] Unexpected error: {e}")
