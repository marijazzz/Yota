import numpy as np

from Cards import *
from Player import *


class Line(object):
    """класс, описывающий выложенные линии"""

    def __init__(self, cards, coordinate, direction=0, properties=(0, 0, 0)):
        self.line = cards  # линия создается из списка карт
        self.pos = coordinate  # координаты самой левой или самой верхней карты линии
        self.direction = direction  # направление движения линии: 0 - нет направления, 1 - горизонтально, 2 - вертикально
        self.properties = list(properties)  # определяет различные или одинаковые свойства карт в линии (0 если свойство одинаково для всех карт, 1 если разное)

    def length(self):
        """Возвращает длину линии"""
        return len(self.line)

    def get_direction(self, position):
        """определяет направление движения линии при добавлении новой карты"""
        if self.pos[0] == position[0]:
            return 2
        return 1

    def add_cards(self, card, position):
        """Добавление карт в линию"""
        if self.length() == 4:
            print('Линия полна')  # если линия полна, то выводим сообщщение о невозможности положить в линию
            return

        if self.properties == [0, 0,
                               0]:  # проверяем, как соотносятся друг с другом свойства карт (одинаковые или разные)
            for i in range(3):
                if self.line[0].properties[i] == card.properties[i]:
                    self.properties[i] = 0
                else:
                    self.properties[i] = 1
        else:
            if not self.check_card(card):
                print('Поставить сюда карту нельзя(')
                return

        self.direction = self.get_direction(position)
        if (position[0] <= self.pos[0]) or (position[1] <= self.pos[1]):  # проверяем позицию, куда хотим положить карту
            self.line.insert(0, card)  # если позиция левее или выше, то обновляем координаты начала линии
            self.pos = position
        else:
            self.line.append(card)  # если правее или ниже, то позицию начала сохраняем

    def change(self, card, hand, position):  # position - индекс Джокера в линии
        """Замена карты в линии в случае Джокера"""
        if type(card) == Joker:
            print('Так нельзя!(')
            return
        hand.append(self.line.pop(position))  # убрали Джокера из линии и добавили его в руку
        self.line.insert(position, card)  # добавили карту в линию вместо Джокера

    def check_card(self, card):
        """Проверка того, можно ли положить в линию карту"""
        bools = 0  # счетчик правильности
        for i in range(3):
            if self.properties[i] == 0:  # i-е свойство разное
                # проверка варианта того, что свойства ВСЕХ карт в линии разные
                for c in self.line:
                    if c.properties[i] == card.properties[i]:
                        bools = 1
                        break
            elif self.properties[i] == 1:  # i-е свойство одинаковое
                # проверка варианта того, что свойства ВСЕХ карт в линии одинаковые
                for c in self.line:
                    if c.properties[i] != card.properties[i]:
                        bools = 1
                        break
            if bools == 1:  # для выхода из цикла
                return False
        if bools == 0:  # ну а когда мешала лишняя проверка?
            return True

    def corner_check(self, other, card):
        """Проверка углового схождения линий...
        карта (self)  позиция (card)
        что-нибудь    карта (other)
        """
        if self.check_card(card) and other.check_card(card):
            return True
        return False

    def line_check(self, other, card):
        """Проверка линейного схождения линий
        карта (self) позиция (card) карта (other)
        self всегда левее/выше other
        """
        if not self.corner_check(other, card): # проверяем, подходит ли карта одновременно к обеим линиям
            return False

        if (self.length() + other.length() + 1) > 4: # проверяем длину потенциальной линии
            return False

        if self.length() >= other.length():
            line = Line(self.line, self.pos, self.direction, self.properties)
            if self.length() == 2:  # случай, когда длина левой линии = 2
                position = (0, 0)
                if self.direction == 1: # случай горизонтальной линии
                    position = (self.pos[0] + 2, self.pos[1])
                elif self.direction == 2: # случай вертикальной линии
                    position = (self.pos[0], self.pos[1] + 2)

                line.add_cards(card, position)

                if not line.check_card(other.line[0]):
                    return False

            else:
                position = (0, 0)
                if self.direction == 1:  # случай горизонтальной линии
                    position = (self.pos[0] + 2, self.pos[1])
                elif self.direction == 2:  # случай вертикальной линии
                    position = (self.pos[0], self.pos[1] + 2)

                line.add_cards(card, position)

                if not line.check_card(other.line[0]):
                    return False
        else:
            line = Line(other.line, other.pos, other.direction, other.properties)
            position = (0, 0)
            if line.direction == 1:  # случай горизонтальной линии
                position = (line.pos[0] - 1, line.pos[1])
            elif line.direction == 2:  # случай вертикальной линии
                position = (line.pos[0], line.pos[1] - 1)

            line.add_cards(card, position)

            if not line.check_card(self.line[0]):
                return False

        return True


class Desk:
    """класс, описывающий положение карт на игральной доске"""

    def __init__(self):
        """
        пустое поле размера (66 + 66) * (66 + 66), где 131 - максимальная длина стороны поля,
        рабочее поле = (1:131) * (1:131)
        """
        self.desk = np.zeros((132, 132))
        self.lines = []  # список всех выложенных линий

    def find(self, position):
        """ищем прилежащии линии"""
        positions = [(self.lines[i].pos, self.lines[i].direction) for i in
                     range(len(self.lines))]  # создаем список всех позиций и напралений
        x, y = position[0], position[1]
        lines = []  # список доступных линий

        if self.desk[x - 1][y] != 0:  # ищем линию слева
            i = 1
            while self.desk[x - i][y] != 0:  # ищем первую карту линии
                i += 1
            i -= 1
            if i != 1:
                idx = positions.index(((x - i, y), 1))
                lines.append(idx)
            else:
                idx = positions.index(((x - i, y), 0))
                lines.append(idx)

        if self.desk[x][y - 1] != 0:  # ищем линию сверху
            i = 1
            while self.desk[x][y - i] != 0:  # ищем первую карту линии
                i += 1
            i -= 1
            if i != 1:
                idx = positions.index(((x, y - i), 2))
                lines.append(idx)
            else:
                idx = positions.index(((x, y - i), 0))
                lines.append(idx)

        if self.desk[x + 1][y] != 0:  # ищем линию справа
            idx = positions.index(((x + 1, y), 1)) or positions.index(((x + 1, y), 0))
            lines.append(idx)

        if self.desk[x + 1][y] != 0:  # ищем линию снизу
            idx = positions.index(((x + 1, y), 1)) or positions.index(((x + 1, y), 0))
            lines.append(idx)

        return lines

    def add_card(self, card, position):
        """Добавление карты на поле"""
        if not self.desk[position[0]][position[1]]:  # смотрим, есть ли в позиции карта
            possible_lines = self.find(position)  # ищем все линии вокруг позиции (хранятся индексы найденных линий линий)

            if not possible_lines:  # проверяем, имеется ли хотя бы одна линия вокруг
                print('Сюда нельзя ставить')
                return

            if len(possible_lines) == 1:
                if self.lines[possible_lines[0]].check_card(card):
                    self.lines[possible_lines[0]].add_cards(card, position)

            elif len(possible_lines) == 2:
                pass

            elif len(possible_lines) == 4:
                pass

            else:
                pass
