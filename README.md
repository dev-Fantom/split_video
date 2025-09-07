# Split video
動画ファイルを指定した時間ごとに分割して出力する。

初期設定：duration=600（10分）

## 機能
- 指定した秒数で動画を自動分割
- フレームレート変更機能（オプション）
- 短いセグメント（60秒未満）の自動結合機能

## 環境
* Python 3.10.0

## 使い方
Install Library form requirements.txt.

requirements.txtからライブラリをインストール

```shell
pip install -r requirements.txt
```

### 引数の説明

1. 動画ファイルが入っているディレクトリ（必須）
2. 分割する秒数（オプション、未指定の場合は600で処理）
3. フレームレート（オプション、未指定の場合は元動画のフレームレートを維持）

### 使用例

基本的な使用方法（10分間隔で分割）：
```bash
python main.py /path/to/video/directory
```

カスタム間隔で分割（5分間隔）：
```bash
python main.py /path/to/video/directory 300
```

フレームレートを指定して分割（7fpsで出力）：
```bash
python main.py /path/to/video/directory 600 7
```

## 出力結果

### 出力ディレクトリ
- フレームレートを指定した場合: `{元ファイル名}_{fps}fps_split/`
- フレームレートを指定しない場合: `{元ファイル名}_split/`

### 分割ファイル名
- 形式: `{元ファイル名}_{開始秒数}_{終了秒数}.mp4`
- 例: `sample_0_600.mp4`, `sample_600_1200.mp4`

### スマートセグメント処理
最後のセグメントが60秒未満になる場合、自動的に直前のセグメントと結合されます。
これにより、非常に短い動画ファイルの生成を防ぎます。

## Author / 作成者

- [Fantom, Inc. (JP)](https://twitter.com/Fantomcojp)
