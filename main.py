import sys
from PyQt5.QtWidgets import QApplication
from src.window import MainWindow
import matlab.engine
from importlib import reload
from calibrate import Calibrate

reload(sys)


def main():
    print("Start Calibrate:\n ")
    eng = matlab.engine.start_matlab()
    Calibrate.calibrate(eng)
    print("Start e-book reader:\n ")
    app = QApplication(sys.argv)
    window = MainWindow(eng)
    window.show()
    qt_return_code = app.exec_()
    print('Qt return code:' + str(qt_return_code))
    sys.exit(qt_return_code)


if __name__ == '__main__':
    main()
