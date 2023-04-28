
import akshare as ak
from utils  import file_utils
#获取当前工程路径
import pandas as pd
import datetime
import time
import random

# 使用akshare获取所有A股代码

def get_all_stock_code(fileName="stock_code_full.csv"):
    print("开始爬取股票代码数据")

    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    resultDf = stock_zh_a_spot_df[["代码", "名称"]]
    #名称重命名为品种名称,代码重命名为品种代码并取后6位字符
    resultDf.columns = ["品种代码", "品种名称"]
    resultDf["品种代码"] = resultDf["品种代码"].astype(str).str.zfill(6)

    dataPath = file_utils.get_data_path()
    filePath = f"{dataPath}/{fileName}"
    print(f"存储路径为:{filePath}")
    stock_zh_a_spot_df.to_csv(filePath, index=False)
    return stock_zh_a_spot_df

#按照股票代码补全sz,sh,bj
def get_full_stock_code(stock_code):
    if stock_code.startswith("6"):
        return f"sh{stock_code}"
    elif stock_code.startswith("0"):
        return f"sz{stock_code}"
    elif stock_code.startswith("3"):
        return f"sz{stock_code}"
    else:
        return f"bj{stock_code}"


# 获取今日股票的实时数据
def get_stock_data_by_today():
    #获取今天日期
    date = datetime.datetime.now().strftime('%Y%m%d')
    filePath = f"{file_utils.get_data_path()}stock_daily_data/allstock_day_{date}.csv"
    stock_zh_a_spot_df = ak.stock_zh_a_spot()
    stock_zh_a_spot_df.to_csv(filePath, index=False)
# 获取某一段时间内的单个股票数据，日粒度
def get_stock_data_by_date(stock_code, start_date, end_date):

    #长度小于等于6的股票代码，补全sz,sh,bj
    if(len(stock_code) <= 6):
        full_stock_code = get_full_stock_code(stock_code)
    fileName = f"{stock_code}_day.csv"
    stock_zh_a_daily_df = ak.stock_zh_a_daily(symbol=full_stock_code, start_date=start_date, end_date=end_date,adjust="qfq")
    dataPath = file_utils.get_data_path()
    stock_zh_a_daily_df.to_csv(f"{dataPath}stock_history_data/{fileName}", index=False)


# 获取某一段时间内的所有股票数据，日粒度,默认爬取1000条数据,制定索引左闭右开
def get_all_stock_data_by_date(start_date, end_date,fullCodeFileName="stock_code_full.csv",start_index=0,end_index=1000):

    # 查看代码文件是否存在，如果存在就读取，不存在就爬取
    filePath = f"{file_utils.get_data_path()}{fullCodeFileName}"
    is_file_exist = file_utils.is_file_exist(filePath)

    if (is_file_exist):
        stock_zh_a_spot_df = pd.read_csv(filePath,dtype={"品种代码":str})
    else:
        stock_zh_a_spot_df = get_all_stock_code(fullCodeFileName)

    for index, row in stock_zh_a_spot_df.iterrows():
        #生成一个0-3的随机数，暂停爬取这个随机数的秒数，防止被封ip
        if index < start_index:
            continue
        if index >= end_index:
            break
        time.sleep(random.randint(0, 3))
        stock_code = row["品种代码"]
        print(f"目前爬取索引:{index},爬取的股票代码：{stock_code}")
        get_stock_data_by_date(stock_code, start_date, end_date)


# 获取指数成分股
def get_index_stock_info(indexCode,fileName=None):
    stock_zh_index_spot_df = ak.index_stock_cons(indexCode)
    dataPath = file_utils.get_data_path()
    if(fileName):
        filePath = f"{dataPath}{fileName}.csv"
    else:
        filePath = f"{dataPath}{indexCode}.csv"
    print(f"存储路径为:{filePath}")
    stock_zh_index_spot_df.to_csv(filePath, index=False)


# 获取中证全指的数据列表（整体的股票池）
def get_zzqz_stock_list():
    get_index_stock_info("000985","stock_code.csv")



# 纵向合并两个DataFrame的数据,并且按照日期排序,并且去重,以日期为主键，如果日期相同，以descDf为主
def update_stock_data_by_date(originDf,descDf):
    #合并两个DataFrame
    mergeDf = pd.concat([originDf,descDf],axis=0)
    #去重
    mergeDf = mergeDf.drop_duplicates(subset=["date"],keep="last")
    #按照日期排序,使用日期规则排序
    mergeDf["date"] = pd.to_datetime(mergeDf["date"],format="%Y/%m/%d")

    mergeDf = mergeDf.sort_values(by=["date"],ascending=True)
    return mergeDf





#date,open,high,low,close,volume,outstanding_share,turnover
#代码,名称,最新价,涨跌额,涨跌幅,买入,卖出,昨收,今开,最高,最低,成交量,成交额
# 匹配出来一个字典，key为中文，value为英文
reflectDictConfig = {
                     "open": "今开",
                     "high": "最高",
                     "low": "最低",
                     "close": "最新价",
                     "volume": "成交量"}

# 遍历allstock_day文件,添加到stock_history_data文件中,并更新日期
def update_stock_data(date=None):
    # 获取今天日期,如果没有补充
    if(date==None):
        date = datetime.datetime.now().strftime('%Y%m%d')
    # 获取历史数据
    filePath = f"{file_utils.get_data_path()}stock_daily_data/allstock_day_{date}.csv"
    stock_zh_a_spot_df = pd.read_csv(filePath)

    # 将今天的数据添加到历史数据中,遍历stock_zh_a_spot_df,获取每一行数据
    for index, row in stock_zh_a_spot_df.iterrows():
        code = row["代码"][2:8]
        # 按照reflectDictConfig,通过Row生成一个结果字典
        dateString = date[0:4] + "/" + date[4:6] + "/" + date[6:8]
        resultDict = {"date":dateString}
        fileName = f"{file_utils.get_data_path()}stock_history_data/{code}_day.csv"

        for key, value in reflectDictConfig.items():
            resultDict[key] = row[value]
        #获取流通股数,取originDf最后一位
        print(code)
        try:
            originDf = pd.read_csv(fileName)
            resultDict["outstanding_share"] = originDf["outstanding_share"].iloc[-1]
        except:
            #对于新股，重新爬取当日数据
            get_stock_data_by_date(code,date,date)
            continue
        #获取换手率
        resultDict["turnover"] = resultDict["volume"]/resultDict["outstanding_share"]

        # 根据resultDict生成一个DataFrame
        resultDf = pd.DataFrame(resultDict, index=[0])

        print(resultDf)


        #换手率计算,与总市值
        #20230427	13.45	13.63	12.9	13.09	429151

        mergeDf = update_stock_data_by_date(originDf,resultDf)
        mergeDf.to_csv(fileName, index=False)



    # # 更新日期
    # stock_zh_a_spot_df_history["日期"] = date
    # # 重新写入文件
    # stock_zh_a_spot_df_history.to_csv(filePath, index=False)



# 爬取一段时间所有股票的数据
def get_all_stock_data(startDate,endDate):
    # 循环请求，每次请求1000条数据,每次请求间隔1小时,超过6000条数据，就停止爬取
    startIndex = 0
    while(startIndex):
        endIndex = startIndex + 1000
        get_all_stock_data_by_date(startDate, endDate, start_index=startIndex, end_index=endIndex)
        startIndex = endIndex
        time.sleep(3600)
        if(startIndex > 6000):
            break

if __name__ == "__main__":
    #更新当日数据
    get_stock_data_by_today()
    update_stock_data()









