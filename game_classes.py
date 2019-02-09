# -*- coding: utf-8 -*-
import lobbys
import tools
games=lobbys.games

deck=['1','2','3','4','5','6','7','8']

class Game:
    
    def __init__(self,m):
        self.id=m.chat.id
        self.playerlist={},
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
        
    def createplayer(self,user):
        self.playerlist.update({user.id:Player(user)})
        
    def startgame(self):
        self.started=True
        preparegame(self)
        
    def preparegame(self):
        #Тут будет раздача карт игрокам и перемешивание колоды
        place=1
        for ids in self.playerlist:
            self.playerlist[ids]['place']=place
            i=0
            while i<self.handcards:
                x=random.choice(self.deck)
                self.playerlist[ids]['cards'].append(x)
                self.deck.remove(x)
                i+=1
            place+=1
        players=[]
        for ids in self.playerlist:
            players.append(self.playerlist[ids])
        self.currentplayer=random.choice(players)
        self.currentplayer.active=True
        
        self.currentplayer.turn()
        
        
    
    def m_update(self):   # Обновление списка игроков
        text='Список игроков:\n\n'
        for ids in self.playerlist:
            text+=ids['name']+'\n'
        tools.medit(text, self.message.chat.id, self.message.message_id)
        
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
        self.place=None
        self.active=False,
        self.nears=[]
        self.tradecard=None
        
    def turn(self):
        kb=types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text='Разыграть карту',callback_data='playcard'),types.InlineKeyboardButton(text='Окончить ход',callback_data='endturn'))
        bot.send_message(self.id, 'Ваша очередь сделать ход.',reply_markup=kb)
                         





