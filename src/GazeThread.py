# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtCore
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QWidget, QPushButton, QApplication, QTextBrowser

import time
import json
import zmq


class GazeThread(QtCore.QThread):
    signal_timeStamp = QtCore.pyqtSignal(str, bool)  # 信号

    def __init__(self, parent=None):
        super(GazeThread, self).__init__(parent)

        port = "5570"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        print("Collecting head pose updates...")

        self.socket.connect("tcp://127.0.0.1:%s" % port)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')

        self.lastScrollTime = 0

    def run(self):
        while True:
            msg = self.socket.recv_multipart()
            topic = msg[0]
            data = json.loads(msg[1])
            timestamp = data['timestamp']
            frame = data['frame']
            confidence = data['confidence']
            headPose = data['pose']
            headUpDown = headPose['pose_Rx'] * 180/3.1415926
            gaze = data['gaze']
            gaze_angle_y = gaze['gaze_angle_y'] * 180 / 3.1415926
            gaze_point_x = gaze['gaze_screen_x']
            gaze_point_y = gaze['gaze_screen_y']
            print("GazeThread " + "timestamp: " + str(timestamp) + " gaze_point: " + str(gaze_point_x) + " " + str(gaze_point_y))

            # if headUpDown < -20 and timestamp - self.lastScrollTime > 1.5:
            #     self.signal_timeStamp.emit("GazeTimestamp:", True)  # 发送信号
            #     self.lastScrollTime = timestamp
            # elif headUpDown > 5 and timestamp - self.lastScrollTime > 1.5:
            #     self.signal_timeStamp.emit("GazeTimestamp:", False)  # 发送信号
            #     self.lastScrollTime = timestamp

            # if gaze_angle_y > 1 and timestamp - self.lastScrollTime > 1.5:
            #     self.signal_timeStamp.emit("GazeTimestamp:", True)  # 发送信号
            #     self.lastScrollTime = timestamp
            # elif gaze_angle_y < -5 and timestamp - self.lastScrollTime > 1.5:
            #     self.signal_timeStamp.emit("GazeTimestamp:", False)  # 发送信号
            #     self.lastScrollTime = timestamp
            if gaze_point_y > 122 and timestamp - self.lastScrollTime > 1.5:
                self.signal_timeStamp.emit("GazeTimestamp:", True)  # 发送信号
                self.lastScrollTime = timestamp
            time.sleep(0.01)
