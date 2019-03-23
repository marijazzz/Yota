import PyQt5
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import *
from PyQt5 import uic
import start


class StartDesigner(QMainWindow, start.Ui_MainWindow):
    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setupUi(self)
        self.pravila.clicked.connect(self.showMessage)


    def quit(self):
        QApplication.instance().quit()

    def showMessage(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("Правила")
        msg.setInformativeText("This is additional information")

        msg.setStandardButtons(QMessageBox.Ok)


        retval = msg.exec_() 


if __name__ == '__main__':
    app = QApplication([])
    w = StartDesigner()
    w.show()
    app.exec()
