import requests

def fetch_exchange_rates():
    try:
        exchange_url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
        response = requests.get(exchange_url)
        data = response.json()

        if response.status_code == 200:
            exchange_rates = "Курс валют до гривні:\n"
            for currency in data:
                exchange_rates += f"{currency['ccy']} -> {currency['base_ccy']}: {currency['buy']} - {currency['sale']}\n"
            return exchange_rates
        else:
            return "Не вдалося отримати курс валют."
    except Exception as e:
        return "Виникла помилка. Спробуйте ще раз пізніше."
