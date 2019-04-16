import numpy as np

from Cards import *

class Line(object):
    """класс, описывающий выложенные линии"""
    def __init__(self):
        self.line = [] # вначале линия пуста

    def lenght(self):
        """Возвращает длину линии"""
        return len(self.line)

    def addCards(self, cards):
        self.line += cards

    def get_value(self):
        """Возвращает количество очков в строке из четырёх карт"""
        sum = 0
        if len(self.line) == 4:
            for i in range(4):
                sum += int(self.line[i][1])
            return sum


class Desk:
    """класс, описывающий положение карт на игральной доске"""
    def __init__(self):
        """
        пустое поле размера (66 + 66) * (66 + 66) * 3, где 131 - максимальная длина стороны поля,
        3 - кол-во параметров для каждой карты, рабочее поле = (1:131) * (1:131)
        """
        self.desk = np.zeros((132, 132, 3))
        # self.desk[i][j][0] = suit
        # self.desk[i][j][1] = value
        # self.desk[i][j][2] = form
        self.line = Line()

