import sys

from PyQt5.QtWidgets import QApplication
from Core.controllers import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()
    window.setWindowTitle('Runge Kutta')
    sys.exit(app.exec_())