import requests
import os
import json

API_KEY = os.environ.get("CITO_API_KEY")
if not API_KEY:
    print("CITO_API_KEY not set")
    exit(1)

URL = "https://api.citoapi.com/v1/cod/cdl/schedule"
headers = {"x-api-key": API_KEY}

response = requests.get(URL, headers=headers, timeout=15)
response.raise_for_status()
data = response.json()

matches = data.get("data", [])

print(f"Total matches returned: {len(matches)}\n")

# Print first match completely
if matches:
    print("First match raw JSON:")
    print(json.dumps(matches[0], indent=2))
else:
    print("No matches returned by API")
