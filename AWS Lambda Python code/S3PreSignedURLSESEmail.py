import boto3
import logging
from datetime import datetime
from botocore.exceptions import ClientError
import base64
import json
import os
import urllib
from urllib import request, parse
from flask import Flask, render_template





#def create_presigned_url(bucket_name, object_name, expiration=3600):
"""
Generate a presigned URL to share an S3 object

:param bucket_name: string
:param object_name: string
:param expiration: Time in seconds for the presigned URL to remain valid
:return: Presigned URL as string. If error, returns None.
"""
s3_client = boto3.client('s3')

response = s3_client.generate_presigned_url('get_object',Params={'Bucket': 'uploadanddownloadtestfin','Key': '8412018697_Error.docx'},ExpiresIn=600)

# Generate a presigned URL for the S3 object

# The response contains the presigned URL
print(response)


SENDER = "srivatsan46@gmail.com"
RECIPIENT = "srivatsanbharadwaj1@gmail.com"
AWS_REGION = "ap-south-1"
SUBJECT = "Requested Document"
BODY_TEXT = ("Document URL is:" + response)

BODY_HTML = """<html>
 <head></head>
 <body>
    <p>
     <h1><a href="%s">Document URL is </a></h1>
    </p>
 </body>
 </html>
             """%(response)

# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses', region_name=AWS_REGION)

# Try to send the email.
try:
    # Provide the contents of the email.
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,
        # If you are not using a configuration set, comment or delete the
        # following line
        # ConfigurationSetName=CONFIGURATION_SET,
    )
# Display an error if something goes wrong.
except ClientError as e:
    print(e.response['Error']['Message'])
else:
    print("Email sent! Message ID:"),
    print(response['MessageId'])

