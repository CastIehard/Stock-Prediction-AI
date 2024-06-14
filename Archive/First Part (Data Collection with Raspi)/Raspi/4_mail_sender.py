from email.message import EmailMessage
import ssl
import smtplib
from my_config import *
import os

cwd = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(cwd, "5.1_mail_body.txt")

with open(path, "r") as file:
    body = file.read()
     
em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['subject'] = subject
em.set_content(body)

# Attach the CSV file
path = os.path.join(cwd, "3.1_data_raw.csv")
with open(path, "rb") as csv_file:
    em.add_attachment(csv_file.read(), maintype="application", subtype="octet-stream", filename="3.1_data_raw.csv")
    
context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_passwort)
    smtp.sendmail(email_sender, email_receiver, em.as_string())

if output_bool:
    print("--> Everything was sent to mail adress")
