import os
import re
import akshare as ak
import matplotlib.pyplot as plt

def calcBuyPEByNYears(buyMR, nYear, cashRate, growthRate):
    newret = 0.0
    ret = 999999.0
    totalGrowth = 0.0
    totalCash = 0.0
    maxBuyPE = 100
    # growth = []
    # cash = []
    # PEs =[]
    # print("====> buyMR: %f, nYear: %d, cashRate: %f: growthRate: %f" % (buyMR, nYear, cashRate, growthRate))
    for i in range(maxBuyPE, 1, -1):
        totalCash = i
        totalGrowth = buyMR
        yearGrowth = 1
        for year in range(1, nYear):
            # yearGrowth += yearGrowth * (growthRate[year - 1] / 100.0)
            yearGrowth += yearGrowth * (growthRate / 100.0)
            totalGrowth +=  yearGrowth
            totalCash += totalCash * (cashRate / 100.0)
        # growth.append(totalGrowth)
        # cash.append(totalCash)
        # PEs.append(i)
        newret = abs(totalGrowth - totalCash)
        # print("buyPE: %f, newret: %f, ret: %f" % (i, newret, ret))
        if ret <= newret:
            continue
        ret = newret
        buyPE = i
    # xp = PEs
    # yp1 = growth
    # yp2 = cash
    # plt.plot(xp, yp1, label='stock')
    # plt.plot(xp, yp2, label='cash')
    # plt.legend()
    # plt.show()
    return buyPE, ret


#get all the nasq stock name list
KEEP_YEARS = 10
CASH_RATE = 3.2
PROFIT_RATE_YOY_MIN = 10.0
PROFIT_RATE_YOY_AVG_YEARS = 5

stock_analysis_fd = open('STOCK-ANALYSIS.log', 'a+')
stock_us_spot_em_df = ak.stock_us_spot_em()
stock_count = 0
for ids, row_stock in stock_us_spot_em_df.iterrows():
    try:
        stock_code = row_stock['代码'].split('.', 1)[1]

        stock_financial_us_analysis_indicator_em_df = ak.stock_financial_us_analysis_indicator_em(symbol=stock_code, indicator="年报")

        #calc buy MR

        stock_financial_last_year = stock_financial_us_analysis_indicator_em_df.iloc[0]
        buyMR = row_stock['总市值'] / stock_financial_last_year['PARENT_HOLDER_NETPROFIT'] / stock_financial_last_year['ROE_AVG'] / 100.0
        
        growthRate = 0.0
        count = PROFIT_RATE_YOY_AVG_YEARS
        for idf, row_financial in stock_financial_us_analysis_indicator_em_df.iterrows():
            profit_rate_yoy = row_financial['NET_PROFIT_RATIO_YOY']
            if profit_rate_yoy == None \
            or row_financial['ROE_AVG'] < PROFIT_RATE_YOY_MIN \
            or row_financial['PARENT_HOLDER_NETPROFIT'] < 0:
                growthRate = 0
                break
            # if growthRate == 0.0:
            #     growthRate =  profit_rate_yoy
            # if growthRate > profit_rate_yoy:
            #     growthRate = profit_rate_yoy
            growthRate += profit_rate_yoy
            count -= 1
            if count == 0:
                break
        growthRate /= PROFIT_RATE_YOY_AVG_YEARS
        if growthRate < PROFIT_RATE_YOY_MIN or count != 0:
            continue
        stock_count += 1
        aimPE, retError = calcBuyPEByNYears(buyMR, KEEP_YEARS, CASH_RATE, growthRate)
        # print("====> buyPE: %f, nowPE: %f, retError: %f" % (aimPE, row_stock['市盈率'], retError))
        if row_stock['市盈率'] < aimPE:
            stock_analysis_str = "====> NAME: %s, CODE: %s, BUY PE: %f, NOW PE: %f, 总市值: %f, PARENT_HOLDER_NETPROFIT: %f, ROE_AVG: %f, count: %d" % (row_stock['名称'], stock_code, aimPE, row_stock['市盈率'], row_stock['总市值'], stock_financial_last_year['PARENT_HOLDER_NETPROFIT'], stock_financial_last_year['ROE_AVG'], stock_count)
            print(stock_analysis_str)
            stock_analysis_fd.write(stock_analysis_str + '\n')
            stock_analysis_fd.flush()
    except:
        # print("============    %s NOT FOUND  =============" % stock_code)
        continue
stock_analysis_fd.close()
print("===> FINISHED: stock_count: %d" % stock_count)