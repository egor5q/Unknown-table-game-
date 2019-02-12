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
import cards
from tools import medit
games=lobbys.games

from game_classes import codetoclass, findallenemy, findnearenemy

token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)


#client=MongoClient(os.environ['database'])
#db=client.unknown
#users=db.users

@bot.message_handler(commands=['creategame'])
def creategame(m):
    if m.chat.id not in games:
        if m.chat.id!=m.from_user.id:
            game=game_classes.Game(m)
            games.update({game.id:game})
            kb=types.InlineKeyboardMarkup()
            kb.add(types.InlineKeyboardButton(text='Присоединиться',callback_data='join'))
            msg=bot.send_message(m.chat.id,'Набор участников для экспедиции открыт! Жмите "Присоединиться" для вступления в игру.',reply_markup=kb)
            game=games[m.chat.id]
            game.message=msg
            t=threading.Timer(30,game.cancelgame)
            t.start()
            game.canceltimer=t
        else:
            bot.send_message(m.chat.id, 'В эту игру нельзя играть в личке! Добавьте бота в какой-нибудь чат.')
            
            
@bot.message_handler(commands=['startgame'])
def startgame(m):
    try:
        game=games[m.chat.id]
    except:
        game=None
    if game!=None:
        game.canceltimer=None
        game.startgame()

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
        else:
            bot.send_message(call.message.chat.id, call.from_user.first_name+', в этом чате нет запущенной игры! Сначала начните её '+
                             'командой /creategame.')
    else:
        kb=types.InlineKeyboardMarkup()
        game=games[int(call.data.split(' ')[1])]
        for ids in game.playerlist:
            if game.playerlist[ids].id==call.from_user.id:
                user=game.playerlist[ids]
        chat=game
        if 'playcard' in call.data:
            for ids in user.cards:
                print(ids)
                print(ids.name)
                kb.add(types.InlineKeyboardButton(text=ids.name, callback_data='info '+str(chat.id)+' '+ids.code))
            medit('Выберите карту:', call.message.chat.id, call.message.message_id, reply_markup=kb)
            
        if 'info' in call.data:
            x=call.data.split(' ')[2]
            text='none'
            card=codetoclass(x)
            text=card.info
            if card.type!='unknown' and card.type!='infection':
                kb.add(types.InlineKeyboardButton(text='⚡️Использовать карту', callback_data='usecard '+str(chat.id)+' '+x))
            kb.add(types.InlineKeyboardButton(text='↩️Назад', callback_data='mainmenu '+str(chat.id)))
            medit(text, call.message.chat.id, call.message.message_id)
            
        if 'usecard' in call.data:
            card=codetoclass(call.data.split(' ')[2])
            if card.type=='action' or card.type=='barrier':
                if user.active:
                    if card.targetable and user.target==None:
                        if card.target_all:
                            enemies=findallenemy(user, game)
                        else:
                            enemies=findnearenemy(user, game)
                        if card.target_self:
                            enemies.append(user)
                        for ids in enemies:
                            kb.add(types.InlineKeyboardButton(text=ids.name, callback_data='usecard '+str(chat.id)+' '+card.code+' '+str(ids.id)))
                        kb.add(types.InlineKeyboardButton(text='Назад', callback_data='mainmenu'))
                        medit('Выберите цель для карты "'+card.name+'":', call.message.chat.id, call.message.message_id)
                    else:
                        enm=call.data.split(' ')[3]
                        enemy=None
                        for ids in chat.playerlist:
                            if ids.id==int(enm):
                                enemy=enm
                        t=threading.Timer(10, card.use, args=[user, enemy, chat])
                        t.start()
                        enemy.defmenu(card)
                else:
                    bot.answer_callback_query(call.id, 'Сейчас не ваш ход!')
                    
            elif card.type=='defence':
                if user.active==False and user.attacked:
                    pass
                else:
                    bot.answer_callback_query(call.id, 'Эту карту можно сыграть только в ответ на сыгранную на вас карту!')       
        
      
   

print('7777')
bot.polling(none_stop=True,timeout=600)

