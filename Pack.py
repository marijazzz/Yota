from random import shuffle
from .Cards import *


class Pack(object):
    """класс, описывающий колоду карт"""

    def __init__(self, card_list=None):
        if not card_list:  # колода создается с нуля, т.е. доступны все карты
            color = '1234'  # 1 - Red, 2 - Blue, 3 - Green, 4 - Yellow
            form = '1234'  # 1 - Triangle, 2 - Cross, 3 - Round, 4 - Square
            value = '1234'  # 1 - 1, 2 - 2, 3 - 3, 4 - 4
            self.cards = [Cards(s, v, f) for s in color for v in value for f in
                          form]  # генератор списков создающий колоду из 64 карт
            self.cards += ['555', '555']  # добавление двух карт Джокера
            shuffle(self.cards)  # перетасовка колоды карт
        else:  # если есть ограничение на доступные карты, т.е. часть карт разыграна
            self.cards = card_list
            shuffle(self.cards)


    def shuffle(self):
        """ Функция перемешивания карт"""
        shuffle(self.cards)

    def addCard(self, card):
        """ Функция добавления карт в колоду"""
        self.cards.append(card)

    def deal_card(self):
        """ Функция сдачи карты """
        return self.cards.pop()
