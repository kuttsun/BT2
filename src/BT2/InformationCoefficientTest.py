import pandas as pd

print("Information Coefficient Test")

# https://note.mu/sakiyama100/n/n20ef5a4c9549
# Time CHLO
inputs = [
    #["Time","Close","High","Low", "Open"]
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
print(df)

# 最初の5行を表示
print(df.head())