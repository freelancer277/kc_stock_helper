
import pandas as pd
from utils import file_utils
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ochl
#根据数据绘制日K线图
filename = file_utils.get_data_path() + 'stock_history_data/000001_day.csv'
stock_df = pd.read_csv(filename)
#,index_col='date',parse_dates=['date']
print(stock_df.head())

# 绘制K线图
fig, ax = plt.subplots()
#date,open,high,low,close,volume,outstanding_share,turnover
candlestick_ochl(
    ax,
    stock_df[["date", "open", "high","low","close"]].values,
    width=0.5,
    colorup="red",
    colordown="green",
)

ax.set_xticklabels(stock_df["date"], rotation=30)
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.set_title("000001 Candlestick Chart")
plt.show()
