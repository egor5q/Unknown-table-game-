# -*- coding: utf-8 -*-
import random
import os
import telebot
from telebot import types
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)
import threading

import lobbys
from tools import medit
import cards
games=lobbys.games

allcards=['unknown', 'infection', 'flame', 'analysis', 'axe', 'untruth', 'viski', 'persistence', 'around', 'newplace_near',
         'newplace_far', 'soblazn', 'scare', 'stayhere', 'nothx', 'miss', 'nofire']


class Game:
    
    def __init__(self,m):
        deck=[]
        for ids in allcards:
            if ids=='unknown':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Unknown())
                    i+=1
            if ids=='infection':
                i=0
                c=8
                while i<c:
                    deck.append(cards.Infection())
                    i+=1
            if ids=='flame':
                i=0
                c=3
                while i<c:
                    deck.append(cards.Flame())
                    i+=1
            if ids=='analysis':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Analysis())
                    i+=1
            if ids=='axe':
                i=0
                c=0
                while i<c:
                    deck.append(cards.Axe())
                    i+=1
            if ids=='untruth':
                i=0
                c=2
                while i<c:
                    deck.append(cards.Untruth())
                    i+=1
            if ids=='viski':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Viski())
                    i+=1
            if ids=='persistence':
                i=0
                c=2
                while i<c:
                    deck.append(cards.Persistence())
                    i+=1
            if ids=='around':
                i=0
                c=0
                while i<c:
                    deck.append(cards.Around())
                    i+=1
            if ids=='newplace_near':
                i=0
                c=2
                while i<c:
                    deck.append(cards.Newplace_near())
                    i+=1
            if ids=='newplace_far':
                i=0
                c=2
                while i<c:
                    deck.append(cards.Newplace_far())
                    i+=1
            if ids=='soblazn':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Soblazn())
                    i+=1
            if ids=='scare':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Scare())
                    i+=1
            if ids=='stayhere':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Stayhere())
                    i+=1
            if ids=='nothx':
                i=0
                c=2
                while i<c:
                    deck.append(cards.Nothx())
                    i+=1
            if ids=='miss':
                i=0
                c=0
                while i<c:
                    deck.append(cards.Miss())
                    i+=1
            if ids=='nofire':
                i=0
                c=1
                while i<c:
                    deck.append(cards.Nofire())
                    i+=1
        print(deck)
            
        self.id=m.chat.id
        self.playerlist={}
        self.started=False
        self.message=None
        self.canceltimer=None
        self.gametimer=None
        self.deck=deck
        self.trash=[]
        self.handcards=4
        self.currentplayer=None
        self.doors=[]
        self.onclock=True  # Ход по часовой стрелке или против
        self.traders=[]    # 2 меняющихся игрока
    

    def createplayer(self,user):
        self.playerlist.update({user.id:Player(user)})
        
    def startgame(self):
        self.started=True
        self.preparegame()
 


    def preparegame(self):
        #Тут будет раздача карт игрокам и перемешивание колоды
        place=1
        for ids in self.playerlist:
            self.playerlist[ids].chatid=self.id
            self.playerlist[ids].number=place
            i=0
            while i<self.handcards:
                x=random.choice(self.deck)
                self.playerlist[ids].cards.append(x)
                self.deck.remove(x)
                i+=1
            place+=1
        players=[]
        for ids in self.playerlist:
            players.append(self.playerlist[ids])
        self.currentplayer=random.choice(players)
        self.currentplayer.active=True
        self.gametimer=threading.Timer(8, self.nextplayer)
        self.gametimer.start()
        
        self.currentplayer.turn(self.id)
  

    def nextplayer(self):
        try:
            if self.onclock==True:
                np=self.currentplayer.number+1
                if np>len(self.playerlist):
                    np=1
            else:
                np=self.currentplayer.number-1
                if np<1:
                    np=len(self.playerlist)
            for ids in self.playerlist:
                if self.playerlist[ids].number==np:
                    curplayer=self.playerlist[ids]
            if self.currentplayer.ready==False:
                medit('Время вышло!', self.currentplayer.message.chat.id, self.currentplayer.message.message_id)
            self.trade(self.currentplayer, curplayer)

        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
            bot.send_message(441399484, traceback.format_exc())
    
    def trade(self, player1, player2, curplayer):        # Обмен картами между двумя игроками
        kb=types.InlineKeyboardMarkup()
        kbb=types.InlineKeyboardMarkup()
        for ids in player1.cards:
            kb.add(types.InlineKeyboardButton(text=ids.name, callback_data='trade '+str(self.id)+' '+ids.code))
        for ids in player2.cards:
            kbb.add(types.InlineKeyboardButton(text=ids.name, callback_data='trade '+str(self.id)+' '+ids.code))
        bot.send_message(player1.id, 'Выберите карту для обмена с '+player2.name+':', reply_markup=kb)
        bot.send_message(player2.id, 'Выберите карту для обмена с '+player1.name+':', reply_markup=kbb)
        t=threading.Timer(15, self.nextturn, args=[curplayer])
        t.start()
        
    def nextturn(self, curplayer):
        for ids in self.traders:
            if ids.fortrade==None:
                tradable=[]
                for idss in ids.cards:
                    if idss.dropable:
                        tradable.append(idss)
                ids.fortrade=random.choice(tradable)
                medit('Время вышло! Была выбрана случайная карта для обмена: "'+ids.fortrade.name+'".', ids.trademessage.chat.id, ids.trademessage.message_id)
        self.traders[0].cards.remove(self.traders[0].fortrade)
        self.traders[1].cards.remove(self.traders[1].fortrade)
        self.traders[0].cards.append(self.traders[1].fortrade)
        self.traders[1].cards.append(self.traders[0].fortrade)
        bot.send_message(self.traders[0].id, 'Обменом получена карта: "'+self.traders[1].fortrade.name+'"!')
        bot.send_message(self.traders[1].id, 'Обменом получена карта: "'+self.traders[0].fortrade.name+'"!')
            
        curplayer.active=True
        self.currentplayer.active=False
        self.currentplayer=curplayer
        self.currentplayer.turn(self.id)
        self.dropvars()
        self.gametimer=threading.Timer(4, self.nextplayer)
        self.gametimer.start()


    def dropvars(self):
        self.traders=[] 
        for ids in self.playerlist:
            self.playerlist[ids].tradecard=None
            self.playerlist[ids].defence=False
            self.playerlist[ids].attacked=False
            self.playerlist[ids].target=None
            self.playerlist[ids].message=None
            self.playerlist[ids].fortrade=None
            
         
    def m_update(self):   # Обновление списка игроков
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Присоединиться',callback_data='join'))
        text='Набор участников для экспедиции открыт! Жмите "Присоединиться" для вступления в игру.\nСписок игроков:\n\n'
        for ids in self.playerlist:
            text+=self.playerlist[ids].name+'\n'
        medit(text, self.message.chat.id, self.message.message_id, reply_markup=kb)
        
    def cancelgame(self):
        if self.canceltimer!=None:
            bot.send_message(self.id,'Игра была отменена!')
            del games[self.id]
        

         
