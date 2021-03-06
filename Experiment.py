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
from calibrate import Calibrate


class Ball:
    def __init__(self, canvas, color, eng):
        self.eng = eng
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
        self.gazeSubscriber = GazeSubscriber(self.queue, self.eng)

        self.count_calibrate = 1

    def draw_experiment(self, index):
        self.canvas.delete(self.id)
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=self.color)
        x_ball = [200, 1336, 768, 1336, 200]
        y_ball = [200, 200, 432, 664, 664]
        self.canvas.move(self.id, x_ball[index], y_ball[index])
        print('Experiment: ' + str(x_ball[index]) + ' ' + str(y_ball[index]))

        self.posBall = [x_ball[index], y_ball[index]]
        msg = self.posBall
        self.queue.put(msg)

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

    def __init__(self, queue, eng):
        self.eng = eng
        port = "5570"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        print("Collecting head pose updates...")

        self.socket.connect("tcp://127.0.0.1:%s" % port)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, u'')

        self.lastScrollTime = 0

        self.myColumns = ['TimeStamp', 'BallPosX', 'BallPosY', 'GazePointX', 'GazePointY']
        self.df = pd.DataFrame(columns=self.myColumns)
        self.entry = dict(zip(self.myColumns, [np.nan] * 4))
        self.dataPath = '.\\experimentData\\'
        self.dataName = 'Experiment' + strftime("%Y-%m-%d-%H-%M", gmtime()) + '.csv'
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
                gaze = data['gaze']
                gaze_angle_x = gaze['gaze_angle_x'] * 180 / 3.1415926
                gaze_angle_y = gaze['gaze_angle_y'] * 180 / 3.1415926
                gaze_point_x = gaze['gaze_screen_x']
                gaze_point_y = gaze['gaze_screen_y']

                # gazeCoordinates = self.eng.ProcessTForm(gaze_point_x, gaze_point_y, nargout=2)
                # print(gazeCoordinates)

                print("BallPos: " + str(self.ballPos))
                self.entry['TimeStamp'] = time.time()  # (datetime.now(timezone.utc) + timedelta(days=3)).timestamp()
                self.entry['BallPosX'] = self.ballPos[0]
                self.entry['BallPosY'] = self.ballPos[1]
                self.entry['GazePointX'] = gaze_point_x
                self.entry['GazePointY'] = gaze_point_y
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

class Experiment:
    def experiment(eng):
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
        ball = Ball(canvas, 'red', eng)

        i = 0
        count = 1000
        while i < count:
            ball.draw_experiment(math.floor(i / 200))
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
            i = i + 1

        ball.gazeSubscriber.stop()
        tk.destroy()

        mean_error = eng.ExperimentData()
        print('Mean Error: ' + str(mean_error) + 'px')


if __name__ == '__main__':
    print("Start MatLab Engine:\n ")
    eng = matlab.engine.start_matlab()
    print("Start Calibrate:\n ")
    Calibrate.calibrate(eng)
    print("Start experiment:\n")
    Experiment.experiment(eng)
