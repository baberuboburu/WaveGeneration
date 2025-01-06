import pandas as pd
import os
import re


# 特定のディレクトリを指定
origin = '20241222'
directory = f'../data/raw/{origin}'
output_column_name = 'output'  # 取得したいカラム名
output_file = f'../data/csv/{origin}.csv'  # 保存するファイル名


# すべてのcsvファイルのoutputカラムを取得し、データフレームに追加
data_frames = []
file_paths = []

for i, filename in enumerate(os.listdir(directory)):
    if filename.endswith('.csv'):
        file_path = os.path.join(directory, filename)
        file_paths.append(file_path)

file_paths.sort()
print(file_paths)


# Timeを1列目に追加する
df_time = pd.read_csv(file_paths[0])
time = df_time['time']
data_frames.append(time)


# outputを2列目以降に追加する
for i, file_path in enumerate(file_paths):
    df = pd.read_csv(file_path)
    if output_column_name in df.columns:
        match = re.search(r'/(\d+-\d+)', file_path)
        if match:
            new_column = match.group(1)
        new_column_name = new_column  # 新しいカラム名
        data_frames.append(df[output_column_name].rename(new_column_name))

# すべてのカラムを横に結合
combined_df = pd.concat(data_frames, axis=1)

# 新しいcsvファイルとして保存
combined_df.to_csv(output_file, index=False)