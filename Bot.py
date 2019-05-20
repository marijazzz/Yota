import Desk
from Exception import *
from Cards import Card


class Bot:
    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.W_AREA = Desk.Desk.MAX_DIMENSION
        self.current_state = []
        self.hand = []
        self.this_card = 0

    def current_desk_state(self, engaged):
        """
        Идентифицируем состояние поля
        :param engaged: получаем его из message['desk']
        :return: массив с нулями на свободных местах и единицами на занятых
        """
        current_state = [[0 for _ in range(self.W_AREA)] for _ in range(self.W_AREA)]
        for elem in engaged:
            current_state[elem[0]][elem[1]] = 1
        return current_state

    def score_best(self, this_card):
        card = self.hand[this_card]
        for x in range(1, len(self.current_state)-1):
            for y in range(1, len(self.current_state)-1):
                flag = False
                flag += (self.current_state[x+1][y] == 1)
                flag += (self.current_state[x-1][y] == 1)
                flag += (self.current_state[x][y+1] == 1)
                flag += (self.current_state[x][y-1] == 1)
                flag *= (self.current_state[x][y] == 0)
                if flag:
                    try:
                        message = {'type': 'IPutCard',
                                   'card': Card(card[:1], card[1:2], card[2:3]),
                                   'desk_position': (x, y)}
                        return message
                    except AddCardException:
                        message = {'type': 'endTurn'}
                        return message

    def on_message(self, message):
        """
        Отклик бота на различные сообщения
        :param message:
        """
        if message['type'] == 'error':
            self.this_card += 1
            return self.score_best(self.this_card)
        # если приходит сообщение о состоянии руки
        if message['type'] == 'HandState':
            self.hand = message['hand']
            return None

        # если приходит сообщение о состоянии доски
        elif message['type'] == 'DeskState':
            self.current_state = self.current_desk_state(message['desk'])
            return None

        # если приходит сообщение о том, что очередь бота
        elif message['type'] == 'YourTurn':
            self.this_card = 0
            return self.score_best(self.this_card)
