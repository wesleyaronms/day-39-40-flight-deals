from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager
from user import User


user_input = User()
email_list = user_input.get_emails()
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

cities_prices = data_manager.cities_lowest_prices
iata_prices = []

for city_price in cities_prices:
    iata_prices.append(flight_search.get_iata(city_price[0], city_price[1]))

for city_price in iata_prices:
    data = flight_search.data(city_price[0],
                              city_price[1],
                              cities_prices[iata_prices.index(city_price)][0])
    if data is not None:
        flight_data = FlightData(data)
        message = flight_data.get_details()
        notification_manager.send_email(message, email_list)
    else:
        data = flight_search.data(city_price[0],
                                  city_price[1],
                                  cities_prices[iata_prices.index(city_price)][0],
                                  stop_over=2,
                                  one_for_city=0)
        if data is not None:
            flight_data = FlightData(data)
            message = flight_data.get_details()
            notification_manager.send_email(message, email_list)
