from random import shuffle

SUIT_COLOR = [0x1F0A0, 0x1F0B0, 0x1F0C0, 0x1F0D0]

class Cards(object):
    """класс, описывающий характеристики обычных карт"""
    def __init__(self, suit, value, form):
        self.suit = suit
        self.value = value
        self.form = form

    def __repr__(self):
        # return "<Cards {0} {1} {2}>".format(self.suit, self.value, self.form)
        return chr(SUIT_COLOR[self.suit] + self.value + self.form)

class Joker(object):
    """класс, описывающий карту Джокера"""
    def __init__(self, suit_, value_, form_):
        pass    #нужно придумать, как задавать значение для Джокера

class Pack(object):
    """класс, описывающий колоду карт"""
    def __init__(self):
        suit = 'RBGY'   # Red, Blue, Green, Yellow
        form = 'TCDS'  # Triangle, Cross, Disk, Square
        value = '1234'
        self.cards = [Cards(s, v, f) for s in suit for v in value for f in form] # генератор списков создающий колоду из 64 карт (пока без Джокера =( )
        shuffle(self.cards) # Перетасовка колоды карт
    def deal_card(self):
        """ Функция сдачи карты """
        return self.cards.pop()

class Hand(object):
    """класс, описывающий состояние руки"""
    def __init__(self, name):
        self.name = name # имя игрока
        self.cards = [] # Изначально рука пустая

    def add_card(self, card):
        """ Добавляет карту игроку """
        self.cards.append(card)

