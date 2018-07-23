# -*- coding: utf-8 -*-

# !/usr/bin/env python

from tkinter import *
import random
import time
from time import gmtime, strftime
import zmq
import json
import queue
import threading
import pandas as pd
import numpy as np
import math
import matlab.engine

class Ball:
    def __init__(self, canvas, color):
        self.color = color
        self.canvas = canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        # 来回反弹
        # --self.x = 0
        # --self.y = -1
        starts = [-5, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3
        self.posBall_x = 0
        self.posBall_y = 0

        # winfo_height()函数来获取画布当前的高度，赋值给对象变量
        self.canvas_height = self.canvas.winfo_height()
        # 获取X轴坐标
        self.canvas_width = self.canvas.winfo_width()
        print('canvas: ' + str(self.canvas_width) + ' ' + str(self.canvas_height))
        self.queue = queue.Queue()
        self.gazeSubscriber = GazeSubscriber(self.queue)

    def draw_class(self):
        self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=self.color)
        x_ball = random.randint(1, 4) * (self.canvas_width / 8) + self.canvas_width / 16
        y_ball = random.randint(0, 4) * (self.canvas_height / 5) + self.canvas_height / 10
        self.canvas.move(self.id, x_ball, y_ball)
        print('Classification: ' + str(x_ball) + ' ' + str(y_ball))

        self.posBall = [x_ball, y_ball]
        msg = self.posBall
        self.queue.put(msg)

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        # 获取某个对象在画布的坐标，返回一个数组（两个坐标，左上角的坐标和右下角的两个坐标）
        pos = self.canvas.coords(self.id)
        posBall_x = 0.5 * (pos[0] + pos[2])
        posBall_y = 0.5 * (pos[1] + pos[3])
        self.posBall = [posBall_x, posBall_y]
        msg = self.posBall
        self.queue.put(msg)
        print("Queue size: " + str(self.queue.qsize()))
        # 打印获取的坐标
        print("Pos: " + str(pos))
        # 如果最上面的纵轴坐标在顶上，则往下移动一个像素
        if pos[1] <= 0:
            self.y = 2
        # 如果最下面的纵轴坐标在底上，则向上移动
        if pos[3] > self.canvas_height:
            self.y = -2
        # 宽度控制#
        # 如果在左边框了，那么向右边移动3像素
        if pos[0] <= 0:
            self.x = 5
        # 如果到右边框了，左移动3像素
        if pos[2] > self.canvas_width:
            self.x = -5


