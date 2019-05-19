class Card():
    """класс, описывающий характеристики карт"""

    PROPERTY_NUM = 3

    def __init__(self, color, value, form):
        self.color = color
        self.value = value
        self.form = form
        self.properties = [self.color, self.value, self.form]

    def __repr__(self):
        # return "<Cards {0} {1} {2}>".format(self.color, self.value, self.form)
        return self.color + self.value + self.form

    def __hash__(self):
        return int(self.color + self.value + self.form)

    def __eq__(self, other):
        return self.properties == other.properties

    # '''
    # color identification (id)
    # 1: Red
    # 2: Blue
    # 3: Green
    # 4: Yellow
    # '''

    def color(self):
        return self.color


    # '''
    # Value identification
    # 1: 1
    # 2: 2
    # 3: 3
    # 4: 4
    # '''

    def value(self):
        return self.value


    # '''
    # Form identification (iden)
    # 1: Triangle
    # 2: Cross
    # 3: Round
    # 4: Square
    # '''

    def form(self):
        return self.form

class RegularCard(Card):
    pass

