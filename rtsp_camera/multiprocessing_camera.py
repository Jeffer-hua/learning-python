import cv2
import numpy as np
import multiprocessing as mp
import time
import os


def produce(q, name, pwd, ip, channel=1):
    cap = cv2.VideoCapture("rtsp://%s:%s@%s//Streaming/Channels/%d" % (name, pwd, ip, channel))
    while True:
        is_opened, frame = cap.read()
        q.put(frame) if is_opened else None
        q.get() if q.qsize() > 1 else None
    cap.release()


def customer(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        frame = q.get()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def run():  # single camera
    user_name, user_pwd, camera_ip = "admin", "!QAZ2wsx3edc", "192.168.1.164"
    mp.set_start_method(method="spawn")
    queue = mp.Queue(maxsize=2)
    processes = [mp.Process(target=produce, args=(queue, user_name, user_pwd, camera_ip)),
                 mp.Process(target=customer, args=(queue, camera_ip))]

    # 主进程退出才退出子进程
    [setattr(process, "daemon", True) for process in processes]
    [process.start() for process in processes]
    [process.join() for process in processes]


def run_multi_camera():
    user_name, user_pwd = "admin", "!QAZ2wsx3edc"
    camera_ip_list = [
        "192.168.1.168",
        "192.168.1.169",
        "192.168.1.170",
        "192.168.1.172"
    ]

    queues = [mp.Queue(maxsize=10) for _ in camera_ip_list]

    processes = []
    for queue, camera_ip in zip(queues, camera_ip_list):
        processes.append(mp.Process(target=produce, args=(queue, user_name, user_pwd, camera_ip)))
        processes.append(mp.Process(target=customer, args=(queue, camera_ip)))

    [process.start() for process in processes]
    [process.join() for process in processes]


if __name__ == '__main__':
    run()
