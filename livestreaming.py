import cv2
import av
import datetime
import sys
import time
import os

PATH = r"/home/nishima/raid/vieo"

FPS = 30
WIDTH, HEIGHT = 640, 480
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')
def create_writer():
    now = datetime.datetime.now()
    filename = f"{now.strftime('%Y-%m-%d')}.mp4"
    filename = os.path.join(PATH, filename)
    return cv2.VideoWriter(filename, FOURCC, FPS, (WIDTH, HEIGHT)), now.date()


writer, current_date = create_writer()

try:
    container = av.open('rtsp://192.168.0.210:8554/unicast')

    for frame in container.decode(video=0):
        now =   datetime.datetime.now()
        if now.date() != current_date:
            writer.release()
            writer, current_date = create_writer()
        
        img = frame.to_ndarray(format='bgr24')
        w, h = img.shape[:2]
        strnow = now.strftime('%Y/%m/%d %H:%M:%S')
        point = (30, h-200-1)
        cv2.putText(img, strnow, point, cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255))
        sys.stdout.buffer.write(img.tobytes())
        
        if writer.isOpened():
            writer.write(img)

except Exception as e:
    print(e)
    time.sleep(10)
    
finally:
    if writer.isOpened():
        writer.release()