class Player:
    def __init__(self,user):
        self.id=id
        self.name=user.first_name
        self.id=user.id
        self.role='good'     #good, infected or unknown (нечто)
        self.effects=[]      #все эффекты типо карантина, заколоченной двери итд
        self.cards=[]        #все карты в руке игрока
        self.alive=True
        self.number=None
        self.active=False
        self.tradecard=None
        self.defence=False
        self.attacked=False
        self.target=None
        self.chatid=None
        self.message=None
        self.fortrade=None
        
    def turn(self, chat):
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Разыграть карту',callback_data='playcard '+str(chat)),types.InlineKeyboardButton(text='Окончить ход',callback_data='endturn'))
        self.message=bot.send_message(self.id, 'Ваша очередь сделать ход.',reply_markup=kb)
        
    def defmenu(self, card):
        kb=types.InlineKeyboardMarkup()
             # Тут юзеру будет предлагаться сыграть карту защиты в ответ на сыгранную на него карту действия
        i=0
        for ids in self.cards:
            if ids.code in card.cancancelled:
                kb.add(types.InlineKeyboardButton(text=ids.name, callback_data='defence '+str(self.chatid)+' '+ids.code))
                i+=1
        if i>0:
            text='На вас была разыграна карта "'+card.name+'"! Если хотите, выберите одну из нижеперечисленных карт для защиты. '+\
            'У вас есть 10 секунд.'
        else:
            text='На вас была разыграна карта "'+card.name+'", но у вас нет подходящих карт для защиты.'
        self.message=bot.send_message(self.id, text, reply_markup=kb)
                         
        
                

def findallenemy(player,game):
        nears=[]
        for ids in game.playerlist:
            if game.playerlist[ids].id!=player.id:
                nears.append(game.playerlist[ids])
        return nears
    
       
def findnearenemy(player,game):
        x=player.number
        near1=x+1
        if near1>len(game.playerlist):
            near1=1
        near2=x-1
        if near2<1:
            near2=len(game.playerlist)
        for ids in game.playerlist:
            if game.playerlist[ids].number==near1:
                near1=game.playerlist[ids]
        for ids in game.playerlist:
            if game.playerlist[ids].number==near2:
                near2=game.playerlist[ids]
        nears=[near1, near2]
        return nears 
        
            
def codetoclass(x):
    if x=='unknown':
        text=cards.Unknown
    if x=='infection':
        text=cards.Infection
    if x=='flame':
        text=cards.Flame
    if x=='analysis':
        text=cards.Analysis
    if x=='axe':
        text=cards.Axe
    if x=='untruth':
        text=cards.Untruth
    if x=='viski':
        text=cards.Viski
    if x=='persistence':
        text=cards.Persistence
    if x=='around':
        text=cards.Around
    if x=='newplace_near':
        text=cards.Newplace_near
    if x=='newplace_far':
        text=cards.Newplace_far
    if x=='soblazn':
        text=cards.Soblazn
    if x=='scare':
        text=cards.Scare
    if x=='stayhere':
        text=cards.Stayhere
    if x=='nothx':
        text=cards.Nothx
    if x=='miss':
        text=cards.Miss
    if x=='nofire':
        text=cards.Nofire
    return text



