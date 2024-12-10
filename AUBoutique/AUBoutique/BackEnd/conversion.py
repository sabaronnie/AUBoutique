import requests
def convert(changeThisCurrency, toThisCurrency, amount):
    url = "https://api.currencybeacon.com/v1/convert"
    api_key = "FQGRmSWPGjOk8k8iHU8EENwuO2qN0ihO"
    params = {
        "from": changeThisCurrency,
        "to": toThisCurrency,
        "amount": amount,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["response"]["value"]
    else:
        print("Error:", response.status_code, response.text)
