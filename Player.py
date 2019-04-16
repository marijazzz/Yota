class Hand(object):
    """класс, описывающий состояние руки"""
    def __init__(self, name):
        self.name = name # имя игрока
        self.cards = [] # Изначально рука пустая

    def add_card(self, card):
        """ Добавляет карту игроку """
        self.cards.append(card)

    def get_amount(self):
        """Возвращает количество карт"""
        return len(self.cards)

class Player:
    """Класс, описывающий количество очков у игрока, количество и достоинство его карт"""
    def __init__(self, name):
        self.name = name
        self.hand = Hand()
        self.score = 0

    def add_card(self, card):
        """Добавление карт"""
        self.hand.add_card(card)