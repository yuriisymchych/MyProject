import requests

def fetch_crypto_rates():
    try:
        crypto_currencies = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'ripple']
        crypto_message = "Курс криптовалют на даний час:\n"

        for crypto in crypto_currencies:
            crypto_url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
            response = requests.get(crypto_url)
            data = response.json()

            if response.status_code == 200:
                price = data[crypto]['usd']
                crypto_message += f"{crypto.capitalize()}: ${price}\n"
            else:
                crypto_message += f"{crypto.capitalize()}: Немає даних\n"

        return crypto_message
    except Exception as e:
        return "Виникла помилка. Спробуйте ще раз пізніше."
