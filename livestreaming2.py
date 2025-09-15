import cv2
import datetime
import sys
import os

PATH = r"/home/nishima/raid/video"

FPS = 15
WIDTH, HEIGHT = 640, 480

# ffmpegにパイプする場合は、FOURCCは不要です
# FOURCC = cv2.VideoWriter_fourcc(*'mp4v')

def main():
    cap = cv2.VideoCapture(0)
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    if not cap.isOpened():
        print("カメラを開けませんでした。")
        return

    try:
        while True:
            # カメラからフレームを読み込む
            ret, frame = cap.read()
            if not ret:
                print("フレームを読み込めません。")
                break

            now = datetime.datetime.now()

            img = cv2.resize(frame, (WIDTH, HEIGHT))

            strnow = now.strftime('%Y/%m/%d %H:%M:%S')
            point = (30, img.shape[0]-30)
            cv2.putText(img, strnow, point, cv2.FONT_HERSHEY_DUPLEX, 1, (255,255,255), 2)
            
            # 生のRGB24形式の画像データを標準出力に書き出す
            # ここがffmpegへのパイプ処理の中核です
            sys.stdout.buffer.write(img.tobytes())

    except Exception as e:
        print(e, file=sys.stderr)
    
    finally:
        # 終了時にリソースを解放
        cap.release()

if __name__ == "__main__":
    main()