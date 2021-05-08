import os
import re
import csv
import time
import json
import sys
import copy
import pdb
import time
import smtplib
import sqlalchemy
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from pydocumentdb import document_client
from sqlalchemy.dialects import postgresql 

# errorMap is a dictionary that has all the error entries of the dataset

errorMap = {}
def insertError(errorName, primary_id, id):
    if errorName not in errorMap.keys():
        errorMap[errorName] = [(primary_id, id)]
    else:
        errorMap[errorName].append((primary_id, id))
        
    
#### PART 1: Converting the dictionary into a csv:

csv_columns = ['ErrorName', 'PrimaryKey']
csv_file = "daily_report.csv"
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
    writer.writeheader()
    for msg, items in errorMap.items():
        [writer.writerow({"ErrorName": msg, "PrimaryKey": item}) for item in items]
# The above code created a csv file called "daily_report.csc"


#### PART 2: Sending this csv (only if generated) to my email

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

SUBJECT = 'Daily Report'
FILENAME = 'daily_report.csv'
FILEPATH = './daily_report.csv'
MY_EMAIL = '<sender>@gmail.com'
MY_PASSWORD = 'mypassword'
TO_EMAIL = '<sender>@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

msg = MIMEMultipart()
msg['From'] = MY_EMAIL
msg['To'] = COMMASPACE.join([TO_EMAIL])
msg['Subject'] = SUBJECT

part = MIMEBase('application', "octet-stream")
part.set_payload(open(FILEPATH, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=FILENAME)  # or
# part.add_header('Content-Disposition', 'attachment; filename="attachthisfile.csv"')
msg.attach(part)

smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(MY_EMAIL, MY_PASSWORD)
smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
smtpObj.quit()
    
    
