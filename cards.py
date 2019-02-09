import random

class Card:
    
    def __init__(self,typee):
        self.type=typee    # infection/action/defence/barrier/panica/unknown
        self.dropable=True
        self.name=None

    def use(self, player, target=None, game=None):
        return False
    
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
    
    def use(self, player, target=None, game=None):
        target.alive=False
        return True
        
class Analysis(Card):
    
    def __init__(self):
        self.name='Анализ'
    
    def use(self, player, target=None, game=None):
        text=''
        for ids in target.cards:
            text+=ids.name+'\n'
        bot.send_message(player.id, 'Карты в руке игрока '+target.name+':\n\n'+text)
        player.cards.remove(self)
        return True
        
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
        return True
            
            
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
        return True
        
class Viski(Card):
    
    def __init__(self):
        self.name='Виски'
        
    def use(self, player, game):
        text=''
        player.cards.remove(self)
        for ids in player.cards:
            text+=ids.name+'\n'
        bot.send_message(game.id, player.name+' выпил виски, и выложил всю правду о себе. Вот его карты'+':\n\n'+text)
        return True
        
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
        return True
        
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
        return True
                         
class Newplace_near(Card):
    
    def __init__(self):
        self.name='Меняемся местами!'
        
    def use(self, player, game):
        nearplayers=findnear(player, game)
        player.nears=nearplayers
        player.cards.remove(self)
        return True
        
class Newplace_far(Card):
    
    def __init__(self):
        self.name='Сматывай удочки!'
        
    def use(self, player, game):
        nearplayers=allplayers(player,game)
        player.nears=nearplayers
        player.cards.remove(self)
        return True
        
        
        
class Soblazn(Card):
    
    def __init__(self):
        self.name='Соблазн'
        
    def use(self, player):
        player.cards.remove(self)
        return True
        
        
class Scare(Card):
    
    def __init__(self):
        self.name='Страх'
        
    def use(self, player, target):
        bot.send_message(player.id, 'Карта, от которой вы отказались: "'+target.tradecard.name+'".')
        player.cards.remove(self)
        return True
        
class Stayhere(Card):
    
    def __init__(self):
        self.name='Мне и здесь неплохо'
        
    def use(self, player, game, target):
        bot.send_message(game.id, player.name+' отказался от обмена местами с '+target.name+' с помощью карты "Мне и здесь неплохо"!')
        return True
    
class Nothx(Card):
    
    def __init__(self):
        self.name='Нет уж, спасибо!'
        
    def use(self, player, game, target):
        bot.send_message(game.id, player.name+' отказался от обмена картами с '+target.name+' с помощью карты "Нет уж, спасибо!"!')
        return True
    
class Miss(Card):
    
    def __init__(self):
        self.name='Мимо!'
        
    def use(self, player, game):
        return True
    
class Nofire(Card):
    
    def __init__(self):
        self.name='Никакого шашлыка!'
        
    def use(self, player, target, game):
        bot.send_message(game.id, player.name+' надел противогаз! Игроку '+target.name+' не удалось сжечь его.')
        return True

class Carantine(Card):
    pass
        
                         
                         
        
            
            
        
        
    
        
        
        
        
    
        
        
