import smtplib, ssl
from email.mime.text import MIMEText
import email
import imaplib

def emailsend(to,mssg):
    smtp_ssl_host = 'smtp.gmail.com'
    smtp_ssl_port = 465
    username = 'zorg123546@gmail.com'
    password = 'zorg87654321'

    from_addr = 'zorg123546@gmail.com'
    to_addrs = to

    message = MIMEText(mssg)
    message['subject'] = username
    message['from'] = from_addr
    message['to'] = ''.join(to_addrs)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()

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
