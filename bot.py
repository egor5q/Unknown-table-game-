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
import lobbys
games=lobbys.games

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


client=MongoClient(os.environ['database'])
db=client.unknown
users=db.users

@bot.message_handler(commands=['creategame'])
def creategame(m):
    if m.chat.id not in games:
        if m.chat.id!=m.from_user.id:
            game=Game(m)
            games.update({game.id:game})
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='Присоединиться',callback_data='join'))
            msg=bot.send_message(m.chat.id,'Набор участников для экспедиции открыт! Жмите "Присоединиться" для вступления в игру.',reply_markup=kb)
            game=games[m.chat.id]
            game.message=msg
         
         
@bot.callback_query_handler(func=lambda call:True)
def inline(call): 
    if call.data=='join':
    try:
        game=games[call.message.chat.id]
    except:
        game=None
    if game!=None:
        if game.started==False:
            if call.from_user.id not in game.playerlist:
                game.createplayer(call.from_user)
                bot.send_message(call.message.chat.id,call.from_user.first_name+' присоединился!')
                game.m_update()
      
   

print('7777')
bot.polling(none_stop=True,timeout=600)

