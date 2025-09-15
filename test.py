import cv2
import sys

WIDTH, HEIGHT = 640, 480
FPS = 15

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("エラー: カメラを開けませんでした。/dev/video0 を確認してください。", file=sys.stderr)
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)

    try:
        with open("raw_frames.bin", "wb") as f:
            for i in range(10): # 10フレームだけ取得
                ret, frame = cap.read()
                if not ret:
                    print("エラー: フレームを読み込めませんでした。", file=sys.stderr)
                    break
                
                img = cv2.resize(frame, (WIDTH, HEIGHT))
                f.write(img.tobytes())
        
        print("raw_frames.bin に10フレームを書き込みました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
    
    finally:
        cap.release()

if __name__ == "__main__":
    main()
