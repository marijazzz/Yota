from random import shuffle


class Cards(object):
    """класс, описывающий характеристики обычных карт"""
    def __init__(self, suit, value, form):
        self.suit = suit
        self.value = value
        self.form = form

    def __repr__(self):
        # return "<Cards {0} {1} {2}>".format(self.suit, self.value, self.form)
        return self.suit + self.value + self.form


class Joker(object):
    """класс, описывающий карту Джокера"""
    def __init__(self, suit_, value_, form_):
        self.suit_ = 15
        self.value_ = 15
        self.form_ = 15


class Pack(object):
    """класс, описывающий колоду карт"""
    def __init__(self):
        suit = '1248'   # 1 - Red, 2 - Blue, 4 - Green, 8 - Yellow
        form = '1248'  # 1 - Triangle, 2 - Cross, 4 - Disk, 8 - Square
        value = '1248' # 1 - 1, 2 - 2, 4 - 3, 8 - 4
        self.cards = [Cards(s, v, f) for s in suit for v in value for f in form] # генератор списков создающий колоду из 64 карт
        self.cards += ['151515', '151515'] # добавление двух карт Джокера
        shuffle(self.cards) # перетасовка колоды карт

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

    def get_amount(self):
        """Возвращает количество карт"""
        return len(self.cards)


class Line(object):
    """класс, описывающий выложенные линии"""
    def __init__(self):
        self.cards = [] # вначале линия пуста

    def lenght(self):
        """Возвращает длину линии"""
        return len(self.cards)

    '''def get_value(self):
        """Возвращает количество очков в строке из четырёх карт"""
        sum = bin(0)
        if len(self.cards) == 4:
            for i in range(4):
                sum += bin(self.cards[i][2])'''


class Player:
    """Класс, описывающий количество очков у игрока, количество и достоинство его карт"""
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.score = 0

    def add_card(self, card):
        self.hand.add_card(card)