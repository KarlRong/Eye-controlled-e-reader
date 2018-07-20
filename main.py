# -*- coding: utf-8 -*-

# !/usr/bin/env python

import sys

import matplotlib.pyplot as plt
from PyQt4 import Qt
from src.window import MainWindow
from importlib import reload

reload(sys)


def main():
    print("Start ")

    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    qt_return_code = app.exec_()
    print('Qt return code:' + str(qt_return_code))
    sys.exit(qt_return_code)


if __name__ == '__main__':
    main()
