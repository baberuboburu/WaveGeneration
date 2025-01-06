import pandas as pd
import os


# 特定のディレクトリを指定
origin = 'kimoto'
data_dir = f'../data/raw/{origin}'
output_dir = f'../data/raw/{origin}_lighter'
chunksize = 100   # ファイルを何分の1にするか


# すべてのcsvファイルのoutputカラムを取得し、データフレームに追加
rows_to_save = []


def process_csv(file_path, file):
  for chunk in pd.read_csv(file_path, chunksize=chunksize):
    # 各チャンクの最初の行を取得して保存
    rows_to_save.append(chunk.iloc[0])

  # 処理結果を新しいファイルに保存
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  output_file = os.path.join(output_dir, file)
  output_df = pd.DataFrame(rows_to_save)
  output_df.to_csv(output_file, index=False)


# ディレクトリの再帰的な探索
for root, dirs, files in os.walk(data_dir):
  for file in files:
    if file.endswith('.csv'):
      file_path = os.path.join(root, file)
      process_csv(file_path, file)