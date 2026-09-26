import requests

url = "https://api.giga.chat/v1/models"

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': 'sk_df365f5dfdf0dc0f5c164a95ce2fc297a697d348d27c224d'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)