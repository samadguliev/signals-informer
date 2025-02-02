from logger import logger
from models import Signal, Currency
from scheduler.celery import app
import requests

@app.task
def update_prices():
    logger.info("Task started")
    signals = Signal.get_all()
    if len(signals) == 0:
        return

    existing_currencies = Currency.get_existing_currencies()
    curr_codes = set(signal.currency_code for signal in signals)

    currencies_to_update = []
    currencies_to_create = []

    response = requests.get("https://api.mexc.com/api/v3/ticker/price")
    if response.status_code != 200:
        logger.error("Failed to get price data")
        return

    for curr in response.json():
        symbol = curr["symbol"][:-4]
        usdt = curr["symbol"][-4:]

        if usdt != "USDT":
            continue

        if symbol in curr_codes:
            if symbol in existing_currencies:
                # Update existing currency
                existing_currency = existing_currencies[symbol]
                existing_currency.price = curr["price"]
                currencies_to_update.append(existing_currency)
            else:
                # Create new currency
                currencies_to_create.append(Currency(code=symbol, price=curr["price"]))

        # Update existing currencies
    if currencies_to_update:
        Currency.update_currencies(currencies_to_update)

        # Create new currencies
    if currencies_to_create:
        Currency.create_currencies(currencies_to_create)

