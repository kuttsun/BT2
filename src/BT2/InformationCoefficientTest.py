import pandas as pd
#import talib
print("Information Coefficient Test")

# https://note.mu/sakiyama100/n/n20ef5a4c9549
# Time CHLO
inputs = [#["Time","Close","High","Low", "Open"]
    [1530482760, 716594, 716653, 716594, 716629],
    [1530482765, 716672, 716672, 716590, 716590],
    [1530482770, 716762, 716762, 716689, 716689],
    [1530482775, 716825, 716825, 716743, 716743],
    [1530482780, 716796, 716825, 716741, 716825]]
# 二次元配列からデータフレームを作成
#df = pd.DataFrame(inputs)

# CSV からデータフレームを作成
df = pd.read_csv("sample.csv")

#df.set_index('time',inplace = True)

# 表示
#print(df)

# 最初の5行を表示
print(df.head())

# カラムを表示
#print(df.columns)

#-------------------------------------


# 終値の差を計算
df["Diff"] = df["Close"] - df["Close"].shift()
# Next に次のデータの Diff を入れる(shift(-1)で１つ未来を示す)
df["Next"] = df["Diff"].shift(-1)
print(df.head())

#-------------------------------------

# nextと投資指標の値の相関を計算(ICの計算)
# ここでは例としてMACDのヒストグラムとの相関を見る

import numpy as np

real = [float(x) for x in df["Close"].values]
real = np.array(real)
# データフレームの作成
results = pd.DataFrame(columns=["fast","slow","signal","IC"])

# 短期EMAの期間を2から4つ(2～5)で試す
for short in range(2,4):
    # 長期EMAの期間を3から8つ(3～10)で試す
    for long in range(3,8):
        # シグナルの期間を2から5つ(2～6)で試す
        for signal in range(2,5):
            matrix = pd.DataFrame(df.Next)
            # MACD の計算(戻り値はMACD,Signal,ヒストグラム)
            _,_,matrix["histgram"] = talib.MACD(real, fastperiod=short, slowperiod=long, signalperiod=signal)
            # 欠損値(NaN)が一つでもある行を抜く
            matrix = matrix.dropna()
            y = matrix["next"]
            
            # mean は平均、stdは標準偏差
            # ddof(Delta Degrees of Freedom) については以下が参考になった
            # https://it-engineer-lab.com/archives/1057

            # 正規化（標準化）
            # データと平均の差を標準偏差で割ると，そのデータが平均からどの程度離れているかを評価できる
            x = (matrix["histgram"] - matrix["histgram"].mean()) / matrix["histgram"].std(ddof=0)
            # 最初のデータの次から評価する
            y = y[1:]
            x = x[1:]
            # 相関係数を求める
            # 戻り値は相関係数を要素に持つ行列なので、1行2列目のデータを取得
            # https://deepage.net/features/numpy-corrcoef.html#api%E3%83%89%E3%82%AD%E3%83%A5%E3%83%A1%E3%83%B3%E3%83%88
            correlation = np.corrcoef(x, y)[0,1]
            # データフレームの作成
            result = pd.DataFrame([[short,long,signal,correlation]], columns=["fast","slow","signal","IC"])
            results = results.append(result, ignore_index=True)

print(results)

#-------------------------------------
# MACD(2,3,2)の散布図の作成
scatter = pd.DataFrame(df.next)
_,_,scatter["histgram"] = talib.MACD(real, fastperiod=2, slowperiod=3, signalperiod=2)
scatter = scatter.dropna()
y = scatter["next"]
#y = (scatter["next"] - scatter["next"].mean())/scatter["next"].std(ddof=0)
x = (scatter["histgram"] - scatter["histgram"].mean())/scatter["histgram"].std(ddof=0)
y = y[1:]
x = x[1:]
a,b = np.polyfit(x,y,1)
correlation = np.corrcoef(x, y)[0,1]
determination = correlation**2

y2 = a * x + b

fig=plt.figure(figsize=(10, 10))
ax=fig.add_subplot(111)
ax.scatter(x,y,alpha=0.5,color="Blue",linewidths="1")
ax.plot(x, y2,color='black')
ax.text(0.1,0, 'y='+ str(round(a,4)) +'x+'+str(round(b,4)),position=(4,0))
ax.text(0.1,0, 'IC='+str(round(correlation,4)),position=(4,40))
ax.text(0.1,0, 'R2='+str(round(determination,4)),position=(4,80))
plt.show()