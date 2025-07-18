import os
import requests
import telegram
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

PRODUCTS = {
    "Aoarashi": "https://matchamiyako.com/en-us/products/aoarashi-100-g-matcha-bag",
    "Isuzu": "https://matchamiyako.com/en-us/products/isuzu-100-gr-matcha",
    "Matcha Latte": "https://matchamiyako.com/en-us/products/matcha-latte"
}

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def check():
    for name, url in PRODUCTS.items():
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            btn = soup.find('button', attrs={'name':'add'})
            if btn and not btn.has_attr('disabled'):
                bot.send_message(chat_id=CHAT_ID,
                                 text=f"✅ *{name}* je dostupný!\n{url}",
                                 parse_mode='Markdown')
                print(f"✅ Sent alert for {name}")
            else:
                print(f"❌ {name} stále vypredaný")
        except Exception as e:
            print(f"⚠️ Chyba pri {name}: {e}")

if __name__ == "__main__":
    check()
