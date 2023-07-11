import sys
import os
import datetime
import json
import requests
from api_key import coinlayer_api_key


COINLAYER_API_URL = "http://api.coinlayer.com/api/"
LIST_OF_CURRENCY_JSON_FILENAME = "data/list_of_currency.json"
LIVE_EXCHANGE_RATE_JSON_FILENAME = "data/list_of_exchange_rate.json"
SYMBOLS = "BTC,ETH,USDT,BNB,XRP,USDC,STETH"


def load_data(filename):
    if not os.path.exists(filename):
        print(f"Ошибка. Файл '{filename}' не найден")
        return
    with open(filename, 'r', encoding="utf-8") as f:
        return json.load(f)


def catch_error(response) -> bool:
    if not response:
        print("Ошибка выполнения запроса")
        print(response.url)
        print(f"HTTP статус: {response.status_code}, ({response.reason})")
        sys.exit(1)
    elif not response.json()["success"]:
        print("Отказано в доступе")
        print("Причина >>>")
        print(f"{response.json()['error']['type']}: "
              f"{response.json()['error']['info']}")
        return False
    return True


def create_response(endpoint, params, filename):
    url = COINLAYER_API_URL + endpoint
    response = requests.get(url, params=params)
    if not catch_error(response):
        return
    with open(filename, "w", encoding="utf-8") as f:
        result = response.json()
        result['date'] = str(datetime.date.today())
        json.dump(result, f)


def get_list_of_currency():
    params = {
        "access_key": coinlayer_api_key,
    }
    create_response("list", params, LIST_OF_CURRENCY_JSON_FILENAME)


def get_live_exchange_rate():
    params = {
        "access_key": coinlayer_api_key,
        "symbols": SYMBOLS,
    }
    create_response("live", params, LIVE_EXCHANGE_RATE_JSON_FILENAME)


def print_currency():
    currencies = load_data(LIST_OF_CURRENCY_JSON_FILENAME)
    if currencies is None:
        return
    print("Валюта")
    for key, value in currencies['fiat'].items():
        print(f"{key}: {value}")
    print()
    print("Криптовалюта")
    for value in currencies['crypto'].values():
        print(f"{value['symbol']}: {value['name']}")
    print()


def print_exchange_rate():
    rate = load_data(LIVE_EXCHANGE_RATE_JSON_FILENAME)
    if rate is None:
        return
    print(f"Стоимость криптовалюты в {rate['target']}")
    for name, cost in rate['rates'].items():
        print(f"1 {name} = {cost} {rate['target']}")


def check_and_reload_data():
    # Нет смысла обновлять файл со всеми валютами каждый день
    # currency = load_data(LIST_OF_CURRENCY_JSON_FILENAME)
    # if currency['date'] != str(datetime.date.today()):
    #     get_list_of_currency()
    rate = load_data(LIVE_EXCHANGE_RATE_JSON_FILENAME)  # Обновление курса каждый день
    if rate['date'] != str(datetime.date.today()):
        get_live_exchange_rate()


def main():
    get_list_of_currency()
    get_live_exchange_rate()


if __name__ == "__main__":
    main()
