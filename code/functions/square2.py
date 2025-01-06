from functions.BASE import BASE
import numpy as np
import pandas as pd


class Square2(BASE):
  def __init__(self, data_path: str, origin: str, Freq: float, Prop: float):
    time = pd.read_csv(data_path)
    Time = time.loc[:,'time'].values
    X = pd.read_csv(data_path).drop(columns=['time'])
    target_wave_name = 'square2'
    Target_wave = self.square2(Time, Freq)
    super().__init__(Time, X, origin, target_wave_name, Target_wave, Freq, Prop)
  

  def square2(self, Time, Freq: float):
    # Define the number of samples and the period
    num_samples = len(Time)
    theta = np.linspace(0, 100 * 2 * np.pi, num_samples)

    # Initialize the wave array
    v_theta = np.zeros_like(theta)

    # Define the wave based on the given conditions
    for k in range(100):  # Loop over each cycle
      start = k * 2 * np.pi
      v_theta[(start <= theta) & (theta < start + 2 * np.pi / 3)] = 1
      v_theta[(start + 2 * np.pi / 3 <= theta) & (theta < start + np.pi)] = 0
      v_theta[(start + np.pi <= theta) & (theta < start + 5 * np.pi / 3)] = -1
      v_theta[(start + 5 * np.pi / 3 <= theta) & (theta < start + 2 * np.pi)] = 0

    return v_theta
  

  def ridge(self):
    for alpha in [0, 0.001, 0.01, 0.1, 1, 10]:
        heatmap_data, X_train_predict, X_test_predict, R2_test = super().learn(alpha)
        super().heatmap(heatmap_data, alpha)
        super().plot(alpha, R2_test, X_train_predict, X_test_predict)