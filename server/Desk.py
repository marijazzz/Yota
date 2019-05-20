from collections import defaultdict
from typing import List

from Exception import *
from Cards import Card


class Desk:

    MAX_DIMENSION = 103

    def __init__(self):
        """
        Словарь, с пустыми значениями в виде None; максимальным считаем размер поля 103 * 103
        """
        def return_none():
            """
            Приведение к нужному формату
            :return:
            """
            return None

        self.desk = defaultdict(return_none)
        self.positions_of_cards_added_this_turn = []

    def add_card_first_time(self, card):
        """
        Добавление первой карты в центр поля
        :param card:
        :return:
        """
        self.desk[(51, 51)] = card  # добавление карты

    @staticmethod
    def is_line_validation(line: List[Card]):
        """
        Проверка корректности постановки данной карты по отношению к другим картам в линии
        :param line:
        :return:
        """

        if len(line) > 4:  # проверка длины линии
            raise LineException('Линия очень длинная')

        # проверка соответствия свойств данной карты остальным картам в линии
        for property_idx in range(Card.PROPERTY_NUM):
            line_property_values = [card.properties[property_idx] for card in line]

            if not (len(set(line_property_values)) == 1
                    or len(line_property_values) == len(set(line_property_values))):
                raise LineException("""Все карты в линии должны иметь либо одинковое значение,
                                       либо у всех карт разное значвение по каждому из 3-х свойств!""")

    @staticmethod
    def get_lines_that_has_position(desk: defaultdict, position: tuple):
        """
        Поиск линий, расположенных рядом с заданной позицией
        :param desk:
        :param position:
        :return:
        """
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # смещение по координатам на 1 вправо, влево, вверх, вниз
        result_horizontal_line = [desk[position]]  # горизонтальное направление потенциального выкладывания карт
        result_vertical_line = [desk[position]]  # вертикальное направление потенциального выкладывания карт

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

    def add_card(self, card, position: tuple):
        """
        Добавление карт на поле
        :param card:
        :param position:
        :return:
        """
        # карта должна выкладываться на пустое место
        if self.desk[position] is not None:
            raise AddCardException('Сюда поставить карту нельзя, там уже есть карты')

        desk_copy = self.desk.copy()
        desk_copy[position] = card
        lines = self.get_lines_that_has_position(desk_copy, position)
        cards_this_turn = [self.desk[position] for position in self.positions_of_cards_added_this_turn]

        # Все карты, выложенные в этот ход, должны составлять одну линию
        lines_that_contains_all_cards_this_turn = [
            line for line in lines if set(cards_this_turn).issubset(set(line))
        ]
        if len(lines_that_contains_all_cards_this_turn) != 1:
            AddCardException(f'Все карты, выложенные в этот ход, должны составлять одну линию')

        # Карты должна примыкать к любой из карт на столе
        if all(len(line) == 1 for line in lines):
            AddCardException(f'Карта должна примыкать к одной из выложенных карт')
        # list of list of card
        for line in lines:
            # Все линии на столе должны подчинятся правилам линий:
            # не больше 4-х карт
            # все карты в линии должны иметь либо одинковое значение,
            # либо у всех карт разное значение по каждому из 3-х свойств
            try:
                self.is_line_validation(line)
            except LineException as e:
                raise AddCardException(f'Сюда поставить карту нельзя. Ошибка линии: {str(e)}')

        self.desk[position] = card
        self.positions_of_cards_added_this_turn.append(position)

    def reset_score(self):
        self.positions_of_cards_added_this_turn = []

    @staticmethod
    def remove_duplicate_in_lines(lines):
        """
        При пересечение линий исключается подсчёт очков для одной общей карты дважды
        :param lines:
        :return:
        """
        result = []
        for line in lines:
            need_to_add = True
            for line_in_result in result:
                if set(line) == set(line_in_result):
                    need_to_add = False
            if need_to_add:
                result.append(line)

        return result

    def count_score_this_turn(self):
        """
        Подсчёт очков за один ход
        :return:
        """
        lines_that_changes_this_turn = []
        score = 0
        for position in self.positions_of_cards_added_this_turn:
            lines = self.get_lines_that_has_position(self.desk, position)
            lines_that_changes_this_turn += lines

        # нужно удалить все дубликаты
        lines_that_changes_this_turn = self.remove_duplicate_in_lines(lines_that_changes_this_turn)

        for line in lines_that_changes_this_turn:  # подсчёт очков в каждой изменённой за 1 ход линии
            if len(line) > 1:
                for card in line:
                    score += int(card.value)  # считается кол-во очков от значения каждой карты

        lines_with_4_cards = [line for line in lines_that_changes_this_turn if len(line) == 4]

        score *= (2 ** len(lines_with_4_cards))

        if self.positions_of_cards_added_this_turn == 4:  # удваивание очков, если вся линия полна
            score *= 2

        return score
