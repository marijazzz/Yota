import socket
import asyncio
from Game_3 import GameServer
from Net.py import Server


class Client:
    """Описывает объекты типа Клиент.
    Создает объект типа клиент на сервере"""

    def __init__(self, tup, name=None, server: Server = None):
        self.sock = tup[0]  # сокет, соответсующий данному клиенту
        self.addr = tup[1]  # адресс клиента
        self.name = name
        self.server = server
        self.cards = []

    def get_id(self):
        return self.addr

    def give_name(self, name):
        self.name = name

    def det_names(self):
        self.sock.send(bytes(self.addr), 'id')
        self.sock.send(b'names', 'type')
        names = []
        for i in range(4):
            names.append(str(self.sock.recv(1024, 'name')))
        return names

    def get_name(self):
        return self.name

    def send_card(self, card, pos):
        self.sock.send(bytes(self.addr), 'id')
        self.sock.send(b'IPutCard', 'type')
        self.sock.send(bytes(card), 'card')
        self.sock.send(bytes(pos), 'pos')
        data = self.sock.recv(1024, 'type')
        if data == b'error':
            reason = self.sock.recv(1024, 'reason')
            return reason
        self.cards.append((card, pos))
        return True

    def start_turn(self):
        name = self.sock.recv(1024, 'name')
        if name == self.name:
            return True
        return False

    def end_turn(self, flag):
        if flag:
            self.sock.send(bytes(self.addr), 'id')
            if self.cards:
                self.sock.send(b'endTurn', 'type')
                self.sock.send(bytes(self.cards), 'cards')
            else:
                self.sock.send(b'endTurnAndRewindHand', 'type')
                deck = self.sock.recv(1024, 'cards')  # ВАЖНЫЙ КОММЕНТ: тут присылается новая колода

        else:
            end = self.sock.recv(1024, 'type')
            if end == b'endTurn':
                cards = self.sock.recv(1024, 'cards')  # ВАЖНЫЙ КОММЕНТ: тут присылаются положенные карты
            elif end == b'endTurnAndRewindHand':
                deck = self.sock.recv(1024, 'cards')  # ВАЖНЫЙ КОММЕНТ: тут присылается новая колода
            name = self.sock.recv(1024, 'name')  # ВАЖНЫЙ КОММЕНТ: тут присылается имя нового текущего игрока

    async def receive_message(self):
        message_type = self.sock.recv(1024, 'type')
        if message_type == b'YourTurn':
            self.start_turn()
        if message_type == b'endTurn':
            self.end_turn(False)
        if message_type == b'error':
            reason = str(self.sock.recv(1024, 'reason'))  # ВАЖНЫЙ КОММЕНТ: тут присылается обоснование ошибки
        if message_type == b'current_score':
            score = list(self.sock.recv(1024, 'score'))
