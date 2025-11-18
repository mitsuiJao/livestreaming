## 概要
パソコンに刺したカメラのストリーミングを可能にします。防犯カメラみたいなもんです。
防犯カメラといえば保存もできます。
定期的に削除しないとパンパンになるから気を付けて！cronとか使えば定期的に消せると思います

カメラの処理にはffmpegを、pythonは文字入れに使ってます。
ストリーミングはHLS使ってます。

## 使い方
ffmpegをインストールした後requirements.txtでモジュールを入れます
カレントで次のコマンドを実行します。ユーザ名とディレクトリは置き換えて!
もし保存は別にいいなら最後の-strftime以降消せばいいと思います
```
/bin/sh -c '.venv/bin/python3 livestreaming2.py | /usr/bin/ffmpeg -f rawvideo -pixel_format bgr24 -s 640x480 -r 15 -i - -c:v libx264 -profile:v baseline -pix_fmt yuv420p -preset veryfast -c:a aac -movflags +faststart -hls_time 2 -hls_list_size 10 -hls_flags delete_segments -start_number 1 www/live.m3u8 -f segment -segment_time 3600 -reset_timestamps 1 -strftime 1 "/home/{username}/{videodirectory}%%Y-%%m-%%d_%%H-%%M-%%S.mp4"'
```

まあ後はsystemdとかに追加しときます。その時は`WorkingDirectory`の設定を忘れずに！
あと`Restart`, `RestartSec`とかも設定するべきかも？

家の外とかから見るにはとかでプロキシ立てたほうがいいよ。セキュリティ的にね
