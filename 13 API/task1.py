import requests
from lxml import etree
from io import BytesIO
from datetime import date
import pandas as pd


CODES = ["BYR", "USD", "EUR", "KZT", "UAH", "AZN", "KGS", "UZS", "GEL"]
URL = "http://www.cbr.ru/scripts/XML_daily.asp"


def generate_months(start: date, end: date):
    current = start
    while current <= end:
        yield current
        if current.month == 12:
            current = date(current.year + 1, 1, 1)
        else:
            current = date(current.year, current.month + 1, 1)


def fetch_month_df(target_date: date) -> dict:
    date_str = target_date.strftime("%d/%m/%Y")

    response = requests.get(URL, params={"date_req": date_str})
    response.raise_for_status()

    root = etree.parse(BytesIO(response.content)).getroot()

    rates = {}
    for valute in root.xpath(".//Valute"):
        code = valute.findtext("CharCode")
        if code not in CODES:
            continue

        vunit = valute.findtext("VunitRate")
        if vunit is None:
            continue

        rates[code] = float(vunit.replace(",", "."))

    row = {"date": target_date.strftime("%Y-%m")}
    for code in CODES:
        row[code] = rates.get(code)

    return row


class CurrencyMiner:
    def __init__(self):
        self.data = []

    def collect(self):
        start = date(2003, 1, 1)
        end = date(2024, 11, 1)

        for month in generate_months(start, end):
            self.data.append(fetch_month_df(month))

    def to_csv(self, path: str):
        pd.DataFrame(self.data).to_csv(path, index=False)


def main():
    miner = CurrencyMiner()
    miner.collect()
    miner.to_csv("student_works/currency.csv")


if __name__ == "__main__":
    main()
