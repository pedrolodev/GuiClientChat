from PyQt6 import QtWidgets
import sys
from mainWindow import MyWindowClass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MyWindow = MyWindowClass()
    MyWindow.show()
    sys.exit(app.exec())
