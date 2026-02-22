import requests
import os
import json

API_KEY = os.environ.get("CITO_API_KEY")
if not API_KEY:
    print("CITO_API_KEY is not set!")
    exit(1)

URL = "https://api.citoapi.com/v1/cod/cdl/schedule"
headers = {"x-api-key": API_KEY}

response = requests.get(URL, headers=headers)
print("Status Code:", response.status_code)

try:
    data = response.json()
    print("Full API Response:")
    print(json.dumps(data, indent=2))
except Exception as e:
    print("Error parsing JSON:", e)
