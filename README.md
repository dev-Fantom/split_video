# Split video
動画ファイルを指定した時間ごとに変換して出力する。

初期設定：duration=600（10分）

## 環境
* Python 3.10.0

## 使い方
Install Library form requirements.txt.

requirements.txtからライブラリをインストール

```shell
pip install -r requirements.txt
```

### 引数の説明

1. 動画ファイルが入っているディレクトリ 
2. 分割する秒数（未指定の場合は600で処理）

```
python main.py /DIRNAME 600
```

## 出力結果
ログ
```
Moviepy - Running:
>>> "+ " ".join(cmd)
Moviepy - Command successful
```

## Author / 作成者

- [Fantom, Inc. (JP)](https://twitter.com/Fantomcojp)
