from Exception import AddCardException

from Cards import RegularCard, Joker, Card
from Player import *

from collections import defaultdict
from typing import List

class LineException(Exception):
    pass

class Desk:
    MAX_DIMENTION = 103
    def __init__(self):
        """
        """

        def returnNone():
            return None
        self.desk = defaultdict(returnNone)
        self.positions_of_cards_added_this_turn = []

    def add_card_first_time(self, card: Card):
        """Добавление первой карты в центр поля"""
        self.desk[(51,51)] = card # добавление карты

    def isLineValidation(self, line: List[Card]):

        if len(line) > 4:
            raise LineException('Линия очень длинная')

        for property_idx in range(Card.PROPERTY_NUM):
            line_property_values = [card.properties[property_idx] for card in line]

            if not (len(set(line_property_values)) == 1
                    or len(line_property_values) == len(set(line_property_values))):
                raise LineException('Все карты в линии должны иметь либо одинковое значение, либо у всех карт разное значвение по каждому из 3-х свойств!')

    def getLinesThatHasPosition(self, desk: defaultdict, position: tuple):
        result = []  # массив с непустыми линиями вокруг указанной позиции на поле
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # смещение по координатам на 1 вправо, влево, вверх, вниз
        result_horizontal_line = [desk[position]]
        result_vertical_line = [desk[position]]

        for offset in offsets:
            cards_in_direction = []
            current_position = (position[0] + offset[0], position[1] + offset[1])
            current_card = desk[current_position]
            while current_card is not None:
                cards_in_direction.append(current_card)
                current_position = (current_position[0] + offset[0], current_position[1] + offset[1])
                current_card = desk[current_position]

            if offset[0] == 0:
                result_vertical_line += cards_in_direction
            else:
                result_horizontal_line += cards_in_direction

        return [result_vertical_line, result_horizontal_line]


    def add_card(self, card: Card, position: tuple):
        # карта должна выкладываться на пустое место
        if self.desk[position] is not None:
            raise AddCardException('Сюда поставить карту нельзя, там уже есть карты')

        desk_copy = self.desk.copy()
        desk_copy[position] = card
        lines = self.getLinesThatHasPosition(desk_copy, position)
        cards_this_turn = [self.desk[position] for position in self.positions_of_cards_added_this_turn]


        # Все карты, выложенные в этот ход, должны составлять одну линию
        lines_that_contains_all_cards_this_turn = [
            line for line in lines if set(cards_this_turn).issubset(set(line))
        ]
        if len(lines_that_contains_all_cards_this_turn) != 1:
            AddCardException(f'Все карты, выложенные в этот ход, должны составлять одну линию')

        # карты должна примыкать к любой из карт на столе
        if all(len(line) == 1 for line in lines):
            AddCardException(f'Карта должна примыкать к одной из выложенных карт')
        # list of list of card
        for line in lines:
            # Все линии на столе должны починятся правилам линий:
            ## не больше 4-х карт
            ## все карты в линии должны иметь либо одинковое значение, либо у всех карт разное значвение по каждому из 3-х свойств
            try:
                self.isLineValidation(line)
            except LineException as e:
                raise AddCardException(f'Сюда поставить карту нельзя. Ошибка линии: {str(e)}')

        self.desk[position] = card
        self.positions_of_cards_added_this_turn.append(position)

    def resetScore(self):
        self.positions_of_cards_added_this_turn = []

    def removeDuplicatesInLines(self, lines):
        result = []
        for line in lines:
            need_to_add = True
            for line_in_result in result:
                if set(line) == set(line_in_result):
                    need_to_add = False
            if need_to_add:
                result.append(line)

        return result

    def countScoreThisTurn(self):
        lines_that_changes_this_turn = []
        score = 0
        for position in self.positions_of_cards_added_this_turn:
            lines = self.getLinesThatHasPosition(self.desk, position)
            lines_that_changes_this_turn += lines

        # нужно удалить все дубликаты
        lines_that_changes_this_turn = self.removeDuplicatesInLines(lines_that_changes_this_turn)

        for line in lines_that_changes_this_turn:
            if len(line) > 1:
                for card in line:
                    score += int(card.value)

        lines_with_4_cards = [line for line in lines_that_changes_this_turn if len(line) == 4]

        score *= (2 ** len(lines_with_4_cards))

        if self.positions_of_cards_added_this_turn == 4:
            score *= 2

        return score