import boto3
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from botocore.exceptions import ClientError
import base64
import json
import os
import urllib
from urllib import request, parse

# connect to s3 - assuming your creds are all set up and you have boto3 installed
s3 = boto3.resource('s3')

# identify the bucket - you can use prefix if you know what your bucket name starts with
#for bucket in s3.buckets.all():
#    print(bucket.name)

# get the bucket
bucket = s3.Bucket('uploadanddownloadtestfin')

# use loop and count increment

count_obj = 0
for i in bucket.objects.all():
    count_obj = count_obj + 1
print(count_obj)

s3_client = boto3.client('s3')
paginator = s3_client.get_paginator('list_objects_v2')
result = paginator.paginate(Bucket='uploadanddownloadtestfin')

for page in result:
    if "Contents" in page:
        for key in page["Contents"]:
            keyString = key["Key"]
            print(keyString)
            metadata = s3_client.head_object(Bucket='uploadanddownloadtestfin',
                                             Key=keyString, )
            CustomeMetaData = metadata.get('Metadata')
            FutureRefeshDate = CustomeMetaData.get('futurerefreshdate')
            ConvertedFutureRefeshDate = datetime.strptime(FutureRefeshDate, '%Y-%m-%d').date()
            print(type(ConvertedFutureRefeshDate))
            print(ConvertedFutureRefeshDate)
            CurrentDate = datetime.now().date()
            print(type(CurrentDate))
            print(CurrentDate)
            ToMobileNumber = CustomeMetaData.get('useridentifier')
            print(ToMobileNumber)

            if CurrentDate < ConvertedFutureRefeshDate:
                SendSms = 1
            else:
                SendSms = 0

            if SendSms == 1:
                print("SMS with s3 object url will be sent through Twilio")

                TWILIO_SMS_URL = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json"
                to_number = ToMobileNumber
                from_number = +447445032769
                body = "Please update your KYC details uploaded in Finastra app"
                TWILIO_ACCOUNT_SID = "AC71241083dba15e17d5b78e6779acaf14"
                TWILIO_AUTH_TOKEN  = "f5abe26b44244ecd96e8fad051d71b6b"

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
                     print(keyString)
                else:
                     print("sms sent")
                     print(keyString)


