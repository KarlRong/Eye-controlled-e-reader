# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QWidget, QPushButton, QApplication, QTextBrowser

import time
import json


class TimeThread(QtCore.QThread):
    signal_time = QtCore.pyqtSignal(str, int)  # 信号

    def __init__(self, parent=None):
        super(TimeThread, self).__init__(parent)
        self.working = True
        self.num = 0

        import zmq
        port = "5570"

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        print("Collecting head pose updates...")

        self.socket.connect("tcp://127.0.0.1:%s" % port)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')

    def start_timer(self):
        self.num = 0
        self.start()

    def run(self):
        while self.working:
            print "Working", self.thread()
            msg = self.socket.recv_multipart()
            topic = msg[0]
            data = json.loads(msg[1])
            timestamp = data['timestamp']
            frame = data['frame']
            confidence = data['confidence']
            headPose = data['pose']
            gaze = data['gaze']
            print(timestamp)

            # self.signal_time.emit("Running time:", timestamp)  # 发送信号
            self.num += 1
            # self.sleep(1)


class TimeDialog(QWidget):
    def __init__(self):
        super(TimeDialog, self).__init__()
        self.timer_tv = QTextBrowser(self)
        self.init_ui()
        self.timer_t = TimeThread()
        self.timer_t.signal_time.connect(self.update_timer_tv)

    def init_ui(self):
        self.resize(300, 200)
        self.setWindowTitle('TimeDialog')
        self.timer_tv.setText("Wait")
        self.timer_tv.setGeometry(QtCore.QRect(10, 145, 198, 26))
        self.timer_tv.move(0, 15)

        btn1 = QPushButton('Quit', self)
        btn1.setToolTip('Click to quit')
        btn1.resize(btn1.sizeHint())
        btn1.move(200, 150)
        btn1.clicked.connect(QCoreApplication.instance().quit)

        start_btn = QPushButton('Start', self)
        start_btn.setToolTip("Click to start")
        start_btn.move(50, 150)
        self.connect(start_btn, QtCore.SIGNAL("clicked()"), self.click_start_btn)

    def click_start_btn(self):
        self.timer_t.start_timer()

    def update_timer_tv(self, text, number):
        self.timer_tv.setText(self.tr(text + " " + str(number)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    time_dialog = TimeDialog()
    time_dialog.show()

    sys.exit(app.exec_())
