from chalice import Chalice, Rate
import requests
import os
from chalicelib.scrape_effeuno import scrape_effeuno


app = Chalice(app_name="telegram-forno-f1")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
    requests.post(url, data=data)


def send_message(scraped_data):
    send_telegram_message("PRICE UPDATE!")
    send_telegram_message(
        "https://www.effeuno.biz/it/negozio/linea-easy-pizza/easy-pizza-pro/p134ha-509-pro/"
    )
    send_telegram_message(str(scraped_data))


@app.schedule(Rate(12, unit=Rate.HOURS))
def index(event):
    # print("Scheduled event triggered")
    # print(event.to_dict())
    scraped_data = scrape_effeuno()

    # Convert price string to integer for comparison (remove commas if any)
    price_str = scraped_data["price"].split(",") if scraped_data["price"] else ["0"]
    price_value = int(price_str[0]) if price_str[0].isdigit() else 0
    price_changed = price_value < 899
    promotion_changed = (
        scraped_data["promotion"]
        != "SPEDIZIONE GRATUITA SOLO PER AGOSTO. Accessori inclusi: PIETRA EFFEUNO"
    )

    if promotion_changed:
        scraped_data["message"] = "Promotion has changed!"
    if price_changed:
        scraped_data["message"] = "Price has changed!"

    if price_changed or promotion_changed:
        send_message(scraped_data)
    return True
