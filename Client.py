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

    def send_id(self):
        self.sock.send(b'id', 'type')
        self.sock.send(bytes(self.addr), 'id')

    def send_name(self):
        self.sock.send(b'name', 'type')
        self.sock.send(bytes(self.name), 'name')

    def send_card(self, card, pos):
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
            name = self.sock.recv(1024, 'name')  # ВЫЖНЫЙ КОММЕНТ: тут присылается имя нового текущего игрока

    async def receive_message(self):
        message_type = self.sock.recv(1024, type)
        if message_type == b'StartTurn':
            self.start_turn()
        if message_type == b'endTurn':
            self.end_turn(False)
