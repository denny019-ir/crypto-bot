import time
import requests
from datetime import datetime, timedelta

TOKEN = "8107637434:AAFxBgTXQkNnlMphjW5KkkYoFkgTGMFtzCs"
CHAT_ID = "7897842354"
COINS = ["bitcoin", "ethereum", "solana", "ripple", "pepe", "bonk"]
VS_CURRENCY = "usd"
API_URL = f"https://api.coingecko.com/api/v3/simple/price"

def get_prices():
    ids = ",".join(COINS)
    params = {
        "ids": ids,
        "vs_currencies": VS_CURRENCY
    }
    try:
        res = requests.get(API_URL, params=params)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def format_message(prices):
    now = datetime.utcnow() + timedelta(hours=9)  # GMT+9
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    message = f"📊 Update Harga Crypto ({timestamp} GMT+9):\n\n"
    if "error" in prices:
        message += f"❌ Gagal ambil data: {prices['error']}"
        return message
    for coin in COINS:
        price = prices.get(coin, {}).get(VS_CURRENCY)
        if price:
            symbol = {
                "bitcoin": "₿",
                "ethereum": "Ξ",
                "solana": "◎",
                "ripple": "XRP",
                "pepe": "🐸",
                "bonk": "🐶"
            }.get(coin, coin.upper())
            message += f"{symbol} {coin.capitalize()}: ${price:,.4f}\n"
        else:
            message += f"{coin.capitalize()}: ❌ Data tidak tersedia\n"
    return message

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Gagal kirim pesan:", e)

if __name__ == "__main__":
    while True:
        data = get_prices()
        message = format_message(data)
        send_telegram_message(message)
        time.sleep(60 * 60 * 2)  # tunggu 2 jam
