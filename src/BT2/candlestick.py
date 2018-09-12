
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

# ローソク足を取得する関数
def get_OHLC(before,after):
    url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc'
    query = {
        # 時間足を秒で指定
        'periods':60,
        # 指定した日時より前のデータを取得
        'before':before,
        # 指定した日時より後のデータを取得
        'after':after,
    }
    res = requests.get(url,params=query).json()['result']['60']
    return res

# 無名関数
unixTime = lambda y,m,d,h: int(time.mktime(datetime(y,m,d,h).timetuple()))

now = datetime.today()
y,m,d,h = now.year,now.month,now.day,now.hour
text = str(y) + '-' + str(m) + '-' + str(d) + ' ' + str(h) + ':00'

data = get_OHLC(unixTime(y,m,d,h),unixTime(y,m,d,h - 1))

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
pd.DataFrame({'time':Time, 'open':Open, 'high':High, 'low':Low, 'close':Close}).to_csv('price.csv')

Date = [datetime(y,m,d,h - 1) + dt.timedelta(minutes=mi) for mi in range(60)]
ohlc = zip(mdates.date2num(Date),Open, High, Low, Close)
ax = plt.subplot()
# x軸の単位を指定（15分間隔で表示）
ax.xaxis.set_major_locator(mdates.MinuteLocator([0,15,30,45]))
# x軸の表示を指定（時：分）
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
# mpl_financeのメソッドを使用（描画幅やチャートの色などを指定。デフォルトは赤黒）
candlestick_ohlc(ax, ohlc, width=(1 / 24 / 60) * 0.7,colorup='g', colordown='r')

# チャート上部のテキスト
plt.title(text + '  BTC / JPY  by Cryptowatch API')

# チャートを png で保存
plt.savefig('price.png')
# チャートを描画
plt.show()