import random

class Card:
    
    def __init__(self,typee):
        self.type=typee    # infection/action/defence/barrier/panica/unknown
        self.dropable=True
        self.name=None

    def use(self, player, target=None):
        pass
    
    def findnear(player,game):
        x=player.number
        near1=x+1
        if near1>len(game.players):
            near1=1
        near2=x-1
        if near2<1:
            near2=len(game.players)
        for ids in game.players:
            if ids.place==near1:
                near1=ids
        for ids in game.players:
            if ids.place==near2:
                near2=ids
        nears=[near1, near2]
        return nears
    
    def allplayers(player,game):
        nears=[]
        for ids in game.players:
            if ids.id!=player.id:
                nears.append(ids)
        return nears
    
class Unknown(Card):
    
    def __init__(self, player):
        player.role='unknown'
        self.dropable=False
        self.name='Нечто'
    
        
class Infection(Card):
    
    def __init__(self,player):
        self.name='Заражение'
        inf=0
        if player.role=='infected':
            for ids in player.cards:
                if ids.type=='infection':
                    inf=1
            if inf==0:
                self.dropable=False
        else:
            self.dropable=False
            
        
        
    
class Flame(Card):
    def __init__(self):
        self.name='Огнемёт'
    
    def use(self, player, target=None):
        target.alive=False
        
class Analysis(Card):
    
    def __init__(self):
        self.name='Анализ'
    
    def use(self, player, target=None):
        text=''
        for ids in target.cards:
            text+=ids.name+'\n'
        bot.send_message(player.id, 'Карты в руке игрока '+target.name+':\n\n'+text)
        player.cards.remove(self)
        
class Axe(Card):
    
    def __init__(self):
        self.name='Топор'
        
    def use(self, player, target=None, game=None):
        if target==None:
            player.effects.remove('carantine')
            text=player.name+' снимает с себя карантин!'
        x=str(self.place)+'-'+str(target.place)
        y=str(target.place)+'-'+str(self.place)
        elif x in game.doors:
            game.doors.remove(x)
            text=player.name+' топором ломает дверь между собой и '+target.name+' с криками "ОТКРЫВАЙ, ЭТО ДЖОННИ!"'
        elif y in game.doors:
            game.doors.remove(y)
            text=player.name+' топором ломает дверь между собой и '+target.name+' с криками "ОТКРЫВАЙ, ЭТО ДЖОННИ!"'
            
        elif 'carantine' in target.effects:
            target.effects.remove('carantine')
            text=player.name+' снимает карантин с '+target.name+'!'
        
        bot.send_message(game.id, text)
        player.cards.remove(self)
            
            
class Untruth(Card):
    
    def __init__(self):
        self.name='Подозрение'
        
    def use(self, player, target, game=None):
        cards=[]
        for ids in target.cards:
            cards.append(ids)
        x=random.choice(cards)
        bot.send_message(player.id,'Вы смотрите случайную карту игрока '+target.name+'. Ей оказалась карта "'+x.name+'"!')
        player.cards.remove(self)
        
class Viski(Card):
    
    def __init__(self):
        self.name='Виски'
        
    def use(self, player, game):
        text=''
        player.cards.remove(self)
        for ids in player.cards:
            text+=ids.name+'\n'
        bot.send_message(game.id, player.name+' выпил виски, и выложил всю правду о себе. Вот его карты'+':\n\n'+text)
        
class Persistence(Card):   # Упорство
     
    def __init__(self):
        self.name='Упорство'
        
    def use(self, player, game):
        cards=[]
        for ids in game.deck:
            if ids.type!='panica':
                cards.append(ids)
        show=[]
        i=0
        while i<3:
            x=random.choice(cards)
            show.append(x)
            cards.remove(x)
            i+=1
        player.showlist=show    
        
class Around(Card):
    
    def __init__(self):
        self.name='Гляди по сторонам'
        
    def use(self, player, game):
        if game.onclock:
            game.onclock=False
        else:
            game.onclock=True
        bot.send_message(game.id, 'Игрок '+player.name+' изменил направление хода!')
        player.cards.remove(self)
                         
class Newplace_near(Card):
    
    def __init__(self):
        self.name='Меняемся местами!'
        
    def use(self, player, game):
        nearplayers=findnear(player, game)
        player.nears=nearplayers
        player.cards.remove(self)
        
class Newplace_far(Card):
    
    def __init__(self):
        self.name='Сматывай удочки!'
        
    def use(self, player, game):
        nearplayers=allplayers(player,game)
        player.nears=nearplayers
        player.cards.remove(self)
        
        
        
class Soblazn(Card):
    
    def __init__(self):
        self.name='Соблазн'
        
    def use(self, player):
        player.cards.remove(self)
        
        
class Scare(Card):
    
    def __init__(self):
        self.name='Страх'
        
    def use(self, player, target):
        bot.send_message(player.id, 'Карта, от которой вы отказались: "'+target.tradecard.name+'".')
        player.cards.remove(self)
                         
                         
        
            
            
        
        
    
        
        
        
        
    
        
        
