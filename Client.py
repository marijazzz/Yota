import socket
import asyncio
from Game_3 import GameServer
import game_window


class Client:
    """Описывает объекты типа Клиент.
    Создает объект типа клиент на сервере"""

    def __init__(self, tup, window,  name='Player', server = None):
        self.sock = tup[0]  # сокет, соответсующий данному клиенту
        self.addr = tup[1]  # адресс клиента
        self.name = name  #
        self.server = server  #
        self.window = window
        self.cards = []  #

    def get_id(self):
        """Передает id клиента"""
        return self.addr

    def get_name(self, name):
        """Присваивает имя клиенту"""
        self.name = name

    def give_name(self, name):
        """Присваивает имя клиенту"""
        self.name = name

    def close(self):
        """Закрывает сокет клиента"""
        self.sock.close()

    def get_names(self):
        """Получает имена всех игроков"""
        self.sock.send(bytes(self.addr), 'id')
        self.sock.send(b'names', 'type')
        names = []
        for i in range(4):
            names.append(str(self.sock.recv(1024, 'name')))
        return names

    def send_card(self, card, pos):
        """Передает карты, которые хочется сыграть"""
        self.sock.send(bytes(self.addr), 'id')
        self.sock.send(b'IPutCard', 'type')
        self.sock.send(bytes(card), 'card')
        self.sock.send(bytes(pos), 'pos')
        data = self.sock.recv(1024, 'type')
        if data == b'error':
            reason = self.sock.recv(1024, 'reason')
            return False
        self.cards.append((card, pos))
        return True

    def start_turn(self):
        """Инициирует начало хода"""
        name = self.sock.recv(1024, 'name')
        if name == self.name:
            return True
        return False

    def end_turn(self, flag, end=None):
        """Инициирует конец хода"""
        deck = None
        if flag:
            self.sock.send(bytes(self.addr), 'id')
            if self.cards:
                cards = []
                name1 = self.name
                self.sock.send(b'endTurn', 'type')
                self.sock.send(bytes(self.cards), 'cards')
            else:
                self.sock.send(b'endTurnAndRewindHand', 'type')
                deck = self.sock.recv(1024, 'cards')  # ВАЖНЫЙ КОММЕНТ: тут присылается новая колода

        else:
            name1 = self.sock.recv(1024, 'name')

            if end == b'endTurn':
                cards = list(self.sock.recv(1024, 'cards'))  # ВАЖНЫЙ КОММЕНТ: тут присылаются положенные карты
                cards = [list(x) for x in cards]
                cards = [[str(x[0]), tuple(x[1])] for x in cards]
            elif end == b'endTurnAndRewindHand':
                deck = list(self.sock.recv(1024, 'cards'))  # ВАЖНЫЙ КОММЕНТ: тут присылается новая колода
                deck = [str(x) for x in deck]
        name = str(self.sock.recv(1024, 'name'))  # ВАЖНЫЙ КОММЕНТ: тут присылается имя нового текущего игрока
        scores = dict(self.sock.recv(1024, 'scores'))  # ВАЖНЫЙ КОММЕНТ: тут присылается текущий счет
        score = scores[bytes(name)]
        self.window.player_turn(cards, name1, score, name, deck)

    def disconnection(self):
        """Посылает на сервер сообзение о желании выйти из игры"""
        self.sock.send(b'disconnection', 'type')

    async def receive_message(self):
        """Обрабатывает сигналы от сервера"""
        message_type = self.sock.recv(1024, 'type')
        if message_type == b'YourTurn':
            self.start_turn()
        if message_type == b'endTurn':
            self.end_turn(False, message_type)
        if message_type == b'endTurnAndRewindHand':
            self.end_turn(False, message_type)
        if message_type == b'error':
            reason = str(self.sock.recv(1024, 'reason'))  # ВАЖНЫЙ КОММЕНТ: тут присылается обоснование ошибки
