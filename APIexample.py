#chatgpt minimal working example
import requests

API_KEY = "your_token_here"
url = "https://admetmesh.scbdd.com/api/predict/"

payload = {
    "smiles": "CC(C)OC(=O)CC(=O)CSc1nc2c(cc1C#N)CCC2",
    "token": API_KEY
}

response = requests.post(url, json=payload)
print(response.status_code)
print(response.json())          
    