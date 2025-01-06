from functions.BASE import BASE
import numpy as np
import pandas as pd


class Halfwave(BASE):
  def __init__(self, data_path: str, origin: str, Freq: float, Prop: float):
    time = pd.read_csv(data_path)
    Time = time.loc[:,'time'].values
    X = pd.read_csv(data_path).drop(columns=['time'])
    target_wave_name = 'halfwave'
    Target_wave = self.halfwave(Time, Freq)
    super().__init__(Time, X, origin, target_wave_name, Target_wave, Freq, Prop)
  

  def halfwave(self, Time, Freq: float):
    # Define the number of samples and the period
    num_samples = len(Time)
    theta = np.linspace(0, 100 * 2 * np.pi, num_samples)

    # Initialize the wave array
    halfwave = np.zeros(num_samples)

    # Define the wave based on the given conditions
    for k in range(int(100)):  # Loop over each cycle
      start = k * 2 * np.pi
      end = (k + 1) * 2 * np.pi
      halfwave[(theta >= start) & (theta < start + np.pi)] = np.sin(theta[(theta >= start) & (theta < start + np.pi)])
      halfwave[(theta >= start + np.pi) & (theta < end)] = 0

    return halfwave
  

  def ridge(self):
    for alpha in [0, 0.001, 0.01, 0.1, 1, 10]:
        heatmap_data, X_train_predict, X_test_predict, R2_test = super().learn(alpha)
        super().heatmap(heatmap_data, alpha)
        super().plot(alpha, R2_test, X_train_predict, X_test_predict)