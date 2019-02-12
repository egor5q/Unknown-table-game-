import random
import os
import telebot
token = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(token)

class Card:
    
    def __init__(self):
        self.type=None    # infection/action/defence/barrier/panica/unknown
        self.dropable=True
        self.name='Name=None'
        self.code='none'
        self.info='Информация отсутствует.'
        self.targetable=False
        self.targetall=False
        self.target_self=False
        self.cancancelled=[]     # Чем можно отменить эффект этой карты

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
    
    def __init__(self):
        super().__init__()
        self.type='unknown'
        self.dropable=False
        self.name='Нечто'
        self.code='unknown'
        self.info='*Нечто*\n\nВы - нечто! Ваша цель - сделать так, чтобы все живые игроки стали зараженными.'
    
        
class Infection(Card):
    
    def __init__(self):
        super().__init__()
        self.type='infection'
        self.name='Заражение'
        self.code='infection'
        self.info='*Заражение*\n\n Если вы получили её от другого игрока - этот игрок Нечто (потому что только Нечто может '+\
        'отдавать карты заражения другим игрокам), а вы теперь зараженный! Если же вы взяли ее из колоды - все в порядке, но будет '+\
        'нехорошо, если другой игрок застанет вас с этой картой на руках...'
            
        
        
    
class Flame(Card):
    def __init__(self):
        super().__init__()
        self.name='Огнемёт'
        self.type='action'
        self.code='flame'
        self.targetable=True
        self.cancancelled=['nofire']
        self.info='*Огнемёт*\n\nС помощью этой штуки вы можете сжечь любого соседнего игрока - и если у него нет карты "Никакого шашлыка!", '+\
        'то он выбывает из игры.'
    
    def use(self, player, target, game):
        nears=findnear(player, game)
        if target in nears and target.defence==False:
            target.alive=False
            bot.send_message(game.id, player.name+' сжигает '+target.name+' заживо!')
            player.cards.remove(self)
            return True
        return False
        
