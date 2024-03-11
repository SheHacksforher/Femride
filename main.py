from vidstream import CameraClient
from vidstream import StreamingServer


import threading
import time

receiving=StreamingServer('192.168.219.219',9999)
sending=CameraClient('10.20.200.155',9999)


t1=threading.Thread(target=receiving.start_server)

t1.start()

time.sleep(2)


t2=threading.Thread(target=sending.start_stream)

t2.start()

while input("")!="STOP":
    continue

receiving.stop_server()
sending.stop_stream()