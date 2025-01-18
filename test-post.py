import requests
import json

# Define the webhook URL
url = "https://log-analytics.ns.namespaxe.com/webhook"

# Define the payload
payload = {
    "message": "Hello, this is a test!",
    "status": "success",
    "timestamp": "2025-01-17T12:00:00Z"
}

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(url, data=json.dumps(payload), headers=headers)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.json())
