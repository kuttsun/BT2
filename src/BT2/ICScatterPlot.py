# 情報係数の散布図をプロット
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

args = sys.argv

# 読み込むファイルをプログラム引数で指定
# CSV からデータフレームを作成
print(args[1]);
df = pd.read_csv(args[1])

# MACD(2,3,2)の散布図の作成
#scatter = pd.DataFrame(df.next)
#_,_,scatter["histgram"] = talib.MACD(real, fastperiod=2, slowperiod=3, signalperiod=2)
#scatter = scatter.dropna()
#y = scatter["next"]
##y = (scatter["next"] - scatter["next"].mean())/scatter["next"].std(ddof=0)
#x = (scatter["histgram"] - scatter["histgram"].mean()) / scatter["histgram"].std(ddof=0)

# x:指標 y:値動き
# ヘッダーを除外するために１から
x = df.Indicator[1:]
y = df.Next[1:]

# 1次近似式を求める
a,b = np.polyfit(x,y,1)
# 相関係数を求める
correlation = np.corrcoef(x, y)[0,1]
# 決定係数
# 最小二乗法による直線フィッティングの場合，相関係数の二乗と決定係数は一致する
# https://mathtrain.jp/ketteikeisu
determination = correlation ** 2

# 描画領域の作成
fig = plt.figure(figsize=(10, 10))
# add_subplot(111) は add_subplot(1,1,1) と同じ（？）
ax = fig.add_subplot(111)
# 散布図のプロット
ax.scatter(x,y,alpha=0.5,color="Blue",linewidths="1")
# 近似線の描画
y2 = a * x + b
ax.plot(x, y2,color='black')
# テキストの描画
# 近似式
ax.text(0.1,0, 'y=' + str(round(a,4)) + 'x+' + str(round(b,4)),position=(4,0))
# 相関係数
ax.text(0.1,0, 'IC=' + str(round(correlation,4)),position=(4,40))
# 決定係数
ax.text(0.1,0, 'R2=' + str(round(determination,4)),position=(4,80))
# 図の保存
plt.savefig(args[1]+'.png')
# 図の表示
plt.show()