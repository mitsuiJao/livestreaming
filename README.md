# livestreaming

シンプルなローカル監視向けライブ配信ツールです。  
Python でカメラ映像に日時を重ね、`ffmpeg` で HLS (`www/live.m3u8`) を生成します。

## 含まれるファイル

- `livestreaming2.py`  
  USBカメラ (`cv2.VideoCapture(0)`) から映像を取得し、日時を描画して標準出力へ生フレームを書き出します。
- `livestreaming.py`  
  RTSP入力を使う別実装（保存処理あり）。
- `www/index.html`  
  `hls.js` で `live.m3u8` を再生する最小ビューアです。

## 必要なもの

- Python 3
- ffmpeg
- `requirements.txt` の Python パッケージ

## セットアップ

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## 使い方（USBカメラ入力）

以下のコマンド内の `{username}` と `{videodirectory}` は実環境に合わせて置き換えてください。

```bash
/bin/sh -c '.venv/bin/python3 livestreaming2.py | /usr/bin/ffmpeg -f rawvideo -pixel_format bgr24 -s 640x480 -r 15 -i - -c:v libx264 -profile:v baseline -pix_fmt yuv420p -preset veryfast -hls_time 2 -hls_list_size 10 -hls_flags delete_segments -start_number 1 www/live.m3u8 -f segment -segment_time 3600 -reset_timestamps 1 -strftime 1 "/home/{username}/{videodirectory}%%Y-%%m-%%d_%%H-%%M-%%S.mp4"'
```

- 保存が不要なら、コマンド後半の `-f segment` 以降（mp4保存部分）を外してください。
- `www/index.html` を配信してブラウザで開くと視聴できます。

## 運用メモ

- 長期運用時は保存先の容量監視・古い動画の定期削除を推奨します。
- 例: `crontab` で古い mp4 を定期削除する（`find /path/to/videos -name "*.mp4" -mtime +7 -delete` など）。
- 常駐化するなら systemd などで `WorkingDirectory` と `Restart` 系設定を入れてください。
- 外部公開する場合は、リバースプロキシや認証を必ず入れてください。
