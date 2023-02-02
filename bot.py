# Author: Leonardo Rossi Leão
# E-mail: leonardo.leao@cnpem.br

import os
import telebot
from actions.file import File

# Connecting Sirius Monitoring Bot
key = os.getenv("telegramToken")
bot = telebot.TeleBot(key)
alter_alarm_time = False

# Bot actions
@bot.message_handler(commands=["opcao1"])
def opcao1(mensagem):
    settings = File.loadSettings()
    if settings["status"] == 1:
        texto = "Monitoramento já está ativo"
    else:
        settings["status"] = 1
        File.alterSettings(settings)
        texto = "Monitoramento foi iniciado"
        File.insertLog("Monitoring on")
    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["opcao2"])
def opcao2(mensagem):
    settings = File.loadSettings()
    if settings["status"] == 0:
        texto = "Monitoramento já está desligado"
    else:
        settings["status"] = 0
        File.alterSettings(settings)
        texto = "Monitoramento foi desligado"
        File.insertLog("Monitoring off")
    bot.send_message(mensagem.chat.id, texto)

@bot.message_handler(commands=["opcao3"])
def opcao3(mensagem):
    global alter_alarm_time
    alter_alarm_time = True
    bot.send_message(mensagem.chat.id, "Digite o tempo em minutos")

def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(mensagem):
    
    global alter_alarm_time
    if not alter_alarm_time:
        texto = """
        Escolha uma opção para continuar (Clique no item):
        /opcao1 Ativar monitoramento
        /opcao2 Desativar monitoramento
        /opcao3 Alterar janela de alarmes
        """
        bot.reply_to(mensagem, texto)
    else:
        alter_alarm_time = False
        settings = File.loadSettings()
        time = mensagem.json["text"]
        try:
            settings["alarm_time"] = int(time)
            File.alterSettings(settings)
            texto = f"Intervalo de alarme alterado para {time} min"
            File.insertLog(f"Alarm time was changed to {time} min")
        except:
            texto = f"Valor inválido"
        bot.send_message(mensagem.chat.id, texto)


bot.polling()