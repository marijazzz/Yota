from random import shuffle
from Cards import *

class Pack(object):
    """класс, описывающий колоду карт"""
    def __init__(self):
        suit = '1234'   # 1 - Red, 2 - Blue, 3 - Green, 4 - Yellow
        form = '1234'  # 1 - Triangle, 2 - Cross, 3 - Round, 4 - Square
        value = '1234' # 1 - 1, 2 - 2, 3 - 3, 4 - 4
        self.cards = [Cards(s, v, f) for s in suit for v in value for f in form] # генератор списков создающий колоду из 64 карт
        self.cards += ['555', '555'] # добавление двух карт Джокера
        shuffle(self.cards) # перетасовка колоды карт

    def deal_card(self):
        """ Функция сдачи карты """
        return self.cards.pop()