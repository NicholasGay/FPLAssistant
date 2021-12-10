import sys
from typing import List

import telebot
import logging
import player_sel
import config

#import os
#os.environ['no_proxy'] = '*'
# telegram_key = os.environ.get('TELEGRAM_API_KEY')

# NOTE EDIT THIS TO ENSURE SECURITY

bot = telebot.TeleBot(config.TELEGRAM_KEY)

logger = telebot.logger
formatter = logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                              '%m-%d %H:%M:%S')
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)
logger.setLevel(logging.INFO)  # or use logging.INFO
ch.setFormatter(formatter)

########################################################################################################################
COMMANDS: List[str] = list()

########################################################################################################################
COMMANDS.append('Hi')


@bot.message_handler(commands=[COMMANDS[0]])
def greet(message):
    bot.send_message(message.chat.id, "Hey! LIM PEH FPL Assistant")


########################################################################################################################
COMMANDS.append('GKP_ADVICE')


@bot.message_handler(commands=[COMMANDS[1]])
def greet(message):
    bot.send_message(message.chat.id, "OK wait, Lim Peh help you do math...")
    strToSend = player_sel.GKP().select_gkp()
    bot.send_message(message.chat.id, strToSend)


########################################################################################################################
COMMANDS.append('DEF_ADVICE')


@bot.message_handler(commands=[COMMANDS[2]])
def greet(message):
    bot.send_message(message.chat.id, "OK wait, Lim Peh help you do math...")
    strToSend = player_sel.DEF().select_DEF()
    bot.send_message(message.chat.id, strToSend)


########################################################################################################################
COMMANDS.append('MID_ADVICE')


@bot.message_handler(commands=[COMMANDS[3]])
def greet(message):
    bot.send_message(message.chat.id, "OK wait, Lim Peh help you do math...")
    strToSend = player_sel.MID().select_MID()
    bot.send_message(message.chat.id, strToSend)


########################################################################################################################
COMMANDS.append('FWD_ADVICE')


@bot.message_handler(commands=[COMMANDS[4]])
def greet(message):
    bot.send_message(message.chat.id, "OK wait, Lim Peh help you do math...")
    strToSend = player_sel.FWD().select_FWD()
    bot.send_message(message.chat.id, strToSend)


########################################################################################################################
COMMANDS.append('DEF_TOP3')


@bot.message_handler(commands=[COMMANDS[5]])
def greet(message):
    bot.send_message(message.chat.id, "OK wait, Lim Peh help you do math...")
    # strToSend = player_sel.DEF().select_DEF_top3("")
    bot.send_message(message.chat.id, "Whats the max price?")
    bot.register_next_step_handler(message, process_input)


def process_input(message):
    strToSend = player_sel.DEF().select_DEF_top3(message.text)
    bot.send_message(message.chat.id, strToSend)


########################################################################################################################
COMMANDS.append('MID_TOP3')


@bot.message_handler(commands=[COMMANDS[6]])
def greet(message):
    bot.send_message(message.chat.id, "OK wait, Lim Peh help you do math...")
    # strToSend = player_sel.DEF().select_DEF_top3("")
    bot.send_message(message.chat.id, "Whats the max price?")
    bot.register_next_step_handler(message, process_def)


def process_def(message):
    strToSend = player_sel.MID().select_Mid_top3(message.text)
    bot.send_message(message.chat.id, strToSend)


########################################################################################################################
# This line must be last
COMMANDS.append('help')


@bot.message_handler(commands=[COMMANDS[-1]])
def hello(message):
    temp = COMMANDS[0:len(COMMANDS) - 1]
    for i in range(len(COMMANDS) - 1):
        temp[i] = "/" + COMMANDS[i]
    toSend = '\n'.join(map(str, temp))
    bot.send_message(message.chat.id, "Avaliable commands are:\n" + toSend)


########################################################################################################################
# CATCH ALL MESSAGES
@bot.message_handler(func=lambda message: True)
def command_default(message):
    str_toSend = "YOU NO SPEAKY ENGLISH? List of commands available with /" + COMMANDS[-1]
    bot.send_message(message.chat.id, str_toSend)
    # request = message.text.split()


bot.infinity_polling(timeout=10, long_polling_timeout=5)
