import cv2
import numpy as np
import multiprocessing as mp
import time
import os


def produce(q, name, pwd, ip, channel=1):
    #增加nvr取流的协议,也是基于rtsp协议而来
    #f"rtsp://{camera_name}:{camera_pwd}@{nvr_ip}:554/cam/realmonitor?channel={channel}&subtype=0"
    cap = cv2.VideoCapture("rtsp://%s:%s@%s//Streaming/Channels/%d" % (name, pwd, ip, channel))
    while True:

        is_opened, frame = cap.read()
        detection_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if is_opened:
            q.put((frame,detection_time))
        else:
            q.put((None,None))
        # 保证实时显示最新的图片
        #time.sleep(1)
        q.get() if q.qsize() > 1 else None
        #print("produce qsize:",q.qsize())
    # cap.release()


def customer(q, window_name):
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        #print("customer qsize:",q.qsize())
        (frame,detection_time) = q.get()
        #time.sleep(2)
        if isinstance(frame,np.ndarray):
            cv2.putText(frame,str(detection_time),(300,300),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
            cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


def run():  # single camera
    user_name, user_pwd, camera_ip = "admin", "!QAZ2wsx3edc", "192.168.1.100"
    #mp.set_start_method(method="spawn")
    # 由于opencv不能直接设置fps,使用time.sleep会出现掉帧的现象
    # 目前设置队列size小一点，去处理最新的几张图片中的一张。
    # eg: fps=25, queue.qsize=2 ,至少能保证1秒有机会处理2张图片。
    queue = mp.Queue()
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

    queues = [mp.Queue(maxsize=2) for _ in camera_ip_list]

    processes = []
    for queue, camera_ip in zip(queues, camera_ip_list):
        processes.append(mp.Process(target=produce, args=(queue, user_name, user_pwd, camera_ip)))
        processes.append(mp.Process(target=customer, args=(queue, camera_ip)))

    [process.start() for process in processes]
    [process.join() for process in processes]


if __name__ == '__main__':
    run()
