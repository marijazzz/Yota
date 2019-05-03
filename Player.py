from Pack import *


class Hand(object):
    """класс, описывающий состояние руки"""

    def __init__(self):
        self.cards = []  # Изначально рука пустая

    def add_card(self, card, position=None):
        """ Добавляет карту игроку """
        self.cards.append(card)

    def get_amount(self):
        """Возвращает количество карт"""
        return len(self.cards)

    def play_card(self, number):
        """Отыгрывание карты"""
        return self.cards.pop(number)  # убирает карту из руки и передает карту на обработку, чтобы положить на поле

   # def update(self, pack):
    #    """Обновление карт"""
     #   pack.cards += self.cards  # добавляем карты из руки в колоду
      #  self.cards = []  # убираем карты с руки
       # pack = Pack(pack.cards)  # обновление карт в колоде с учетом скинутых
        #for i in range(4):
         #   self.cards.append(pack.deal_card())  # даем в руку новые карты
        #return pack


class Player:
    """Класс, описывающий количество очков у игрока, количество и достоинство его карт"""

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id
        self.hand = Hand()
        self.score = 0

    def add_card(self, card, position=None):
        """Добавление карт"""
        self.hand.add_card(card)

#    def update(self, pack):
 #       """Обновление карт на руке (в случае пропуска хода)"""
  #      pack = self.hand.update(pack)  # обновляем руку и колоду
   #     self.end_turn()  # завершаем ход
    #    return pack  # возвращаем новую колоду

    def define_Joker(self, joker, color, value, form):
        """
        Передача игроком параметров Джокеру
        """
        joker.change(color, value, form)

    def get_Joker(self, joker):
        """
        Функция, осуществляющая очищение параметров Джокера, когда игрок забирает его со стола и добавление Джокера в руку
        """
        joker.clear()
        self.add_card(joker)

    def end_turn(self):
        """Завершение хода"""
        pass
