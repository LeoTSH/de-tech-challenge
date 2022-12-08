import requests
import pandas as pd
import json

url = "https://api.covid19api.com/country/singapore/status/confirmed"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
data = json.loads(response.text)

with open("../data/singapore_data.json", "w") as f:
    json.dump(data,
        f, 
        ensure_ascii=False, 
        indent=4
        )
