# -*- coding: utf-8 -*-

# !/usr/bin/env python

import sys

from PyQt4.QtGui import QApplication
from src.window import MainWindow
from calibrate import calibrate

reload(sys)


def main():
    print "Start "

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    qt_return_code = app.exec_()
    print 'Qt return code:' + str(qt_return_code)
    sys.exit(qt_return_code)


if __name__ == '__main__':
    main()
