from functions.cosx import Cosx
from functions.cos2x import Cos2x
from functions.cos3x import Cos3x
from functions.cos4x import Cos4x
from functions.cos5x import Cos5x
from functions.sinx import Sinx
from functions.sin2x import Sin2x
from functions.sin3x import Sin3x
from functions.sin4x import Sin4x
from functions.sin5x import Sin5x
from functions.square import Square
from functions.square2 import Square2
from functions.sawtooth import Sawtooth
from functions.triangle import Triangle
from functions.halfwave import Halfwave


# 必要な情報の入力
origin = '20241222'
data_path = f'./data/csv/{origin}.csv'
Freq = 1
Prop = 0.8


# 実行
Waves = [
  Cosx(data_path, origin, Freq, Prop), 
  Cos2x(data_path, origin, Freq, Prop),
  Cos3x(data_path, origin, Freq, Prop),
  Cos4x(data_path, origin, Freq, Prop),
  Cos5x(data_path, origin, Freq, Prop),
  Sinx(data_path, origin, Freq, Prop), 
  Sin2x(data_path, origin, Freq, Prop),
  Sin3x(data_path, origin, Freq, Prop),
  Sin4x(data_path, origin, Freq, Prop),
  Sin5x(data_path, origin, Freq, Prop),
  Square(data_path, origin, Freq, Prop), 
  Square2(data_path, origin, Freq, Prop),
  Sawtooth(data_path, origin, Freq, Prop),
  Triangle(data_path, origin, Freq, Prop),
  Halfwave(data_path, origin, Freq, Prop)
]

for Wave in Waves:
  print(f'-------------------- { Wave.__class__.__name__} --------------------')
  Wave.ridge()