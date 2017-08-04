import requests
import base64
import json

keyFile = open("keys.json", "r")
keys = json.loads(keyFile.read())
keyFile.close()

key, secret, target = keys["key"], keys["secret"], keys["url"]

encoded = base64.b64encode(key + ":" + secret)

payload = {"grant_type":"client_credentials",}
headers = {"Authorization": "Basic " + encoded, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",}

r = requests.post(target, headers = headers, data = payload, verify = False)
results = r.json()

keys["token_type"], keys["access_token"] = results["token_type"], results["access_token"]

file = open("keys.json", "w")
file.write(json.dumps(keys))
file.close()