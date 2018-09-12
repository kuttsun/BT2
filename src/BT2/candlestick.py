
# HTTP 通信を行うためのライブラリ
import requests
import time
from datetime import datetime,timezone
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import pytz

# cryptwatch からデータを取得してローソク足を生成
# https://qiita.com/0x0/items/883fd45c4bd3eb50fcb3
period = 300

# タイムゾーンを指定しなかった場合、JSTになる
g_begin = datetime(2018,9,11,0,0,0,0)
#g_begin = datetime(2018,9,11,0,0,0,0,pytz.timezone('Asia/Tokyo'))
print(g_begin)
print(g_begin.timestamp())
# begin に1日加算
g_end = g_begin + dt.timedelta(days=1)
print(g_end)
print(g_end.timestamp())

# ローソク足を取得する関数
def get_OHLC(before,after):
    url = 'https://api.cryptowat.ch/markets/bitflyer/btcjpy/ohlc'
    query = {
        # 時間足を秒で指定
        'periods':period,
        # 指定した日時より前のデータを取得
        'before':int(before.timestamp()),
        # 指定した日時より後のデータを取得
        'after':int(after.timestamp()),
    }
    res = requests.get(url,params=query).json()['result'][str(period)]
    return res

def download(x):
    begin = g_begin - dt.timedelta(days=x)
    end = g_end - dt.timedelta(days=x)
    # cryptowatch からデータ取得
    data = get_OHLC(end,begin)
    
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
    print(filename)

# cryptowatch は原則 6000件までしか取得できないので、それを超える範囲は取得できない
# 例えば、1分足であれば4日前までしか取得できず、それ以前は null になる
for x in range(30):
    download(x)
