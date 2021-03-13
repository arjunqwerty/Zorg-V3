import smtplib
from email.mime.text import MIMEText

def emailsend(to,mssg):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '18cc8c2ea71e43'
    password = '27abc8c416d687'

    sender_email = 'zorg123546@gmail.com'

    message = MIMEText(mssg, 'html')
    message['Subject'] = 'Zorg'
    message['From'] = sender_email
    message['To'] = str(to)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login,password)
        server.sendmail(sender_email, to, message.as_string())
