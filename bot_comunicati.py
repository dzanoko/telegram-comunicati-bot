import requests
from bs4 import BeautifulSoup
from telegram import Bot
import time
import os

# === CONFIGURAZIONE ===
TOKEN = "8016734003:AAGsNcVWUDZ9b7TYHR6oa_wFgHl3l2JIj0c"
CHAT_ID = "331906201"

URLS = {
    "Lega Pro": "https://www.lega-pro.com/category/comunicati/primavera-4/",
    "SGS": "https://www.figc.it/it/giovani/norme/comunicati",
    "LND": "https://www.crlombardia.it/comunicati?q=&page=&content_category_value_id=27&stagione=&data-il=2025-10-14&data-dal=2025-10-14&data-al=2025-10-14&delegazioni%5B%5D=12",
}

bot = Bot(token=TOKEN)

# === FUNZIONE PER SCARICARE IL PRIMO LINK/TITOLO DI OGNI PAGINA ===
def get_latest_title(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")

        if "lega-pro" in url:
            item = soup.find("h2")
        elif "figc" in url:
            item = soup.find("a", class_="card__link")
        elif "crlombardia" in url:
            item = soup.find("a", class_="elementor-post__read-more")
        else:
            item = None

        if item:
            return item.text.strip()
        return None
    except Exception as e:
        print(f"Errore su {url}: {e}")
        return None

# === MAIN LOOP ===
def main():
    seen = {}

    # se esiste un file di stato precedente, caricalo
    if os.path.exists("seen.txt"):
        with open("seen.txt", "r", encoding="utf-8") as f:
            for line in f:
                key, value = line.strip().split("||")
                seen[key] = value

    while True:
        for name, url in URLS.items():
            latest = get_latest_title(url)
            if not latest:
                continue

            if seen.get(name) != latest:
                seen[name] = latest
                msg = f"Nuovo comunicato {name}!"
                bot.send_message(chat_id=CHAT_ID, text=msg)
                print(msg)

        # salva stato
        with open("seen.txt", "w", encoding="utf-8") as f:
            for key, value in seen.items():
                f.write(f"{key}||{value}\n")

        time.sleep(900)  # 15 minuti


if __name__ == "__main__":
    main()
