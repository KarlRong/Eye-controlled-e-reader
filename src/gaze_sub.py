import time
import json


def main():
    import zmq
    port = "5570"

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting head pose updates...")

    socket.connect("tcp://127.0.0.1:%s" % port)
    socket.setsockopt_string(zmq.SUBSCRIBE, u'')

    while True:
        msg = socket.recv_multipart()
        topic = msg[0]
        data = json.loads(msg[1])
        timestamp = data['timestamp']
        frame = data['frame']
        confidence = data['confidence']
        headPose = data['pose']
        gaze = data['gaze']
        print(timestamp)
        time.sleep(0.01)


if __name__ == '__main__':
    main()
