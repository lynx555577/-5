import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from rich import print


def get_cbr_rates(date=None):
    if date is None:
        date = datetime.now().strftime("%d/%m/%Y")

    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Ошибка запроса к серверу ЦБ РФ: {response.status_code}")

    root = ET.fromstring(response.content)

    rates = {"RUB": 1}
    for record in root.findall("Valute"):
        char_code = record.find("CharCode").text
        nominal = int(record.find("Nominal").text)
        value_str = record.find("Value").text.replace(",", ".")
        value = float(value_str)
        rate = value / nominal
        rates[char_code] = rate

    return rates


def main():
    # Используем текущую дату по умолчанию
    date = datetime.now().strftime("%d/%m/%Y")

    try:
        rates = get_cbr_rates(date)

        while True:
            amount = float(input("Введите сумму для конвертации: "))
            base_currency = input("Введите базовую валюту (например, RUB): ").upper()
            target_currency = input("В какую валюту хотите перевести? (например, USD): ").upper()

            if base_currency in rates and target_currency in rates:
                base_rate = rates[base_currency]
                target_rate = rates[target_currency]
                converted_amount = round((amount / base_rate) * target_rate, 2)
                print(f"{amount} {base_currency} ≈ {converted_amount} {target_currency}")
            else:
                print(f"Валюты {base_currency} или {target_currency} не найдены.")

            choice = input("Продолжить? [Y/n]: ").lower().strip()
            if choice not in ["y", "yes"]:
                break

    except ValueError as e:
        print("Неверный формат ввода.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()