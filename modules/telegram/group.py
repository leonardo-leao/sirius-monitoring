# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import os
import telebot

#from actions.file import File

class TelegramGroupMessage():

    key = os.getenv("telegramToken")
    bot = telebot.TeleBot(key, parse_mode="Markdown")

    @staticmethod
    def sendMessage(message: str) -> None:

        """ Send a message to Sirius Monitoring Group """

        group = -721650661
        TelegramGroupMessage.bot.send_message(group, message)

    @staticmethod
    def sendPhoto(photo):

        """ Send a photo to Sirius Monitoring Group """

        group = -721650661
        TelegramGroupMessage.bot.send_photo(group, photo)

    @staticmethod
    def sendAlert(pv: str, infos: dict) -> None:

        message = f"""**{pv}**\nTemperatura: {round(infos["value"], 2)}°C \nDiferença da média: {round(infos["value"]-infos["trainedValue"], 2)}°C"""
        photo = infos["plot"]

        #File.insertLog("Alert sent")
        TelegramGroupMessage.sendMessage(message)
        TelegramGroupMessage.sendPhoto(photo)

if __name__ == "__main__":
    TelegramGroupMessage()