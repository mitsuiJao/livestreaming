import cv2
import av
import datetime
import sys
import time

container = av.open('rtsp://192.168.0.210:8554/unicast')

for frame in container.decode(video=0):
    start_time = time.time()
    
    img = frame.to_ndarray(format='bgr24')
    w, h = img.shape[:2]
    now = datetime.datetime.now()
    strnow = now.strftime('%Y/%m/%d %H:%M:%S')
    point = (30, h-200-1)
    cv2.putText(img, strnow, point, cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255))
    sys.stdout.buffer.write(img.tobytes())