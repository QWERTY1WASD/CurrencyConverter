import sys
import json
import requests
from api_keys import coinlayer_api_key


COINLAYER_API_URL = "http://api.coinlayer.com/api/"


def catch_error(response) -> bool:
    if not response:
        print("Ошибка выполнения запроса")
        print(response.url)
        print(f"HTTP статус: {response.status_code}, ({response.reason})")
        sys.exit(1)
        return False
    elif not response.json()["success"]:
        print("Отказано в доступе")
        print("Причина >>>")
        print(f"{response.json()['error']['type']}: "
              f"{response.json()['error']['info']}")
        return False
    return True


def get_list_of_currency():
    url = COINLAYER_API_URL + "list"
    params = {
        "access_key": coinlayer_api_key
    }
    response = requests.get(url, params=params)
    if not catch_error(response):
        return
    return response.json()


def main():
    result = get_list_of_currency()
    currencies = result["fiat"]
    crypto_currencies = result["crypto"]
    print("Валюта")
    for key, value in currencies.items():
        print(f"{key}: {value}")
    print()
    print("Криптовалюта")
    for value in crypto_currencies.values():
        print(f"{value['symbol']}: {value['name']}")
    print()



if __name__ == "__main__":
    main()
