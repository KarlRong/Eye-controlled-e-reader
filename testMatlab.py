import matlab.engine


def main():
    eng = matlab.engine.start_matlab()
    output = eng.CalibrateModelGPR()
    print(output)
    eng.quit()


if __name__ == '__main__':
    main()
