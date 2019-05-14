from random import shuffle
from Cards import *


class Pack(object):
    """Класс, описывающий колоду карт"""

    def __init__(self):
        color = '1234'  # 1 - Red, 2 - Blue, 3 - Green, 4 - Yellow
        form = '1234'  # 1 - Triangle, 2 - Cross, 3 - Round, 4 - Square
        value = '1234'  # 1 - 1, 2 - 2, 3 - 3, 4 - 4
        self.cards = [
            RegularCard(s, v, f)
            for s in color
            for v in value
            for f in form
        ]  # генератор списков создающий колоду из 64 карт
        # self.cards += [Joker(), Joker()]  # добавление двух карт Джокера
        self.shuffle()  # перетасовка колоды карт

    def shuffle(self):
        """
        Функция перемешивания карт
        :return:
        """

        shuffle(self.cards)

    def addCard(self, card: Card):
        """
        Добавление карт в колоду
        :param card:
        :return:
        """
        self.cards.append(card)

    def deal_card(self):
        """
        Функция сдачи карты
        :return:
        """
        return self.cards.pop()

    def lenght(self):
        """
        Возвращение количества карт в колоде
        :return:
        """
        return len(self.cards)