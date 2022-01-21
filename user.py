import requests
import os


USER_SHEET_ENDPOINT = os.getenv("USER_SHEET_ENDPOINT")
TOKEN = os.getenv("TOKEN")

header = {
    "Authorization": TOKEN,
}


class User:

    def __init__(self):
        print("Bem vindo ao Flight Club.\nTe enviaremos por email as melhores ofertas de passagens.")
        user_name = input("Qual o seu nome?\n")
        user_lastname = input("Qual o seu sobrenome?\n")

        on = True
        while on:
            user_email = input("Qual o seu email?\n")
            check_user_email = input("Por favor, confirme o seu email.\n")
            if user_email == check_user_email:
                parameters = {
                    "user": {
                        "firstName": user_name,
                        "lastName": user_lastname,
                        "email": user_email,
                    }
                }
                response = requests.post(
                    url=USER_SHEET_ENDPOINT,
                    json=parameters,
                    headers=header)
                response.raise_for_status()
                print("Bem-vindo ao clube!")
                on = False
            else:
                print("Desculpe, você digitou dois emails diferentes.\nTente novamente.")
        return

    def get_emails(self):
        response = requests.get(url=USER_SHEET_ENDPOINT, headers=header)
        response.raise_for_status()
        data = response.json()
        email_list = [_["email"] for _ in data["users"]]
        return email_list
