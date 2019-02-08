# -*- coding: utf-8 -*-
import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import game_classes
import games

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.unknown
users=db.users

@bot.message_handler(commands=['creategame'])
def creategame(m):
   game=Game(m)


print('7777')
bot.polling(none_stop=True,timeout=600)

