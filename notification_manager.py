import smtplib
import os


email = os.getenv("email")
password = os.getenv("password")


class NotificationManager:
    def send_email(self, message, email_list):
        """Envia as mensagens para todos os emails no Google Sheets"""
        for users_email in email_list:
            try:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=email, password=password)
                    connection.sendmail(
                        from_addr=email,
                        to_addrs=users_email,
                        msg=f"Subject:Alerta de preço de viagem\n\n{message}".encode()
                        )
            except:
                pass
