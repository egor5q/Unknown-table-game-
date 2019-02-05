# -*- coding: utf-8 -*-
class Game:
    
    def __init__(self,m):
        self.id=m.chat.id
        self.playerlist={},
        self.started=False
        
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
        
            
         
        





