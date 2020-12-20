import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import base64
import json
import os
import urllib
from urllib import request, parse
import requests
s3_client = boto3.client('s3')
metadata = s3_client.head_object(Bucket='uploadanddownloadtestfin', Key='8412018697_Error.docx', )
CustomeMetaData = metadata.get('Metadata')
FutureRefeshDate = CustomeMetaData.get('futurerefreshdate')
ConvertedFutureRefreshDate = datetime.strptime(FutureRefeshDate, '%Y-%m-%d').date()
print(type(ConvertedFutureRefreshDate))
print(ConvertedFutureRefreshDate)

CurrentDate = datetime.now().date()
print(type(CurrentDate))

print(CurrentDate)

if CurrentDate > ConvertedFutureRefreshDate:
    print("Invoke Lambda to send notification")
    SendEmail = 1
    SendSms = 1

else:
    print("Dont need to invoke Lambda")
    SendEmail = 0
    SendSms = 0

if SendEmail == 1:
        print("Email with s3 object URL will be sent through AWS SES")
        SENDER = "srivatsan46@gmail.com"
        RECIPIENT = "hivrale.sachin@gmail.com"
        AWS_REGION = "ap-south-1"
        SUBJECT = "Please update your KYC details"
        BODY_TEXT = ("Please update your KYC details uploaded in Finastra app"
                     )

        BODY_HTML = """<html>
         <head></head>
         <body>
           <h1>Please update your KYC details uploaded in Finastra app</h1>
           <p>
             <h1>Please update your KYC details uploaded in Finastra app</h1></p>
         </body>
         </html>
                     """

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
else:
    print("Email with s3 object URL will not be sent through AWS SES")

if SendSms == 1:
    print("SMS with s3 object url will be sent through Twilio")

    TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
    to_number = +919689553981
    print(to_number)
    from_number = +447492881392
    body = "Please update your KYC details uploaded in Finastra app"
    TWILIO_ACCOUNT_SID = "AC49df166ac7ff3b13e9331bfbfbc75a2c"
    TWILIO_AUTH_TOKEN  = "64968fc43b892f6aca9c5ffe100edefd"

    if not TWILIO_ACCOUNT_SID:
        print("Unable to access Twilio Account SID.")
    elif not TWILIO_AUTH_TOKEN:
        print("Unable to access Twilio Auth Token.")
    elif not to_number:
        print("The function needs a 'To' number in the format +12023351493")
    elif not from_number:
         print("The function needs a 'From' number in the format +19732644156")
    elif not body:
         print("The function needs a 'Body' message to send.")

    # insert Twilio Account SID into the REST API URL
    populated_url = TWILIO_SMS_URL.format(TWILIO_ACCOUNT_SID)
    post_params = {"To": to_number, "From": from_number, "Body": body}

    # encode the parameters for Python's urllib
    data = parse.urlencode(post_params).encode()
    req = request.Request(populated_url)

    # add authentication header to request based on Account SID + Auth Token
    authentication = "{}:{}".format(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    base64string = base64.b64encode(authentication.encode('utf-8'))
    req.add_header("Authorization", "Basic %s" % base64string.decode('ascii'))

    try:

        with request.urlopen(req, data) as f:
           print("Twilio returned {}".format(str(f.read().decode('utf-8'))))
    except ClientError as e:
           print(e.response['Error']['Message'])
    else:
           print("sms sent")


