import requests
import json

from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):
        if base not in keys:
            raise APIException(f'Отсутствуют данные о валюте: {base}')
        if quote not in keys:
            raise APIException(f'Отсутствуют данные о валюте: {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Третьим аргументом должно быть число')
        if amount <= 0:
            raise APIException('Количество конвертируемой валюты должно быть положительным числом')
        if base == quote:
            raise APIException('Нельзя конвертировать одинаковые валюты')
        params = {
            'fsym': keys[quote],
            'tsyms': keys[base]
        }
        r = requests.get('https://min-api.cryptocompare.com/data/price', params=params)
        price = json.loads(r.text)[keys[base]]
        return float(price) * amount
