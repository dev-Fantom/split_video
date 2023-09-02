import os
import glob
import sys

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


def split_video(file_path, duration=600):
    # ファイル名から拡張子を取得
    file_name_path, file_extension = os.path.splitext(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # 分割したビデオの保存先ディレクトリを作成
    output_dir = file_name_path + "_split"
    os.makedirs(output_dir, exist_ok=True)

    # 動画の長さを取得
    video = VideoFileClip(file_path)
    total_duration = video.duration

    # 指定した間隔でビデオを分割
    start_time = 0
    end_time = duration

    while start_time < total_duration:
        # 分割範囲を指定してビデオを切り出し
        output_path = os.path.join(output_dir, f"{file_name}_{start_time}_{end_time}{file_extension}")
        ffmpeg_extract_subclip(file_path, start_time, end_time, targetname=output_path)

        # 次の分割範囲を更新
        start_time += duration
        end_time += duration


def split_videos_in_directory(directory, duration=600):
    # ディレクトリ内のすべてのMP4ファイルを取得
    video_files = glob.glob(os.path.join(directory, "*.mp4"))
    for video_file in video_files:
        # print(f"{video_file=}")
        split_video(video_file, duration)


# メイン処理
if __name__ == "__main__":
    directory_path = sys.argv[1]
    split_videos_in_directory(directory_path, duration=600)
