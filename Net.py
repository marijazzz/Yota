import socket
from Game_3 import GameServer
import Client.py


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
        """Инициирует отключение клиента"""
        self.clients.remove(client)
        client.close()

    def start_game(self):
        """Инициирует начало игры"""
        self.play = True
        self.room.send(b'StartGame')

    def turn(self):
        """Обрабатывает ход игрока"""
        card = self.room.recv(1024, 'card')
        pos = self.room.recv(1024, 'pos')
        return card, pos

    def send_error(self, id):
        """Отправляет ошибки"""
        self.room.sendto(b'error', 'type', (self._ip, id))
        self.room.sendto(bytes(self.send_message[message]['reason']), 'reason', (self._ip, id))

    def end_and_change_turn(self, new_player):
        """Передает ход следующему игроку"""
        self.room.send(bytes(self.current_player.cards), 'cards')
        self.room.send(bytes(new_player.name), 'name')
        self.room.send(bytes(self.send_message[message]['desk']), 'score')
        self.current_player = new_player
        self.room.sendto(b'YourTurn', 'type', (self._ip, new_player.addr))

    async def receive_message(self):
        """Обрабатывает сообщения от игрока"""
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
