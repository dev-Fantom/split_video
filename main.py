import os
import glob
import sys

from moviepy.video.io.VideoFileClip import VideoFileClip


def split_video(file_path: str, duration: int, fps: int = None) -> None:
    # ファイル名から拡張子を取得
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    # 分割したビデオの保存先ディレクトリを作成
    if fps:
        output_dir = f"{file_name}_{fps}fps_split"
    else:
        output_dir = f"{file_name}_split"
    os.makedirs(output_dir, exist_ok=True)

    # 動画の長さを取得し、動画ファイルを適切に閉じる
    with VideoFileClip(file_path) as video:
        total_duration = int(video.duration)

    # 最後の動画が1分未満の場合の処理を考慮して分割範囲を計算
    full_segments = total_duration // duration
    remainder = total_duration % duration
    
    segments = []
    
    if remainder < 60 and full_segments > 0:
        # 最後のセグメントが60秒未満の場合、直前のセグメントと結合
        for i in range(full_segments - 1):
            start_time = i * duration
            end_time = start_time + duration
            segments.append((start_time, end_time))
        
        # 最後のセグメントは残り時間を含む
        last_start = (full_segments - 1) * duration
        last_end = total_duration
        segments.append((last_start, last_end))
    else:
        # 通常の分割処理
        start_time = 0
        while start_time < total_duration:
            end_time = min(start_time + duration, total_duration)
            segments.append((start_time, end_time))
            start_time += duration

    # 各セグメントを処理
    for start_time, end_time in segments:
        # 分割範囲を指定してビデオを切り出し
        output_path = os.path.join(output_dir, f"{file_name}_{start_time}_{end_time}{file_extension}")
        
        # VideoFileClipを使用してフレームレート制御付きで分割
        with VideoFileClip(file_path) as video:
            subclip = video.subclip(start_time, end_time)
            if fps:
                subclip = subclip.set_fps(fps)
            subclip.write_videofile(output_path, verbose=False, logger=None)


def split_videos_in_directory(directory: str, duration: int, fps: int = None) -> None:
    # ディレクトリ内のすべてのMP4ファイルを取得
    video_files = glob.glob(os.path.join(directory, "*.mp4"))
    for video_file in video_files:
        # 動画ファイル毎に分割処理
        split_video(video_file, duration, fps)


# メイン処理
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使用方法: python main.py <ディレクトリパス> [duration] [fps]")
        print("ディレクトリパス: 処理する動画ファイルがあるディレクトリ")
        print("duration: 分割する秒数 (デフォルト: 600)")
        print("fps: フレームレート (オプション)")
        sys.exit(1)

    directory_path = sys.argv[1]
    if not os.path.isdir(directory_path):
        print("指定されたパスはディレクトリではありません。")
        sys.exit(1)

    # コマンドライン引数からdurationを取得し、指定がない場合は600秒をデフォルト値とする
    try:
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 600
    except ValueError:
        print("Durationは整数である必要があります。")
        sys.exit(1)

    # コマンドライン引数からfpsを取得し、指定がない場合はNoneをデフォルト値とする
    fps = None
    if len(sys.argv) > 3:
        try:
            fps = int(sys.argv[3])
        except ValueError:
            print("FPSは整数である必要があります。")
            sys.exit(1)

    split_videos_in_directory(directory_path, duration, fps)
