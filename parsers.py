import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from items import Item


class RestCountriesParser:

    def __init__(self):
        self.session = requests.session()

    def scrape_country_info(self, country: str) -> None:
        url = f"https://restcountries.com/v3.1/name/{country}"

        try:
            response = self.session.get(url)
            response.raise_for_status()

            data = response.json()[0]
            table = [
                ["Name", self._get_country_name(data)],
                ["Capital", self._get_country_capital(data)],
                ["Flag", self._get_country_flag(data)]
            ]

            print(tabulate(table, headers="firstrow", tablefmt="grid"))

        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")

    @staticmethod
    def _get_country_name(data: dict) -> str:
        return data.get("name", {}).get("official", "N/A")

    @staticmethod
    def _get_country_capital(data: dict) -> str:
        return data.get("capital", ["N/A"])[0]

    @staticmethod
    def _get_country_flag(data: dict) -> str:
        return data.get("flags", {}).get("png", "N/A")


class EbayParser:

    def __init__(self):
        self.session = requests.session()

    def scrape_item_info(self, url: str):
        response = self.session.get(url).content

        soup = BeautifulSoup(response, "html.parser")

        return Item(
            url=url,
            name=self._get_item_name(soup),
            image=self._get_item_image(soup),
            price=self._get_item_price(soup),
            seller=self._get_item_seller(soup),
        )

    @staticmethod
    def _get_item_name(soup: BeautifulSoup) -> str:
        element = soup.find("h1", class_="x-item-title__mainTitle")

        return element.find("span", class_="ux-textspans ux-textspans--BOLD").text

    @staticmethod
    def _get_item_image(soup: BeautifulSoup) -> str:
        div_element = soup.find_all("div", class_="ux-image-carousel-item")[0]
        img_element = div_element.find("img")

        return img_element["src"]

    @staticmethod
    def _get_item_price(soup: BeautifulSoup) -> float:
        element = soup.find("div", class_="x-price-primary")
        price = element.find("span", class_="ux-textspans").text
        return float(price.replace("US $", "").replace(",", ""))

    @staticmethod
    def _get_item_seller(soup: BeautifulSoup) -> str:
        element = soup.find("div", class_="x-sellercard-atf__info__about-seller")
        return element.get("title")
