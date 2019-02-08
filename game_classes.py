# -*- coding: utf-8 -*-
import lobbys
import tools

class Game:
    
    def __init__(self,m):
        self.id=m.chat.id
        self.playerlist={},
        self.started=False
        self.message=None
        
    def createplayer(self,user):
        self.playerlist.update({user.id:{
            'name':user.first_name,
            'id':user.id,
            'role':'good',    #good, evil or unknown (нечто)
            'effects':[],     #все эффекты типо карантина, заколоченной двери итд
            'cards':[],       #все карты в руке игрока
            'alive':True
        }
                               })
        
    def startgame(self):
        self.started=True
        preparegame(self)
        
    def preparegame(self):
        #Тут будет раздача карт игрокам и перемешивание колоды
        pass
    
    def m_update(self):   # Обновление списка игроков
        text='Список игроков:\n\n'
        for ids in self.playerlist:
            text+=ids['name']+'\n'
        tools.medit(text, self.message.chat.id, self.message.message_id)
        
            
         
        





