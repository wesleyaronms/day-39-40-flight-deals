import os
import requests


TOKEN = os.getenv("BITLY_TOKEN")
BITLY_ENDPOINT = os.getenv("BITLY_ENDPOINT")

header = {
    "Authorization": TOKEN,
    "Content-Type": "application/json",
}


class FlightData:

    def __init__(self, data):
        """Recebe os dados de FlightSearch()"""

        self.data = data
        self.routes = len(data["data"][0]["route"])     # data["data"] contém uma lista onde se encontram as passagens

    def get_details(self):
        """Retorna uma lista de mensagens contendo as informações de passagem disponível"""

        price = str(self.data["data"][0]["conversion"]["BRL"])
        if len(price) > 3:
            price = price[:-3] + "," + price[-3:]
        city_from = self.data["data"][0]["route"][0]["cityFrom"]
        airport_from = self.data["data"][0]["route"][0]["flyFrom"]
        date_departure = self.data["data"][0]["route"][0]["local_departure"].split("T")[0]
        url_link = self.data["data"][0]["deep_link"]
        # print(url_link)
        short_url = self.short_url(url_link)

        if self.routes < 4:
            city_to = self.data["data"][0]["route"][0]["cityTo"]
            airport_to = self.data["data"][0]["route"][0]["flyTo"]
            date_return = self.data["data"][0]["route"][1]["local_departure"].split("T")[0]
            message = f"Alerta de preço! Apenas R${price} de {city_from}-{airport_from} " \
                      f"para {city_to}-{airport_to}, ida {date_departure}, volta {date_return}.\n" \
                      f"{short_url}"
            return message

        else:
            via_city = self.data["data"][0]["route"][0]["cityTo"]
            via_iata = self.data["data"][0]["route"][0]["flyTo"]
            city_to = self.data["data"][0]["route"][1]["cityTo"]
            airport_to = self.data["data"][0]["route"][1]["flyTo"]
            date_return = self.data["data"][0]["route"][3]["local_departure"].split("T")[0]
            message = f"Alerta de preço! Apenas R${price} de {city_from}-{airport_from} " \
                      f"para {city_to}-{airport_to}, ida {date_departure}, volta {date_return}.\n" \
                      f"Viagem possui uma conexão. Parada em {via_city}-{via_iata}.\n" \
                      f"{short_url}"
            return message

    def short_url(self, deep_link):
        parameters = {
            "domain": "bit.ly",
            "long_url": deep_link,
        }

        response = requests.post(url=BITLY_ENDPOINT, json=parameters, headers=header)
        response.raise_for_status()
        data = response.json()
        return data["link"]
