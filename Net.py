import socket


class Server:
    """Описывает объекты типа сервер.
    Создет комнату."""

    _ip = '127.0.0.1'

    def __init__(self, port, sock, mother=False):
        self.port = port  # определяем порт, на котором будет находиться данна комната
        self.room = sock or socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)  # создаем сокет сервера
        self.room.bind((self._ip, port))  # соединяем сервер с конкретным ip
        # self.room.listen(4)  # принимаем посылки от не более чем 4-х источников
        self.mother = mother  # определяем материнский сервер

        if mother:
            self.rooms = set()  # в случае материнского сервера: содержит список всех доступных комнат
        else:
            self.clients = set()  # список клиентов на сервере в случае игрового сервера
            self.current_player = None  # текущий игрок
            self.play = False  # состояние игры на сервере

    def disconnection(self, client: Client):
        self.clients.remove(client)
        client.close()

    def turn(self):
        card = self.room.recv(1024, 'card')
        pos = self.room.recv(1024, 'pos')
        return card, pos

    def change_turn(self, new_player):
        for player in self.clients:
            if player == self.current_player:
                player.

        self.room.sendto(b'YouTurn', 'turn', new_player)
        self.current_player = new_player


class Client:
    """Описывает объекты типа Клиент.
    Создает объект типа клиент на сервере"""

    def __init__(self, tup, name=0, server: Server = 0):
        self.sock = tup[0]  # сокет, соответсующий данному клиенту
        self.addr = tup[1]  # адресс клиента
        self.name = name
        self.server = server

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
        """Посылает на сервер карту и ее позицию от клиента"""
        self.sock.send(bytes(card), 'card')
        self.sock.send(bytes(pos), 'pos')

    def start_turn(self):
        """Принимает информацию о начале хода"""
        data = self.sock.recv(1024, 'turn')
        if data == 'YouTurn':
            return 'StartTurn'

    def end_turn(self, flag):
        """Посылает информацю о конце собственного хода или принимает информацию о конце чужого хода
        True: конец собственного
        False: конец чужого"""
        if flag:
            self.sock.send(b'EndTurn', 'turn')
        else:
            name = self.sock.recv(1024, 'name')
            data = self.sock.recv(1024, 'turn')
            if data == 'EndTurn':
                return name


def create_mother(port):
    """Создает материнский сервер: большой сервер, от которого отходят более мелкие """
    server = Server(port, True)
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



