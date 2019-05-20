import socket
from Game_3 import GameServer


class Server(GameServer):
    """Описывает объекты типа сервер.
    Создет комнату."""

    _ip = '127.0.0.1'
    _flags = ['type', 'id', 'name', 'card', 'cards', 'pos', 'reason']

    def __init__(self, port, sock, mother=False):
        self.port = port  # определяем порт, на котором будет находиться данна комната
        self.room = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)  # создаем сокет сервера
        self.room.bind((self._ip, port))  # соединяем сервер с конкретным ip
        self.room.listen(4)  # принимаем посылки от не более чем 4-х источников
        self.mother = mother  # определяем материнский сервер

        if mother:
            self.rooms = set()  # в случае материнского сервера: содержит список всех доступных комнат
        else:
            self.clients = set()  # список клиентов на сервере в случае игрового сервера
            self.current_player = None  # текущий игрок
            self.play = False  # состояние игры на сервере

    def disconnection(self, client):
        self.clients.remove(client)
        client.close()

    def start_game(self):
        self.play = True
        self.room.send(b'StartGame')

    def turn(self):
        card = self.room.recv(1024, 'card')
        pos = self.room.recv(1024, 'pos')
        return card, pos

    def send_error(self, id):
        self.room.sendto(b'error', 'type', (self._ip, id))
        self.room.sendto(bytes(self.send_message[message]['reason']), 'reason', (self._ip, id))

    def end_and_change_turn(self, new_player):
        """Передает ход следующему игроку"""
        self.room.send(bytes(self.current_player.cards), 'cards')
        self.room.send(bytes(new_player.name), 'name')
        self.room.send(b'current_score', 'type')
        self.room.send(bytes(self.send_message[message]['desk']), 'score')
        self.current_player = new_player
        self.room.sendto(b'YourTurn', 'type', (self._ip, new_player.addr))

    async def receive_message(self):
        id = self.room.recv(1024, 'id')
        message_type = self.room.recv(1024, 'type')

        if message_type == b'names':
            for client in self.slients:
                self.room.sendto(bytes(client.name), 'name', (self._ip, id))

        if message_type == b'IPutCard':
            card = self.room.recv(1024, 'card')
            pos = self.room.recv(1024, 'pos')
            message = {'type': str(message_type), 'card': str(card), 'desk_position': tuple(pos)}
            self.on_message(str(id), message)

        if message_type == b'endTurn':
            message = {'type': message_type}
            b = self.on_message(str(id), message)
            if b is None:
                new_player_id = int(self.players[self.current_turn_player_index].client_id)
                new_player = None
                for client in self.clients:
                    if client.addr == new_player_id:
                        new_player = client
                        break
                self.end_and_change_turn(new_player)
            else:
                self.room.sendto(b'error', 'type', (self._ip, id))
                self.room.sendto(self.send_message[message]['reason'], 'reason', (self._ip, id))

        if message_type == b'endTurnAndRewindHand':
            message = {'type': message_type}
            b = self.on_message(str(id), message)
            if b is None:
                new_player_id = int(self.players[self.current_turn_player_index].client_id)
                new_player = None
                for client in self.clients:
                    if client.addr == new_player_id:
                        new_player = client
                        break
                self.end_and_change_turn(new_player)

        if message_type == b'disconnection':
            message = {'type': message_type}
            self.on_message(id, message)
            self.disconnection()


class Client:
    """Описывает объекты типа Клиент.
    Создает объект типа клиент на сервере"""

    def __init__(self, tup, name=None, server: Server = None):
        self.sock = tup[0]  # сокет, соответсующий данному клиенту
        self.addr = tup[1]  # адресс клиента
        self.name = name
        self.server = server
        self.cards = []

    def get_name(self, name):
        """Присваивает имя клиенту"""
        self.name = name

    def send_name(self):
        """Передает имя"""
        self.sock.send(bytes(self.name), 'name')

    def close(self):
        """Закрывает сокет клиента"""
        self.sock.close()

    def turn(self, card: str, pos: tuple):
        """Посылает на сервер карту и ее позицию от клиента и принимает правильность постановки карты"""
        self.sock.send(bytes(card), 'card')
        self.sock.send(bytes(pos), 'pos')
        data = self.sock.recv(1024, 'check')
        if data:
            self.cards.append((card, pos))
            return True
        return False

    def end_turn(self, flag):
        """Посылает информацю о конце собственного хода или принимает информацию о конце чужого хода
        True: конец собственного
        False: конец чужого"""
        if flag:
            self.sock.send(bytes(self.cards), 'cards')
        self.sock.recv(1024, 'name')

    def disconnection(self):
        """Посылает на сервер сообзение о желании выйти из игры"""
        self.sock.send(b'disconnection', 'type')

    def work(self):
        """Определяет работу клиента"""


def create_mother(port):
    """Создает материнский сервер: большой сервер, от которого отходят более мелкие """
    server = Server(port, None, True)
    return server


Mother = create_mother(9909)


def open_game(mother):  # срабатывает при открытии окна
    """Создает клиента компьютера, с которого был подан запрос на поиск игры"""
    connection = False  # проверяем установку соединения
    for room in mother.rooms:  # пробегаемся по всем доступным комнатам
        if not room.play and len(room.clients) < 4:  # если в комнате нет игры и там еще не 4 человека, то...
            client = Client(room.room.accept())  # создаем клиента в этой комнате
            room.clients.add(client)  # добавляем клиента в комнату
            client.server = room  # определяем комнату, как сервер данного клиента
            connection = True  # подтверждаем подключение

    if not connection:  # если соединение не установлено
        sock, addr = mother.accept()  # создаем сокет и адресс новой комнаты
        server = Server(addr, sock)  # создаем клиент на данных сокете и порте
        mother.rooms.add(server)  # добавляем комнату в список комнат
        client = Client(server.room.accept())  # создаем клиента на новообретенном клиенте
        client.server = server  # определяем новую комнату, как сервер данного клиента
