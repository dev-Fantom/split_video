import os
import glob
import sys

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def split_video(file_path: str, duration: int) -> None:
    # ファイル名から拡張子を取得
    file_name, file_extension = os.path.splitext(os.path.basename(file_path))

    # 分割したビデオの保存先ディレクトリを作成
    output_dir = f"{file_name}_split"
    os.makedirs(output_dir, exist_ok=True)

    # 動画の長さを取得し、動画ファイルを適切に閉じる
    with VideoFileClip(file_path) as video:
        total_duration = int(video.duration)

    # 指定した間隔でビデオを分割
    start_time = 0
    end_time = duration

    while start_time < total_duration:
        # 実際の終了時間が動画の総時間を超えないように調整
        end_time = min(end_time, total_duration)

        # 分割範囲を指定してビデオを切り出し
        output_path = os.path.join(output_dir, f"{file_name}_{start_time}_{end_time}{file_extension}")
        ffmpeg_extract_subclip(file_path, start_time, end_time, targetname=output_path)

        # 次の分割範囲を更新
        start_time += duration
        end_time = start_time + duration


def split_videos_in_directory(directory: str, duration: int) -> None:
    # ディレクトリ内のすべてのMP4ファイルを取得
    video_files = glob.glob(os.path.join(directory, "*.mp4"))
    for video_file in video_files:
        # 動画ファイル毎に分割処理
        split_video(video_file, duration)


# メイン処理
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ディレクトリパスを引数として指定してください。")
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

    split_videos_in_directory(directory_path, duration)
