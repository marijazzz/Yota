class Hand(object):
    """Класс, описывающий состояние руки"""

    def __init__(self):
        self.cards = []  # Изначально рука пустая

    def add_card(self, card):
        """ Добавляет карту игроку """
        self.cards.append(card)

    def get_amount(self):
        """
        Возвращает количество карт
        :return:
        """
        return len(self.cards)

    def play_card(self, number):
        """
        Отыгрывание карты
        :param number:
        :return:
        """
        return self.cards.pop(number)  # убирает карту из руки и передает карту на обработку, чтобы положить на поле


class Player:
    """Класс, описывающий количество очков у игрока, количество и достоинство его карт"""

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id
        self.hand = Hand()
        self.score = 0

    def add_card(self, card):
        """
        Добавление карт
        :param card:
        :return:
        """
        self.hand.add_card(card)
