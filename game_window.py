import sys
import Net, Client
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import socket
import Game_3
import Client

import time

from Player import Player
from Session import GameSession
import game_window


REMOTE_SERVER = "www.google.com"


def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except socket.error:
        pass
    return False


class GameServer:
    PLAYERS_NEED_FOR_GAME = 4  # количество человек в одной игре
    bots_counter = 0  # счётчик ботов для обеспечения уникальности имени и ID

    def __init__(self, send_message, max_turn_duration_sec: int = 90):
        self.send_message = send_message  # сообщение от клиента
        self.waiting_for_game_players = []  # очередь из игроков, ожидающих начала игры
        self.game_sessions = []  # данная игровая сессия
        self._max_turn_duration_sec = max_turn_duration_sec

    async def go_go_game(self):
        """
        Запускает игру при наличии достаточного количества игроков
        """
        # для создания игровой сессии нужно взять первых PLAYERS_NEED_FOR_GAME игроков из очереди
        players_to_play = self.waiting_for_game_players[:self.PLAYERS_NEED_FOR_GAME]
        # обновление списка из оставшихся игроков
        self.waiting_for_game_players = self.waiting_for_game_players[self.PLAYERS_NEED_FOR_GAME:]
        # начало игровой сессии
        game_session = GameSession(players=players_to_play,
                                   send_message=self.send_message,
                                   max_turn_duration_sec=self._max_turn_duration_sec)
        self.game_sessions.append(game_session)
        await game_session.start_game()

    def add_bots_for_offline(self):
        for i in range(3):
            print('Adding bot...')
            self.bots_counter += 1
            client = Player(name='Bot {}'.format(self.bots_counter),
                            client_id='bot_id {}'.format(self.bots_counter))
            self.waiting_for_game_players.append(client)  # добавление бота в очередь

    async def on_message(self, client_id: str, message: dict):
        """
        Отклик сервера на различные сообщения
        :param client_id:
        :param message:
        :return:
        """

        async def send_for_all():
            for session in self.game_sessions:
                if session.has_client(client_id):
                    await session.on_message(client_id, message)

        # если игрок нажал "хочу играть"
        if message['type'] == 'HelloIWannaPlay':
            # проверяем наличие интернет-соединения
            if is_connected(REMOTE_SERVER):
                # если есть, то добавляем в очередь игры
                client = Player(client_id=client_id, name=message['user_name'])
                self.waiting_for_game_players.append(client)  # добавление данного игрока в очередь
            # если нет, запускаем игру с ботами
            else:
                self.add_bots_for_offline()  # добавляет трёх ботов
                await self.go_go_game()  # запускает игру

        # если игрок нажал "хочу играть один" и в сессии он один
        elif message['type'] == 'PlayAlone':
            client = Player(client_id=client_id, name=message['user_name'])
            self.waiting_for_game_players.append(client)  # добавление данного игрока в очередь
            self.add_bots_for_offline()  # добавляет трёх ботов
            await self.go_go_game()  # запускает игру

        # если сообщение о том, что игрок положил карту на стол
        elif message['type'] == 'IPutCard':
            await send_for_all()

        # окончание игры
        elif message['type'] == 'endTurn':
            await send_for_all()

        # пропуск хода
        elif message['type'] == 'endTurnAndRewindHand':
            await send_for_all()

        # выход из игры
        elif message['type'] == 'disconnection':
            await send_for_all()

    async def search_game(self):
        """
        Поиск игроков
        """
        # если игроков меньше, чем PLAYERS_NEED_FOR_GAME
        if len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
            # то пока их не станет PLAYERS_NEED_FOR_GAME
            while len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
                # обнуляем таймер
                timer = 0
                # запоминаем количество игроков при запуске таймера
                current_found = self.waiting_for_game_players
                # запускаем минуту ожидания
                while timer < 2:
                    # каждую секунду проверяем, изменилось ли количество игроков
                    if len(self.waiting_for_game_players) == current_found:
                        # если их столько же, итерируем ещё секунду
                        time.sleep(1)
                        timer += 1
                    # если изменилось, но все ещё не 4, то обнуляем счётчик и снова ждём
                    else:
                        current_found = len(self.waiting_for_game_players)
                        timer = 0
                # если за 60 секунд никого не нашёл, добавляем на пустые места ботов
                print('adding bot')
                self.bots_counter += 1
                client = Player(name='Bot {}'.format(self.bots_counter),
                                client_id='bot_id {}'.format(self.bots_counter))
                self.waiting_for_game_players.append(client)  # добавление бота в очередь
            await self.go_go_game()  # запускам игру

        # если игроков стало достаточное количество
        else:
            await self.go_go_game()  # запускам игру


