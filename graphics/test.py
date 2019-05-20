import sys
import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Player:
    def __init__(self, name, score):
        self.player_name = name
        self.player_score = score

    def update(self, score):
        self.player_score = score


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
            stream >> image
            self.update(square)
            event.setDropAction(QtCore.Qt.MoveAction)
            if (self.play_field[square.x() // self.tile_size][square.y() // self.tile_size].get_image()) is None:
                if random.randint(0, 1) == 1:
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

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DecorationRole:
            return QIcon(self.images[index.row()].scaled(60, 60,
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        if role == QtCore.Qt.UserRole:
            return self.images[index.row()]
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
                image = QPixmap(self.data(index, QtCore.Qt.UserRole))
                stream << image
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
        print(images)

    def add_cards(self):
        for y in range(len(self.images), 4):
            if len(self.image_stack) != 0:
                img = self.image_stack.pop(0)
                card_image = img.image.copy(0, 0, 500, 500)
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
        self.rulesButton = QPushButton('Правила')
        self.playButton = QPushButton('Играть')
        self.zoom_inButton = QPushButton('zoom in')
        self.zoom_outButton = QPushButton('zoom out')
        self.end_turnButton = QPushButton('Закончить ход')
        self.exitButton = QPushButton('Exit')
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
        self.player = 'Player'
        self.setWindowTitle("Ёпта")

    def open_image(self):
        new_image = []
        z = ['411', '212', '312', '112', '342', '321', '234', '322', '333', '242', '222', '444']
        for i in range(12):
            temporary_image = Card()
            temporary_image.set_card(z[i])
            new_image.append(temporary_image)
        self.cardImage = new_image
        self.set_up_card()

    def set_up_card(self):
        self.model.set_stack(self.cardImage)
        self.model.add_cards()
        self.CardWidget.clear()

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
        self.player_name.setText('Player')
        self.splitter2.setOrientation(QtCore.Qt.Vertical)
        self.splitter2.addWidget(self.splitter)
        self.splitter2.addWidget(self.buttons)
        self.frameLayout.addWidget(self.player_name)
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
        self.splitter2.hide()
        self.splitter.hide()

    def set_name(self):
        text_box_value = self.player_name.text()
        self.player = text_box_value

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

    def end_turn(self):
        self.model.add_cards()

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
    app = QApplication(sys.argv)
    window = MainWindow()
    window.open_image()
    window.show()
    tmr = QtCore.QTimer()
    tmr.setSingleShot(True)
    tmr.timeout.connect(window.logo)
    tmr.start(1500)
    sys.exit(app.exec_())
