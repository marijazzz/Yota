class Card:
    """класс, описывающий характеристики обычных карт"""

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

    def color(self):
        return self.color

    def value(self):
        return self.value

    def form(self):
        return self.form


print(Card('1', '2', '3').__repr__())