class Server(GameServer):
    """Описывает объекты типа сервер.
    Создет комнату."""

    _ip = '127.0.0.1'
    _flags = [('type', 1), ('id', 0), ('name', 5), ('card', 2), ('cards', 6), ('pos', 3), ('reason', 4), ('score', 7)]

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
        card = self.room.recv(1024, 2)
        pos = self.room.recv(1024, 3)
        return card, pos

    def send_error(self, id):
        """Отправляет ошибки"""
        self.room.sendto(b'error', 1, (self._ip, id))
        self.room.sendto(bytes(self.send_message['message']['reason']), 4, (self._ip, id))

    def end_and_change_turn(self, new_player):
        """Передает ход следующему игроку"""
        self.room.send(bytes(self.current_player.name), 5)
        self.room.send(bytes(self.current_player.cards), 6)
        self.room.send(bytes(new_player.name), 5)
        self.room.send(bytes(self.send_message['message']['desk']), 7)
        self.current_player = new_player
        self.room.sendto(b'YourTurn', 1, (self._ip, new_player.addr))

    async def receive_message(self):
        """Обрабатывает сообщения от игрока"""
        id = self.room.recv(1024, 0)
        message_type = self.room.recv(1024, 1)

        if message_type == b'names':
            for client in self.slients:
                self.room.sendto(bytes(client.name), 5, (self._ip, id))

        if message_type == b'IPutCard':
            card = self.room.recv(1024, 2)
            pos = self.room.recv(1024, 3)
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
                self.room.sendto(b'error', 1, (self._ip, id))
                self.room.sendto(self.send_message[message]['reason'], 4, (self._ip, id))

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


def open_game(mother, window):  # срабатывает при открытии окна
    """Создает клиента компьютера, с которого был подан запрос на поиск игры"""
    connection = False  # проверяем установку соединения
    sock = socket.socket()
    sock.bind((mother._ip, 63022))
    client = Client.Client((sock, 63021), window)
    for room in mother.rooms:  # пробегаемся по всем доступным комнатам
        if not room.play and len(room.clients) < 4:  # если в комнате нет игры и там еще не 4 человека, то...
            client.sock.connect((mother._ip, room.port))
            room.clients.add(client)  # добавляем клиента в комнату
            client.server = room  # определяем комнату, как сервер данного клиента
            print(type(client.server))
            client.addr_serv(mother._ip, mother.port + 7 + len(mother.rooms))
            connection = True  # подтверждаем подключение

    if not connection:  # если соединение не установлено
        sock1 = socket.socket()
        server = Server(mother.port + 7 + len(mother.rooms), sock1)  # создаем клиент на данных сокете и порте
        print(type(server))
        sock1.connect_ex((server._ip, server.port))
        mother.rooms.add(server)  # добавляем комнату в список комнат
        client = Client.Client((sock, 63022), window)  # создаем клиента на новообретенном клиенте
        client.server = server  # определяем новую комнату, как сервер данного клиента
        client.addr_serv = (mother._ip, mother.port + 7 + len(mother.rooms))
        print(type(client.server))
        window.client = client


class Player:
    def __init__(self, name, score):
        self.player_name = name
        self.player_score = score
        self.current = 0

    def update(self, score):
        self.player_score = score

    def set_current(self):
        self.current = 1


class PlayersWidget(QWidget):
    def __init__(self, parent):
        super(PlayersWidget, self).__init__()
        self.parent = parent
        self.players = []
        self.rectangles = []
        self.setGeometry(0, 0, self.parent.width(), 50)
        x = self.width() / 4
        y = self.height() / 4
        for i in range(4):
            self.rectangles.append(QtCore.QRect(x * i, 0, x, y))
            self.players.append(Player('0', 0))

    def set_players(self, name):
        for i in range(4):
            self.players.append(Player(name[i], 0))
        print(self.players[3].player_name)

    def get_players(self):
        return self.players

    def update_players(self, name1, score, name2):
        for i in range(4):
            if self.players[i].player_name == name1:
                self.players[i].player_score = score
            if self.players[i].player_name == name2:
                self.players[i].set_current()
        self.update()

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        for i in range(4):
            text = self.players[i].player_name + ': '+ str(self.players[i].player_score)
            if self.players[i].current == 1:
                painter.setPen(QtCore.Qt.red)
            else:
                painter.setPen(QtCore.Qt.black)
            painter.drawText(self.rectangles[i], QtCore.Qt.AlignTop, text)
        painter.end()

