from functions.BASE import BASE
import numpy as np
import pandas as pd


class Sin4x(BASE):
  def __init__(self, data_path: str, origin: str, Freq: float, Prop: float):
    time = pd.read_csv(data_path)
    Time = time.loc[:,'time'].values
    X = pd.read_csv(data_path).drop(columns=['time'])
    target_wave_name = 'sin4x'
    Target_wave = self.sin4x(Time, Freq)
    super().__init__(Time, X, origin, target_wave_name, Target_wave, Freq, Prop)
  

  def sin4x(self, Time, Freq: float):
    return np.sin( 4 * 2 * np.pi * Freq * Time )
  

  def ridge(self):
    for alpha in [0, 0.001, 0.01, 0.1, 1, 10]:
        heatmap_data, X_train_predict, X_test_predict, R2_test = super().learn(alpha)
        super().heatmap(heatmap_data, alpha)
        super().plot(alpha, R2_test, X_train_predict, X_test_predict)