class Analysis(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Анализ'
        self.type='action'
        self.code='analysis'
        self.targetable=True
        self.cancancelled=False
        self.info='*Анализ*\n\nЭта карта позволит вам посмотреть ВСЕ карты на руке соседнего игрока.'
    
    def use(self, player, target, game):
        nears=findnear(player, game)
        if target in nears:
            text=''
            for ids in target.cards:
                text+=ids.name+'\n'
            bot.send_message(player.id, 'Карты в руке игрока '+target.name+':\n\n'+text)
            bot.send_message(game.id, player.name+' использует карту "'+self.name+'" на '+target.name+'!')
            player.cards.remove(self)
            return True
        return False
        
class Axe(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Топор'
        self.type='action'
        self.code='axe'
        self.targetable=True
        self.target_self=True
        self.cancancelled=False
        self.info='*Топор*\n\nОТКРЫВАЙ, ЭТО ДЖОННИ! Сломайте любую соседнюю дверь или снимите карантин с себя или соседнего игрока.'
        
    def use(self, player, target, game):
        x=str(self.place)+'-'+str(target.place)
        y=str(target.place)+'-'+str(self.place)
        if target==None:
            player.effects.remove('carantine')
            text=player.name+' снимает с себя карантин!'
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
        super().__init__()
        self.name='Подозрение'
        self.type='action'
        self.code='untruth'
        self.targetable=True
        self.cancancelled=False
        self.info='*Недоверие*\n\nПосмотрите случайную карту на руке соседнего игрока.'
        
    def use(self, player, target, game=None):
        cards=[]
        for ids in target.cards:
            cards.append(ids)
        x=random.choice(cards)
        bot.send_message(player.id,'Вы смотрите случайную карту игрока '+target.name+'. Ей оказалась карта "'+x.name+'"!')
        bot.send_message(game.id, player.name+' использует карту "'+self.name+'" на '+target.name+'!')
        player.cards.remove(self)
        return True
        
class Viski(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Виски'
        self.type='action'
        self.code='viski'
        self.info='*Виски*\n\nОт всего этого голова кругом идёт... Время выпить! Использовав, вы показываете все свои карты '+\
        'на руке всем игрокам.'
        
    def use(self, player, target, game):
        text=''
        player.cards.remove(self)
        for ids in player.cards:
            text+=ids.name+'\n'
        bot.send_message(game.id, player.name+' выпил виски, и выложил всю правду о себе. Вот его карты'+':\n\n'+text)
        return True
        
class Persistence(Card):   # Упорство
     
    def __init__(self):
        super().__init__()
        self.name='Упорство'
        self.type='action'
        self.code='persistence'
        self.info='*Упорство*\n\nИспользовав, вы смотрите 3 верхние карты колоды, берете одну на руку и сбрасываете остальные.'
        
    def use(self, player, target, game):
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
        player.cards.remove(self)
        return True
        
class Around(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Гляди по сторонам'
        self.type='action'
        self.code='around'
        self.info='*Гляди по сторонам*\n\nИспользовав, вы меняете направление хода на противоположное.'
        
    def use(self, player, target, game):
        if game.onclock:
            game.onclock=False
        else:
            game.onclock=True
        bot.send_message(game.id, 'Игрок '+player.name+' изменил направление хода!')
        player.cards.remove(self)
        return True
                         
class Newplace_near(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Меняемся местами!'
        self.type='action'
        self.code='newplace_near'
        self.targetable=True
        self.cancancelled=['stayhere']
        self.info='*Меняемся местами!*\n\nУ меня нехорошее предчувствие, надо сваливать отсюда! Использовав, вы меняетесь местами с '+\
        'соседним игроком.'
        
    def use(self, player, target, game):
        nearplayers=findnear(player, game)
        player.nears=nearplayers
        player.cards.remove(self)
        return True
        
class Newplace_far(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Сматывай удочки!'
        self.type='action'
        self.code='newplace_far'
        self.cancancelled=['stayhere']
        self.targetable=True
        
    def use(self, player, target, game):
        nearplayers=allplayers(player,game)
        player.cards.remove(self)
        return True
        
        
        
class Soblazn(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Соблазн'
        self.type='action'
        self.code='soblazn'
        self.cancancelled=['scare', 'nothx', 'miss']
        self.targetable=True
        
    def use(self, player, target, game):
        player.cards.remove(self)
        return True
        
        
class Scare(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Страх'
        self.type='defence'
        self.code='scare'
        
    def use(self, player, target, game):
        bot.send_message(player.id, 'Карта, от которой вы отказались: "'+target.tradecard.name+'".')
        player.cards.remove(self)
        return True
        
class Stayhere(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Мне и здесь неплохо'
        self.type='defence'
        self.code='stayhere'
        
    def use(self, player, target, game):
        bot.send_message(game.id, player.name+' отказался от обмена местами с '+target.name+' с помощью карты "Мне и здесь неплохо"!')
        player.cards.remove(self)
        return True
    
class Nothx(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Нет уж, спасибо!'
        self.type='defence'
        self.code='nothx'
        
    def use(self, player, target, game):
        bot.send_message(game.id, player.name+' отказался от обмена картами с '+target.name+' с помощью карты "Нет уж, спасибо!"!')
        player.cards.remove(self)
        return True
    
class Miss(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Мимо!'
        self.type='defence'
        self.code='miss'
        
    def use(self, player, target, game):
        player.cards.remove(self)
        return True
    
class Nofire(Card):
    
    def __init__(self):
        super().__init__()
        self.name='Никакого шашлыка!'
        self.type='defence'
        self.code='nofire'
        
    def use(self, player, target, game):
        bot.send_message(game.id, player.name+' надел противогаз! Игроку '+target.name+' не удалось сжечь его.')
        player.cards.remove(self)
        return True

class Carantine(Card):
    pass
        
                         
                         
        
            
            
        
        
    
        
        
        
        
    
        
        
