from http.client import responses

import requests
import json


url = "https://mindicador.cl/api"

response = requests.get(url)
data = json.loads(response.text.encode("utf-8"))
pretty_json = json.dumps(data, indent=2)
print(pretty_json)