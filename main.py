import sys
from PyQt5.QtWidgets import QApplication
from src.window import MainWindow

from importlib import reload

reload(sys)


def main():
    print("Start ")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    qt_return_code = app.exec_()
    print('Qt return code:' + str(qt_return_code))
    sys.exit(qt_return_code)


if __name__ == '__main__':
    main()