class ImageWidget(QWidget):
    def __init__(self, parent):
        super(ImageWidget, self).__init__()
        self.image = QPixmap()
        self.image.load('logo.png')
        self.parent = parent

    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        rect = QtCore.QRect(0, 0, self.parent.width(), self.parent.height())
        painter.fillRect(rect, QtCore.Qt.white)
        painter.drawPixmap(0, 0, self.parent.width(), self.parent.height(), self.image)
        painter.end()


class Card:
    def __init__(self):
        self.card = None
        self.image = QPixmap()

    def set_card(self, card):
        self.card = card
        self.image.load(str(self.card) + '.png')


class Tile:
    def __init__(self):
        self.card = None
        self.piece_image = None

    def set_image(self, image):
        self.card = 1
        self.piece_image = image

    def other_player_card(self, card):
        self.card = 1
        self.piece_image = QPixmap()
        self.piece_image.load(card + '.png')

    def get_image(self):
        return self.piece_image


class CardWidget(QWidget):
    def __init__(self, parent=None):
        super(CardWidget, self).__init__()
        self.parent = parent
        self.field_size = 103
        self.tile_size = 100
        self.play_field = [[0] * self.field_size for i in range(self.field_size)]
        for i in range(self.field_size):
            for j in range(self.field_size):
                self.play_field[i][j] = Tile()
        self.setAcceptDrops(True)
        self.setMinimumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
        self.setMaximumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
        self.tile_image = self.load_tile_image('tile.png')
        self.central_tile_image = self.load_tile_image('tile.png')

    def zoom_in(self):
        if self.tile_size < 100:
            self.tile_size += 5
            self.setMinimumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.setMaximumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.update()
            self.parent.scroll_area.horizontalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * self.parent.CardWidget.field_size // 2)
            self.parent.scroll_area.verticalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * self.parent.CardWidget.field_size // 2)

    def zoom_out(self):
        if self.tile_size > 30:
            self.tile_size -= 5
            self.setMinimumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.setMaximumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.update()
            self.parent.scroll_area.horizontalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * (self.parent.CardWidget.field_size - 3) / 2)
            self.parent.scroll_area.verticalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * (self.parent.CardWidget.field_size - 1) / 2)

    def clear(self):
        for i in range(self.field_size):
            for j in range(self.field_size):
                self.play_field[i][j] = Tile()
        self.update()

    def load_tile_image(self, path=None):
        new_image = QPixmap()
        if not new_image.load(path):
            QMessageBox.warning(self, "Open Image", "The image file could not be loaded.", QMessageBox.Cancel)
            return
        return new_image

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('card'):

            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.update()
        event.accept()

    def dragMoveEvent(self, event):
        square = self.target_square(event.pos())
        if event.mimeData().hasFormat('card') and (self.play_field[square.x() // self.tile_size]
        [square.y() // self.tile_size].get_image()) is None:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
        self.update()

    def dropEvent(self, event):
        if event.mimeData().hasFormat('card'):
            card_data = event.mimeData().data('card')
            stream = QtCore.QDataStream(card_data, QtCore.QIODevice.ReadOnly)
            square = self.target_square(event.pos())
            image = QPixmap()
            name = QtCore.QPoint()
            stream >> image >> name
            self.update(square)
            event.setDropAction(QtCore.Qt.MoveAction)
            if (self.play_field[square.x() // self.tile_size][square.y() // self.tile_size].get_image()) is None:
                if self.parent.client.send_card(int(name.x()), (square.x(), square.y())) == True:
                    self.play_field[square.x() // self.tile_size][square.y() // self.tile_size].set_image(image)
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        r = QtCore.QRect(0, 0, self.field_size * self.tile_size, self.field_size * self.tile_size)
        painter.fillRect(r, QtCore.Qt.white)
        for x in range(self.field_size):
            for y in range(self.field_size):
                if self.play_field[x][y].card is None:
                    if x == 52 and y == 52:
                        painter.drawPixmap(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size,
                                           self.central_tile_image)
                    else:
                        painter.drawPixmap(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size,
                                           self.tile_image)
                else:
                    painter.drawPixmap(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size,
                                       self.play_field[x][y].get_image())

        painter.end()

    def target_square(self, position):
        return QtCore.QRect(position.x() // self.tile_size * self.tile_size,
                            position.y() // self.tile_size * self.tile_size, self.tile_size, self.tile_size)


class CardModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        super(CardModel, self).__init__(parent)
        self.image_stack = []
        self.images = []
        self.hand = []

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DecorationRole:
            return QIcon(self.images[index.row()].scaled(60, 60,
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        if role == QtCore.Qt.UserRole:
            return self.images[index.row()]
        if role == QtCore.Qt.UserRole + 1:
            return self.hand[index.row()]
        return None

    def add_card(self, image):
        row = len(self.images)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.images.insert(row, image)
        self.endInsertRows()

    def flags(self, index):
        if index.isValid():
            return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                    QtCore.Qt.ItemIsDragEnabled)
        return QtCore.Qt.ItemIsDropEnabled

    def removeRows(self, row, count, parent):
        if parent.isValid():
            return False
        if row >= len(self.images) or row + count <= 0:
            return False
        begin_row = max(0, row)
        end_row = min(row + count - 1, len(self.images) - 1)
        self.beginRemoveRows(parent, begin_row, end_row)
        del self.images[begin_row:end_row + 1]
        self.endRemoveRows()
        return True

    def mimeData(self, indexes):
        mime_data = QtCore.QMimeData()
        encoded_data = QtCore.QByteArray()
        stream = QtCore.QDataStream(encoded_data, QtCore.QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid():
                name = self.data(index, QtCore.Qt.UserRole + 1)
                image = QPixmap(self.data(index, QtCore.Qt.UserRole))
                stream << image << name
        mime_data.setData('card', encoded_data)
        return mime_data

    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.images)

    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction

    def set_stack(self, images):
        self.image_stack = images

    def clear(self):
        self.images = []
        self.hand = []

    def add_cards(self):
        for y in range(len(self.images), 4):
            if len(self.image_stack) != 0:
                img = self.image_stack.pop(0)
                card_image = img.image.copy(0, 0, 500, 500)
                print(img.card)
                self.hand.append(QtCore.QPoint(int(img.card), 0))
                self.add_card(card_image)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.frame = QFrame()
        self.frameLayout = QGridLayout(self.frame)
        self.cardList = QListView()
        self.model = CardModel(self)
        self.CardWidget = CardWidget(parent=self)
        self.scroll_area = QScrollArea()
        self.scroll_widget = self.CardWidget
        self.splitter = QSplitter()
        self.players_widget = PlayersWidget(self)
        self.rulesButton = QPushButton('Правила')
        self.playButton = QPushButton('Играть')
        self.zoom_inButton = QPushButton('zoom in')
        self.zoom_outButton = QPushButton('zoom out')
        self.end_turnButton = QPushButton('Закончить ход')
        self.exitButton = QPushButton('Exit')
        self.free_handButton = QPushButton('Скинуть руку')
        self.splitter2 = QSplitter()
        self.buttons = QFrame()
        self.buttonLayout = QHBoxLayout(self.buttons)
        self.player_name = QLineEdit()
        self.set_nameButton = QPushButton('Ввести имя')
        self.tmp_widget = ImageWidget(self)
        self.cardImage = None
        self.setGeometry(200, 200, 400, 400)
        self.set_up_menus()
        self.set_up_widgets()
        self.client = None
        self.setWindowTitle("Ёпта")

    def open_image(self):
        new_image = []
        deck = ['411', '212', '312', '112', '342', '321', '234', '322', '333', '242', '222', '444']
        for i in range(12):
            temporary_image = Card()
            temporary_image.set_card(deck[i])
            new_image.append(temporary_image)
        self.cardImage = new_image
        self.set_up_card()

    def set_up_card(self):
        self.model.set_stack(self.cardImage)
        self.model.add_cards()
        self.CardWidget.clear()

    def set_up_card1(self):
        self.model.set_stack(self.cardImage)
        self.model.add_cards()


    def set_up_menus(self):
        game_menu = self.menuBar().addMenu("&Game")
        exit_action = game_menu.addAction("E&xit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(qApp.quit)
        rules_action = game_menu.addAction('Rules')
        rules_action.triggered.connect(self.show_message)
        rules_action.setShortcut("Ctrl+R")

    def set_up_widgets(self):
        self.cardList.setDragEnabled(True)
        self.cardList.setViewMode(QListView.IconMode)
        self.cardList.setIconSize(QtCore.QSize(80, 80))
        self.cardList.setGridSize(QtCore.QSize(90, 90))
        self.cardList.setSpacing(10)
        self.cardList.setMovement(QListView.Snap)
        self.cardList.setAcceptDrops(True)
        self.cardList.setDropIndicatorShown(True)
        self.cardList.setModel(self.model)
        self.cardList.setMaximumWidth(100)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * (self.CardWidget.field_size - 10) / 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * (self.CardWidget.field_size - 5) / 2)
        self.splitter.addWidget(self.cardList)
        self.splitter.addWidget(self.scroll_area)
        self.buttonLayout.addWidget(self.rulesButton)
        self.buttonLayout.addWidget(self.playButton)
        self.buttonLayout.addWidget(self.zoom_inButton)
        self.buttonLayout.addWidget(self.zoom_outButton)
        self.buttonLayout.addWidget(self.end_turnButton)
        self.buttonLayout.addWidget(self.exitButton)
        self.buttonLayout.addWidget(self.set_nameButton)
        self.buttonLayout.addWidget(self.free_handButton)
        self.free_handButton.clicked.connect(self.end_turn)
        self.player_name.setText('Player')
        self.splitter2.setOrientation(QtCore.Qt.Vertical)
        self.splitter2.addWidget(self.splitter)
        self.splitter2.addWidget(self.buttons)
        self.frameLayout.addWidget(self.player_name)
        self.splitter2.addWidget(self.players_widget)
        self.frameLayout.addWidget(self.splitter2)
        self.setCentralWidget(self.frame)
        self.set_nameButton.clicked.connect(self.set_name)
        self.rulesButton.clicked.connect(self.show_message)
        self.playButton.clicked.connect(self.start_game)
        self.zoom_inButton.clicked.connect(self.zoom_in)
        self.zoom_outButton.clicked.connect(self.zoom_out)
        self.end_turnButton.clicked.connect(self.end_turn)
        self.exitButton.clicked.connect(qApp.quit)
        self.player_name.hide()
        self.frameLayout.addWidget(self.tmp_widget)
        self.tmp_widget.show()
        self.set_nameButton.show()
        self.end_turnButton.hide()
        self.zoom_inButton.hide()
        self.zoom_outButton.hide()
        self.free_handButton.hide()
        self.splitter2.hide()
        self.splitter.hide()
        self.players_widget.show()

    def set_name(self):
        text_box_value = self.player_name.text()
        self.client.give_name(text_box_value)

    def logo(self):
        self.tmp_widget.hide()
        self.splitter2.show()
        self.player_name.show()

    def start_game(self):
        self.playButton.hide()
        self.rulesButton.hide()
        self.zoom_inButton.show()
        self.zoom_outButton.show()
        self.end_turnButton.show()
        self.splitter.show()
        self.player_name.hide()
        self.set_nameButton.hide()
        self.players_widget.show()
        self.free_handButton.show()
        self.zoom_inButton.setEnabled(False)
        self.zoom_outButton.setEnabled(False)
        self.end_turnButton.setEnabled(False)
        self.free_handButton.setEnabled(False)
        name = ['waiting', 'waiting', 'waiting', 'waiting']
        self.players_widget.set_players(name)
        self.waiting_done()

    def waiting_done(self):
        self.zoom_inButton.setEnabled(True)
        self.zoom_outButton.setEnabled(True)
        self.end_turnButton.setEnabled(True)
        self.free_handButton.setEnabled(True)
        #self.players_widget.set_players(self.client.get_names())

    def end_turn(self):
        self.client.end_turn(True)
        self.model.add_cards()

    def player_turn(self, cards, name1, score, name2, deck = None):
        for i in range(len(cards)):
            self.CardWidget.play_field[cards[1][0]][cards[1][1]].other_player_card(cards[0])
        self.players_widget.update_players(name1, score, name2)
        if deck is not None:
            new_image = []
            for i in range(len(deck)):
                temporary_image = Card()
                temporary_image.set_card(deck[i])
                new_image.append(temporary_image)
            self.cardImage = new_image
            self.set_up_card1()




    def zoom_in(self):
        self.CardWidget.zoom_in()

    def show_message(self):
        try:
            text = open(r"rules.txt", "r", encoding="utf8").read()
        except Exception as e:
            print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Правила")
        msg.setInformativeText(text)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def zoom_out(self):
        self.CardWidget.zoom_out()


if __name__ == '__main__':
    Mother = create_mother(8017)
    app = QApplication(sys.argv)
    window = MainWindow()
    open_game(Mother, window)
    window.open_image()
    window.show()
    tmr = QtCore.QTimer()
    tmr.setSingleShot(True)
    tmr.timeout.connect(window.logo)
    tmr.start(1500)
    sys.exit(app.exec_())
