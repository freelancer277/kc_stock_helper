import pandas as pd
from pandas import DataFrame as df
from utils import file_utils
import datetime
#求某天，某个股票是否是n天最盘价新高，如果标的的上市时间不足n，是否需要返回新高,n默认为250

def is_new_high(infoDf, date, n=250,need_more_than_n_days=True,new_high_type="high"):
    # 获取最近n天的收盘价
    infoDf = infoDf[infoDf['date'] <= date]

    infoDf = infoDf.sort_values(by='date', ascending=False)
    infoDf = infoDf.head(n)
    if(need_more_than_n_days):
        if(len(infoDf)<n):
            return False
    # 获取最近n天的最高价
    high_price = infoDf[new_high_type].max()

    # 获取最近一天的收盘价
    last_price = infoDf[new_high_type].head(1).values[0]


    # 判断今天的价格是否是最近n天的最高价
    if last_price >= high_price:
        return True
    else:
        return False

#返回一段时间内某只股票所有满足n天新高的日期
def get_new_high_date_list(df, start_date, end_date, n=250,need_more_than_n_days=True,new_high_type="high"):
    # 遍历start_date到end_date之间的日期

    date_list = pd.date_range(start_date, end_date)
    new_high_date_list = []
    for date in date_list:
        date = date.strftime('%Y-%m-%d')
        # 判断某天是否是n天新高
        if is_new_high(df, date, n,need_more_than_n_days,new_high_type=new_high_type):
            new_high_date_list.append(date)
    return new_high_date_list

#计算一段时间内一些股票股票的n天新高日期
def get_all_stock_new_high_date_infoDf(start_date, end_date,stock_code_list, n=250,need_more_than_n_days=True,new_high_type="high"):
    #Need To Fix

    # 遍历所有股票的代码
    resultDf = df()
    all_stock_new_high_date_list = []
    for stock_code in stock_code_list:
        print(f"{stock_code}分析中...")
        try:
            # 获取某只股票的数据
            infoDf = pd.read_csv(f"{file_utils.get_data_path()}stock_history_data/{stock_code}_day.csv",dtype={'code':str})
            # 获取某只股票的n天新高日期
            new_high_date_list = get_new_high_date_list(infoDf, start_date, end_date, n,need_more_than_n_days,new_high_type)

            # 将某只股票的n天新高日期放到一个数组里面
            all_stock_new_high_date_list.append(new_high_date_list)
        except Exception as e:
            print(e)
            print(f"{stock_code}分析失败")
    # 转换成一个DataFrame,列名为股票代码，行名为日期
    resultDf = df(all_stock_new_high_date_list, index=stock_code_list)
    resultDf = resultDf.T
    return resultDf


# 遍历原有DataFrame,变行内容为列，列名为行内容
def tranDfToNewDf(originDf):
    #按列遍历
    resultDict = dict()
    for col in originDf.columns:

        for row in originDf.index:
            if(originDf.loc[row,col] != None):
                dateStr = originDf.loc[row,col]
                if(dateStr not in resultDict):
                    resultDict[dateStr] = [col]
                else:
                    resultDict[dateStr].append(col)
    #将resultDict 转换为DataFrame
    max_len  = max(len(v) for v in resultDict.values())
    for k,v in resultDict.items():
        if(len(v)<max_len):
            v.extend([None]*(max_len-len(v)))

    newDf = df.from_records(resultDict)
    return newDf



# 从全市场新高分析中剔除不在中证全指中的股票
def filter_stock_not_in_zz_stock_index(originDf):
    # 读取中证全指成分股
    zz_stock_index_df = pd.read_csv(f"{file_utils.get_data_path()}stock_code.csv", dtype={'品种代码': str})
    zz_stock_index_list = zz_stock_index_df['品种代码'].tolist()
    # 遍历originDf的每个cell,如果value为非中证全指成分股的股票,将此结果置空
    for col in originDf.columns:
        for row in originDf.index:
            if(originDf.loc[row,col] not in zz_stock_index_list):
                print(f"{originDf.loc[row,col]}不在中证全指成分股中")
                originDf.loc[row,col] = None



    return originDf




if __name__ == "__main__":
    #从1月5日开始
    start_date = "2022-01-05"
    #end_date是今天
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')

    resultFileName = file_utils.get_project_path() + "/data/单日最高价新高股票列表.csv"

    #A股全市场新高分析
    fileName = file_utils.get_project_path() + "/data/stock_code_full.csv"
    stock_code_list = pd.read_csv(fileName, dtype={'品种代码': str})['品种代码'].tolist()


    infoDf = get_all_stock_new_high_date_infoDf(start_date,end_date,stock_code_list)

    infoDf = tranDfToNewDf(infoDf)
    infoDf.to_csv(resultFileName,index=False)

    originDf = pd.read_csv(resultFileName,dtype=str)
    zzFileName = file_utils.get_project_path() + "/data/中证全指单日最高价新高股票列表.csv"
    resultDf = filter_stock_not_in_zz_stock_index(originDf)
    resultDf.to_csv(zzFileName, index=False)



