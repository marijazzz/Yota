class Cards(object):
    """класс, описывающий характеристики обычных карт"""

    def __init__(self, color, value, form):
        self.color = color
        self.value = value
        self.form = form
        self.properties = [self.color, self.value, self.form]

    def __repr__(self):
        # return "<Cards {0} {1} {2}>".format(self.color, self.value, self.form)
        return self.color + self.value + self.form

    def color(self):
        return self.color

    def value(self):
        return self.value

    def form(self):
        return self.form


class Joker(object):
    """класс, описывающий карту Джокера"""

    def __init__(self, color_, value_, form_):
        self.color_ = 5
        self.value_ = 5
        self.form_ = 5


        # '''
        # color identification (id)
        # 1: Red
        # 2: Blue
        # 3: Green
        # 4: Yellow
        # '''
        #
        # class color:
        #     """Класс, описывающий цвета карт"""
        #     def __init__(self, id):
        #         self.id = id
        #
        #     def __eq__(self, other):
        #         """Переопределение равенства"""
        #         return self.id == other.id
        #
        #     def __ne__(self, other):
        #         """Переопределение неравенства"""
        #         return not (self.id == other.id)
        #
        #
        # '''
        # Value identification
        # 1: 1
        # 2: 2
        # 3: 3
        # 4: 4
        # '''
        #
        # class Value:
        #     """Класс, описывающий численное значение карт"""
        #     def __init__(self, value):
        #         self.value = value
        #
        #     def __eq__(self, other):
        #         """Переопределение равенства"""
        #         return self.value == other.value
        #
        #     def __ne__(self, other):
        #         """Переопределение неравенства"""
        #         return not (self.value == other.value)
        #
        #
        # '''
        # Form identification (iden)
        # 1: Triangle
        # 2: Cross
        # 3: Round
        # 4: Square
        # '''
        #
        # class Form:
        #     """Класс, описывающий форму карт"""
        #     def __init__(self, iden):
        #         self.iden = iden
        #
        #     def __eq__(self, other):
        #         """Переопределение равенства"""
        #         return self.iden == other.iden
        #
        #     def __ne__(self, other):
        #         """Переопределение неравенства"""
        #         return not (self.iden == other.iden)
