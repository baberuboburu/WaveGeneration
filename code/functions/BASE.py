import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class BASE():
  def __init__(self, Time, X, origin: str, target_wave_name: str, Target_wave, Freq: float, Prop: float):
    # 定数の初期化
    self.Freq = Freq
    self.origin = origin
    self.target_wave_name = target_wave_name
    self.Prop = Prop

    # 目標波形の設定
    self.Time = Time
    self.Target_wave = Target_wave
    self.X_train, self.X_test, self.Y_train, self.Y_test, self.T_train, self.T_test= train_test_split(X, Target_wave, self.Time, test_size=1-Prop, shuffle=False)


  def learn(self, alpha: float):
    # 学習
    model = Ridge(alpha=alpha)
    model.fit(self.X_train, self.Y_train)

    # 正答率などの計算
    print(f'alpha={alpha}')
    R2_train = model.score(self.X_train, self.Y_train)
    R2_test = model.score(self.X_test, self.Y_test)
    X_train_predict = model.predict(self.X_train)
    X_test_predict = model.predict(self.X_test)
    RMSE_train = np.sqrt(mean_squared_error(self.Y_train, X_train_predict))
    RMSE_test = np.sqrt(mean_squared_error(self.Y_test, X_test_predict))
    print('Accuracy(train):{}%'.format(100*R2_train))
    print('Accuracy(test):{}%'.format(100*R2_test))
    print('RMSE(train):', RMSE_train)
    print('RMSE(test):', RMSE_test)

    # heatmapの準備
    feature_weights = pd.DataFrame({
      'Feature': self.X_train.columns,
      'Weight': model.coef_
    })
    heatmap_data = feature_weights.set_index('Feature').T

    return heatmap_data, X_train_predict, X_test_predict, R2_test


  def heatmap(self, heatmap_data, alpha: float):
    # 重みのヒートマップを保存する
    plt.figure(figsize=(20, 4))
    sns.heatmap(
        heatmap_data,
        annot=True,
        cmap='coolwarm',
        cbar=True,
        linewidths=0.5
    )

    # 画像の保存
    heatmap_path = self.prepare_heatmap(alpha)
    plt.title('Feature Weights Heatmap')
    plt.savefig(heatmap_path)
    plt.close()


  def plot(self, alpha, R2_test, X_train_predict, X_test_predict):
    #目標波形の図示の設定
    _ ,ax = plt.subplots(2, 1, figsize=(6.4, 4.8), dpi=500, tight_layout=True)
    ax[0].plot(self.Time, self.Target_wave, label='target wave', color='red')
    ax[0].set_xlabel('Time / s', fontsize=8)
    ax[0].set_ylabel('Voltage / V', fontsize=8)
    ax[0].set_xticks(np.linspace(self.T_train[-1]-2/self.Freq, self.T_test[0]+2/self.Freq, 5))
    ax[0].set_xticks(np.linspace(self.T_train[-1]-2/self.Freq, self.T_test[0]+2/self.Freq, 9), minor=True)
    ax[0].set_yticks(np.linspace(-2, 2, 5))
    ax[0].set_yticks(np.linspace(-2, 2, 9), minor=True)
    ax[0].set_xlim(self.T_train[-1]-2/self.Freq, self.T_test[0]+2/self.Freq)
    ax[0].set_ylim(-2,2)
    ax[0].tick_params(labelsize=8)
    ax[0].legend(loc='upper right', fontsize=8)
    ax[0].grid(which='major', alpha=1)
    ax[0].grid(which="minor", alpha=0.75)

    #学習モデルの図の設定
    ax[1].plot(self.Time, self.Target_wave, label='target wave', color='red')
    ax[1].plot(self.T_train, X_train_predict, label='train model', color='blue')
    ax[1].plot(self.T_test, X_test_predict, label='test model', color='lime')
    ax[1].set_title(f'alpha={alpha}', loc='right', fontsize=8)
    ax[1].set_xlabel('Time / s', fontsize=8)
    ax[1].set_ylabel('Voltage / V', fontsize=8)
    ax[1].set_xticks(np.linspace(self.T_train[-1]-2/self.Freq, self.T_test[0]+2/self.Freq, 5))
    ax[1].set_xticks(np.linspace(self.T_train[-1]-2/self.Freq, self.T_test[0]+2/self.Freq, 9), minor=True)
    ax[1].set_yticks(np.linspace(-2, 2, 5))
    ax[1].set_yticks(np.linspace(-2, 2, 9), minor=True)
    ax[1].set_xlim(self.T_train[-1]-2/self.Freq, self.T_test[0]+2/self.Freq)
    ax[1].set_ylim(-2,2)
    ax[1].text((self.T_train[-1] + self.T_test[0])/2, -1.9, 'Accuracy(test):{:.4f}%'.format(100*R2_test), horizontalalignment='center', verticalalignment='bottom', fontsize=10)
    ax[1].tick_params(labelsize=8)
    ax[1].legend(loc='upper right', ncol=3, fontsize=8)
    ax[1].grid(which='major', alpha=1)
    ax[1].grid(which='minor', alpha=0.75)

    wave_path = self.prepare_wave(alpha)
    plt.savefig(wave_path)


  def prepare_heatmap(self, alpha: float):
    # heatmapに利用するディレクトリpathの準備
    heatmap_directory = f'./img/{self.origin}/heatmap/{self.target_wave_name}(Prop={self.Prop}'
    heatmap_filename = f'alpha={alpha}.png'
    heatmap_path = f'{heatmap_directory}/{heatmap_filename}'
    if not os.path.exists(heatmap_directory):
      os.makedirs(heatmap_directory)

    return heatmap_path

  
  def prepare_wave(self, alpha: float):
    # 波形生成タスクの結果の画像を保存するディレクトリのpathの準備
    wave_directory = f'./img/{self.origin}/WaveGeneration/{self.target_wave_name}(Prop={self.Prop})'
    wave_filename = f'alpha={alpha}.png'
    wave_path = f'{wave_directory}/{wave_filename}'
    if not os.path.exists(wave_directory):
      os.makedirs(wave_directory)
    
    return wave_path