class GazeSubscriber:

    def __init__(self, queue):
        port = "5570"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        print("Collecting head pose updates...")

        self.socket.connect("tcp://127.0.0.1:%s" % port)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')

        self.lastScrollTime = 0

        self.myColumns = ['TimeStamp', 'ScreenPartX', 'ScreenPartY', 'BallPosX', 'BallPosY',
                          'GazeAngleX', 'GazeAngleY', 'GazePointX', 'GazePointY',
                          'Gaze0X', 'Gaze0Y', 'Gaze0Z', 'Gaze1X', 'Gaze1Y', 'Gaze1Z',
                          'EyeBall0X', 'EyeBall0Y', 'EyeBall0Z',
                          'EyeBallCenter0X','EyeBallCenter0Y', 'EyeBallCenter0Z',
                          'EyeBall1X', 'EyeBall1Y', 'EyeBall1Z',
                          'EyeBallCenter1X', 'EyeBallCenter1Y', 'EyeBallCenter1Z',
                          'Pupil0X', 'Pupil0Y', 'Pupil0Z',
                          'Pupil1X', 'Pupil1Y', 'Pupil1Z',
                          'HeadPosX', 'HeadPosY', 'HeadPosZ',
                          'HeadAngleX', 'HeadAngleY', 'HeadAngleZ']
        self.df = pd.DataFrame(columns=self.myColumns)
        self.entry = dict(zip(self.myColumns, [np.nan] * 33))
        self.dataPath = '.\\calibrateData\\'
        self.dataName = 'OpenFace' + strftime("%Y-%m-%d-%H-%M", gmtime()) + '.csv'
        self.running = True

        self.started = False

        self.thread1 = threading.Thread(target=self.threadSubscribe)
        self.queue = queue
        self.thread1.start()

        self.thread2 = threading.Thread(target=self.threadPos)
        self.thread2.start()

    def stop(self):
        self.running = False
        print(self.dataName)
        print('Rows: ' + str(self.df.shape[0]))
        if self.df.shape[0] > 1:
            self.df.to_csv(self.dataPath + self.dataName)

    def threadSubscribe(self):
        while self.running:
            if self.started:
                msg = self.socket.recv_multipart()
                data = json.loads(msg[0])
                timestamp = data['timestamp']
                headPose = data['pose']
                HeadPosX = headPose['pose_Tx']
                HeadPosY = headPose['pose_Ty']
                HeadPosZ = headPose['pose_Tz']
                HeadPosRx = headPose['pose_Rx'] * 180 / 3.1415926
                HeadPosRy = headPose['pose_Ry'] * 180 / 3.1415926
                HeadPosRz = headPose['pose_Rz'] * 180 / 3.1415926
                gaze = data['gaze']
                gaze_angle_x = gaze['gaze_angle_x'] * 180 / 3.1415926
                gaze_angle_y = gaze['gaze_angle_y'] * 180 / 3.1415926
                gaze_point_x = gaze['gaze_screen_x']
                gaze_point_y = gaze['gaze_screen_y']
                gaze_0_x = gaze['gaze_0_x']
                gaze_0_y = gaze['gaze_0_y']
                gaze_0_z = gaze['gaze_0_z']
                gaze_1_x = gaze['gaze_1_x']
                gaze_1_y = gaze['gaze_1_y']
                gaze_1_z = gaze['gaze_1_z']
                eye_ball_0_x = gaze['eye_ball_0_x']
                eye_ball_0_y = gaze['eye_ball_0_y']
                eye_ball_0_z = gaze['eye_ball_0_z']
                eye_ball_center_0_x = gaze['eye_ball_center_0_x']
                eye_ball_center_0_y = gaze['eye_ball_center_0_y']
                eye_ball_center_0_z = gaze['eye_ball_center_0_z']
                eye_ball_1_x = gaze['eye_ball_1_x']
                eye_ball_1_y = gaze['eye_ball_1_y']
                eye_ball_1_z = gaze['eye_ball_1_z']
                eye_ball_center_1_x = gaze['eye_ball_center_1_x']
                eye_ball_center_1_y = gaze['eye_ball_center_1_y']
                eye_ball_center_1_z = gaze['eye_ball_center_1_z']
                pupil_0_x = gaze['pupil_0_x']
                pupil_0_y = gaze['pupil_0_y']
                pupil_0_z = gaze['pupil_0_z']
                pupil_1_x = gaze['pupil_1_x']
                pupil_1_y = gaze['pupil_1_y']
                pupil_1_z = gaze['pupil_1_z']

                print("GazeThread " + "timestamp: " + str(timestamp) + " gaze_angle_y: " + str(gaze_angle_y))
                print("BallPos: " + str(self.ballPos))
                self.entry['TimeStamp'] = time.time()  # (datetime.now(timezone.utc) + timedelta(days=3)).timestamp()
                screenWidth = 1536
                screenHeight = 864
                self.entry['BallPosX'] = self.ballPos[0]
                part_x = math.ceil(self.ballPos[0] / (screenWidth / 8))
                self.entry['BallPosY'] = self.ballPos[1]
                part_y = math.ceil(self.ballPos[1] / (screenHeight / 5))
                self.entry['ScreenPartX'] = part_x
                self.entry['ScreenPartY'] = part_y
                self.entry['GazeAngleX'] = gaze_angle_x
                self.entry['GazeAngleY'] = gaze_angle_y
                self.entry['GazePointX'] = gaze_point_x
                self.entry['GazePointY'] = gaze_point_y
                self.entry['Gaze0X'] = gaze_0_x
                self.entry['Gaze0Y'] = gaze_0_y
                self.entry['Gaze0Z'] = gaze_0_z
                self.entry['Gaze1X'] = gaze_1_x
                self.entry['Gaze1Y'] = gaze_1_y
                self.entry['Gaze1Z'] = gaze_1_z
                self.entry['HeadPosX'] = HeadPosX
                self.entry['HeadPosY'] = HeadPosY
                self.entry['HeadPosZ'] = HeadPosZ
                self.entry['HeadAngleX'] = HeadPosRx
                self.entry['HeadAngleY'] = HeadPosRy
                self.entry['HeadAngleZ'] = HeadPosRz
                self.entry['EyeBall0X'] = eye_ball_0_x
                self.entry['EyeBall0Y'] = eye_ball_0_y
                self.entry['EyeBall0Z'] = eye_ball_0_z
                self.entry['EyeBallCenter0X'] = eye_ball_center_0_x
                self.entry['EyeBallCenter0Y'] = eye_ball_center_0_y
                self.entry['EyeBallCenter0Z'] = eye_ball_center_0_z
                self.entry['EyeBall1X'] = eye_ball_1_x
                self.entry['EyeBall1Y'] = eye_ball_1_y
                self.entry['EyeBall1Z'] = eye_ball_1_z
                self.entry['EyeBallCenter1X'] = eye_ball_center_1_x
                self.entry['EyeBallCenter1Y'] = eye_ball_center_1_y
                self.entry['EyeBallCenter1Z'] = eye_ball_center_1_z
                self.entry['Pupil0X'] = pupil_0_x
                self.entry['Pupil0Y'] = pupil_0_y
                self.entry['Pupil0Z'] = pupil_0_z
                self.entry['Pupil1X'] = pupil_1_x
                self.entry['Pupil1Y'] = pupil_1_y
                self.entry['Pupil1Z'] = pupil_1_z
                # print(self.entry)
                self.df = self.df.append(self.entry, ignore_index=True)
                # print(self.df)

    def threadPos(self):
        while self.running:
            if self.queue.qsize() > 0:
                try:
                    self.ballPos = self.queue.get(0)
                    print(self.started)
                    if self.started == False:
                        self.started = True
                except queue.Empty:
                    pass
            time.sleep(0.001)


def calibrate():
    # Create Canvas
    tk = Tk()
    tk.title("Calibrate")
    tk.resizable(0, 0)
    tk.wm_attributes("-topmost", 1, "-fullscreen", 1)
    # bd=0,highlightthickness=0 No border around canvas
    canvas = Canvas(tk, width=1920, height=1080, bd=0, highlightthickness=0)
    canvas.pack()
    tk.update()
    # Create ball
    ball = Ball(canvas, 'red')
    class_regression = True
    if class_regression:
        # Keep update
        i = 0
        while i < 1000:
            ball.draw()
            if i % 100 == 0:
                # ball.draw()
                # 快速刷新屏幕
                tk.update_idletasks()
                tk.update()

            time.sleep(0.01)
            i = i + 1
    else:
        i = 0
        while i < 4:
            ball.draw_class()
            tk.update_idletasks()
            tk.update()
            time.sleep(1)
            i = i + 1
    ball.gazeSubscriber.stop()
    tk.destroy()

    # eng = matlab.engine.start_matlab()
    # eng.CalibrateModelGPR(nargout=0)

if __name__ == '__main__':
    calibrate()
