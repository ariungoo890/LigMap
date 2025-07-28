#Wash molecules example
import requests

baseUrl = 'https://admetlab3.scbdd.com/'

if __name__ == '__main__':
    api = '/api/washmol' #changed '/api/washmol' to '/api/admet/washmol'
    url = baseUrl + api
    payload = {
        'smiles': ["molecule", "CC(C)OC(=O)CC(=O)CSc1nc2c(cc1C#N)CCC2"],
    }
    response = requests.post(url, json=payload)
    print("status code:", response.status_code)
    if response.status_code == 200:
        result = response.json()
        data = result['data']
        print("Data:", data)
#200 => the request was successful
#anything else (like 400, 403, or 500) => there was an error 
    else:
        print("Request succeeded but no 'data' field in response. ")
        print("Response:")
else: 
    print("Request failed with status code:" , response.status_code)
    print("Error message:", response.text)
        
