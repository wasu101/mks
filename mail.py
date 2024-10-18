import smtplib
from email.mime.text import MIMEText
import ssl

smtp_server = 'mail.mksjewelry.com'
smtp_port = 587
username = 'mksbkk\it-support002'
password = 'Nmlolsadd_123'
from_email = 'it-support002@mksjewelry.com'
to_email = 'worrakan_jak2541@hotmail.com'
subject = 'Test Email'
body = 'This is a test email.'

msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = from_email
msg['To'] = to_email

try:
    context = ssl._create_unverified_context()
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print('Email sent successfully.')
except smtplib.SMTPAuthenticationError:
    print('Failed to send email. Authentication error.')
except smtplib.SMTPConnectError:
    print('Failed to send email. Connection error.')
except smtplib.SMTPRecipientsRefused:
    print('Failed to send email. Recipient refused.')
except smtplib.SMTPException as e:
    print(f'Failed to send email. SMTP error: {e}')
except Exception as e:
    print(f'Failed to send email. Error: {e}')
