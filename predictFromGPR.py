import matlab.engine
import time


class GPR(object):
    def __init__(self):
        future = matlab.engine.start_matlab(async=True)
        self.eng = future.result()
        # self.eng = matlab.engine.start_matlab()

    def predictGPR(self, data):
        x = self.eng.predictFromGPR_X(data)
        y = self.eng.predictFromGPR_Y(data)
        return [x, y]

    def quit(self):
        self.eng.quit()


def main():
    gpr = GPR()
    i = 0
    while i < 100:
        gpr.predictGPR()
        time.sleep(0.01)
        print('Count: ' + str(i))
        i = i + 1
    gpr.quit()


if __name__ == '__main__':
    main()
