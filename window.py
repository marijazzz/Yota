import PyQt5
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from PyQt5 import uic
import start
from PyQt5.QtGui import QPainter, QColor


class StartDesigner(QMainWindow, start.Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setupUi(self)
        self.flag = False
        self.rules.clicked.connect(self.showMessage)
        self.start_game.clicked.connect(self.startGame)
        self.drawButton.hide()
        self.drawButton.clicked.connect(self.draw)


    def showMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Правила")
        msg.setInformativeText("This is additional information")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def startGame(self):
        self.start_game.hide()
        self.rules.hide()
        self.drawButton.show()

    def draw(self):
        self.flag = True
        self.update()

    def paintEvent(self, QPaintEvent):
        if self.flag:
            qp = QPainter()
            qp.begin(self)
            self.card(qp)
            qp.end()

    def card(self, qp):
        qp.setBrush(QColor(255, 255, 255))
        qp.drawRect(100, 100, 100, 100)
        qp.setBrush(QColor(0, 0, 0))
        qp.drawRect(120, 120, 60, 60)
        qp.setBrush(QColor(255, 0, 0))
        qp.drawEllipse(120 , 120 , 60, 60)

if __name__ == '__main__':
    app = QApplication([])
    w = StartDesigner()
    w.show()
    app.exec()
