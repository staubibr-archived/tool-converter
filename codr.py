import requests
import json

print("\n **************************************** getCubeMetadata **************************************** \n")

url = 'https://www150.statcan.gc.ca/t1/wds/rest/getCubeMetadata'
body = '[{"productId":35100003}]'
request = requests.post(url, data=body, headers={'Content-type': 'application/json'})
content = json.loads(request.content)

print(json.dumps(content[0]["object"], indent=4))

print("\n *************************** getDataFromCubePidCoordAndLatestNPeriods *************************** \n")

url = 'https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods'
body = '[{"productId": 35100003, "coordinate": "1.12.0.0.0.0.0.0.0.0", "latestN":3}]'
request = requests.post(url, data=body, headers={'Content-type': 'application/json'})
content = json.loads(request.content)

print(json.dumps(content[0]["object"], indent=4))
