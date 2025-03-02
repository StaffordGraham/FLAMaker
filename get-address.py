import requests
response = requests.get("https://api.postcodes.io/postcodes/SW1A2AA")
if response.status_code==200:
    data =response.json()
    address=data['result']
    print (address)


