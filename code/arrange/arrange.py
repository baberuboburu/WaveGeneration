import pandas as pd
import os


data_dir = '../data/raw/20241222'


def process_csv(file_path):
  # CSVファイルを読み込み、上から11行をスキップしてカラム名を設定
  # df = pd.read_csv(file_path, skiprows=11, names=['time', 'input', 'input2', 'trigger', 'output'])
  df = pd.read_csv(file_path, skiprows=1, names=['time', 'input', 'output', 'trigger'])
  # 処理結果を新しいファイルに保存
  df.to_csv(file_path, index=False)

# ディレクトリの再帰的な探索
for root, dirs, files in os.walk(data_dir):
  for file in files:
    if file.endswith('.csv'):
      file_path = os.path.join(root, file)
      print(file_path)
      process_csv(file_path)

print("全てのCSVファイルの処理が完了しました。")