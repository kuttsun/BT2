
# HTTP 通信を行うためのライブラリ
import requests
import time
from datetime import datetime
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

# cryptwatch からデータを取得してローソク足を生成
# https://qiita.com/0x0/items/883fd45c4bd3eb50fcb3
period = 60
begin = datetime(2018,9,11)
# begin に1日加算
end = begin + dt.timedelta(days=1)

# ローソク足を取得する関数
def get_OHLC(before,after):
    url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc'
    query = {
        # 時間足を秒で指定
        'periods':period,
        # 指定した日時より前のデータを取得
        'before':before,
        # 指定した日時より後のデータを取得
        'after':after,
    }
    res = requests.get(url,params=query).json()['result'][str(period)]
    return res

# datetime から unixtime へ変換する無名関数
unixTime = lambda target: int(time.mktime(target.timetuple()))

# cryptowatch からデータ取得
data = get_OHLC(unixTime(end),unixTime(begin))

# 実行結果の詳細は以下を参照
# http://www.hacky.xyz/entry/2018/05/26/205229
Time,Open,High,Low,Close = [],[],[],[],[]
for i in data:
    Time.append(i[0])
    Open.append(i[1])
    High.append(i[2])
    Low.append(i[3])
    Close.append(i[4])

# CSV で出力
filename = str(period) + '_' + begin.strftime("%Y%m%d%H%M%S") + '-' + end.strftime("%Y%m%d%H%M%S")
pd.DataFrame({'time':Time, 'open':Open, 'high':High, 'low':Low, 'close':Close}).to_csv(filename + '.csv')

y,m,d,h = begin.year,begin.month,begin.day,begin.hour
Date = [begin + dt.timedelta(minutes=mi) for mi in range(60)]
ohlc = zip(mdates.date2num(Date),Open, High, Low, Close)
ax = plt.subplot()
# x軸の単位を指定（15分間隔で表示）
ax.xaxis.set_major_locator(mdates.MinuteLocator([0,15,30,45]))
# x軸の表示を指定（時：分）
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# mpl_financeのメソッドを使用（描画幅やチャートの色などを指定。デフォルトは赤黒）
candlestick_ohlc(ax, ohlc, width=(1 / 24 / 60) * 0.7,colorup='g', colordown='r')

# チャート上部のテキスト
text = str(y) + '-' + str(m) + '-' + str(d) + ' ' + str(h) + ':00'
plt.title(text + '  BTC / JPY  by Cryptowatch API')

# チャートを png で保存
plt.savefig(filename + '.png')
# チャートを描画
plt.show()