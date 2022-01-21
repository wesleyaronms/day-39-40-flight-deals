import requests
import os


MY_SHEET_ENDPOINT = os.getenv("MY_SHEET_ENDPOINT")
TOKEN = os.getenv("TOKEN")

header = {
    "Authorization": TOKEN,
}


class DataManager:

    def __init__(self):
        """Retorna, da planilha do Sheets", as cidades/destinos e os valores máximos de passagem estabelecidos"""

        response = requests.get(url=MY_SHEET_ENDPOINT, headers=header)
        response.raise_for_status()
        self.data = response.json()
        self.cities_lowest_prices = [[key["city"], key["lowestPrice"]] for key in self.data["prices"]]
