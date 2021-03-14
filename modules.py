import smtplib
from email.mime.text import MIMEText
#import email, ssl
#import imaplib

def emailsend(to,mssg):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '18cc8c2ea71e43'
    password = '27abc8c416d687'
    #username_mail = 'zorg123546@gmail.com'
    #password = 'zorg87654321'

    sender_email = 'zorg123546@gmail.com'

    message = MIMEText(mssg, 'html')
    message['Subject'] = 'Zorg'
    message['From'] = sender_email
    message['To'] = str(to)

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login,password)
        server.sendmail(sender_email, to, message.as_string())

'''
def emailrecieve(area_emer):
    EMAIL = 'zorg45365@gmail.com'
    PASSWORD = 'zorg12345678'
    SERVER = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    status, data = mail.search(None, 'ALL')
    mail_ids = []
    l=[]
    d={}
    a=a1=0
    b=b1=10000
    for block in data:
        mail_ids += block.split()
    for i in mail_ids:
        status, data = mail.fetch(i, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                message = email.message_from_bytes(response_part[1])
                mail_from = message['from']
                mail_subject = message['subject']
                if message.is_multipart():
                    mail_content = ''
                    for part in message.get_payload():
                        if part.get_content_type() == 'text/plain':
                            mail_content += part.get_payload()
                else:
                    mail_content = message.get_payload()
                d[a]=f'{mail_content}'
                d[b]=f'{mail_subject}'
                a+=1
                b+=1
    for j in range(len(mail_ids)):
        l1=[]
        l1.append(d[b1])
        s=d[a1]
        s.lower()
        n=s.find('+')
        s1=''
        s2=''
        for i in range(n):
            s1+=s[i]
        u=s.find('$')
        for i in range(n+1,u):
            s2+=s[i]
        l1.append(s1)
        l1.append(s2)
        l.append(l1)
        a1+=1
        b1+=1
    req_hosp_emails=[]
    for i in range(len(l)):
        if l[i][1]==area_emer:
            req_hosp_emails.append(l[i][2])
    return req_hosp_emails
'''