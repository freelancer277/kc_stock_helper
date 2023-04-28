# kc_stock_helper
help stock imformation


# 安装库
要求本地python python3.8以上
在项目根目录下执行如下命令
```
pip install -r requirements.txt

```

# 历史数据加载
在项目根解压Data压缩包,解压后的文件夹放在项目根目录下,目前默认爬取了从2021-01-01之后的所有数据

# 增量数据更新
每天收盘后运行stock_data_downlaoder/akshare_downloader.py 即可

# 分析新高
运行stock_analysis中的peak_analysis.py 即可
默认为中证全指的所有股票为分析对象，250日内的新高，以最高价为准,上市日期不足250日的股票被认为是新高,需要修改条件的同学自行修改
如果希望分析A股全市场的股票，可以将代码中的注释部分取消注释

# 函数功能

见代码内注释


