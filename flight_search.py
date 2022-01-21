from datetime import datetime
import requests
import os


API_KEY = os.getenv("API_KEY")
from_city = "SAO"

month = int(datetime.now().strftime("%m"))
months_ahead = (month + 6) % 12     # "(month + {o número de meses a frente a procurar por passagens})"
date_from = datetime.now().strftime("%d/%m/%Y")
date_to = datetime.now().strftime(f"%d/{months_ahead:02d}/%Y")
date_to = date_to

header = {
    "apikey": API_KEY,
}


class FlightSearch:
    def data(self, dest_iata, price_to, dest_name, stop_over=0, one_for_city=1):
        """Retorna os dados contendo as informações da passagem"""

        dest_iata = dest_iata
        price_to = price_to
        dest_name = dest_name
        stop_over = stop_over
        parameters_flight_search = {
            "fly_from": from_city,
            "fly_to": dest_iata,
            "date_from": date_from,
            "date_to": date_to,
            "price_to": price_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "curr": "BRL",
            "locale": "br",
            "one_for_city": one_for_city,
            "max_stopovers": stop_over,
            "limit": 1,
        }

        response = requests.get(
            url="https://tequila-api.kiwi.com/v2/search",
            params=parameters_flight_search,
            headers=header
        )
        response.raise_for_status()
        data = response.json()
        try:
            data["data"][0]
        except IndexError:
            if stop_over == 1:
                print(f"Não há passagens para {dest_name} nessa faixa de preço.")
            return None
        else:
            return data

    def get_iata(self, city: str, lowest_price: int):
        """Retorna o mesmo que DataManager().cities_lowest_prices, porém, com o nome da cidade convertido
        em seu respectivo código IATA, necessário para a busca de passagens"""

        parameters_get_id = {
            "term": city,
            "location_types": "city",
        }

        response = requests.get(
            "https://tequila-api.kiwi.com/locations/query",
            params=parameters_get_id,
            headers=header
        )
        response.raise_for_status()
        data = response.json()
        code_iata = [data["locations"][0]["code"], lowest_price]
        return code_iata
