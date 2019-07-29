import requests

input_for_create = {
  "agent_type": "ModularAgent"
}

url = "http://127.0.0.1:8000/"
response = requests.post(url + "create/", json=input_for_create)

print(response.status_code, response.reason)

