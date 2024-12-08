import requests

def convert(changeThisCurrency,toThisCurrency,amount):
    url = "https://api.currencybeacon.com/v1/convert"
    params = {"from": changeThisCurrency,"to": toThisCurrency,"amount": amount}
    api_key = "p9WCI0sOzsOma0mHAN3S0EGyH2LByTJY"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["response"]["value"]
    else:
        print("Error:", response.status_code, response.text)
        
print(convert("USD", "LBP", 500))