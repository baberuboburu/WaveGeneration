import pandas as pd


# ファイル
origin = 'kimoto_lighter'
file = f'../data/csv/{origin}.csv'
column = '9-13'   # 削除したいカラム名


def rm_column(file: str, column: str):
  df = pd.read_csv(file)
  df = df.drop(columns=[column])
  df.to_csv(file, index=False)
  return


rm_column(file, column)