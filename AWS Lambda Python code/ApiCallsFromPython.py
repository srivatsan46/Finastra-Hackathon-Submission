
import requests, json
import boto3
token_url = "https://api.fusionfabric.cloud/login/v1/finastra-dev/oidc/token"

test_api_url1 = "https://api.fusionfabric.cloud/calendars/v1/"
test_api_url2 = "business-days/target-date?country=DE&currency=USD&startDate=2022-09-09&workingDaysOffset=3"


client_id = 'efe49624-3388-49da-b8a3-c7026094bb5a'
client_secret = '2b409f9d-1992-4116-83fd-bde22bf7b4f9'



#step A, B - single call with client credentials as the basic auth header - will return access_token
data = {'grant_type': 'client_credentials'}

access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

#print(access_token_response.headers)
#rint(access_token_response.text)

tokens = json.loads(access_token_response.text)

print("access token: " + tokens['access_token'])

#step B - with the returned access_token we can make as many calls as we want

print("access token: " + tokens['access_token'])

api_call_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens['access_token']}
#print(api_call_headers)

Complete_test_url = test_api_url1 + test_api_url2
print(Complete_test_url)

api_call_response = requests.get(Complete_test_url, headers=api_call_headers, verify=False)

print(api_call_response)
print(type(api_call_response))

print(api_call_response.text)
responsejson = api_call_response.json()
print(type(responsejson))
print(responsejson)
targetDate = responsejson.get('targetDate')
print(type(targetDate))
print(targetDate)

s3 = boto3.resource('s3')
s3_object = s3.Object('uploadanddownloadtestfin', 'API_test2.txt')
print(s3_object)
s3_object.metadata.update({'futurerefreshdate': targetDate})
s3_object.copy_from(CopySource={'Bucket': 'uploadanddownloadtestfin', 'Key': 'API_test.txt'}, Metadata=s3_object.metadata, MetadataDirective='REPLACE')
