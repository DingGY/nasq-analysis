import os
import re
import matplotlib.pyplot as plt

# nvidia
# targetPE = 0.0
# buyPE = 38.8
# buyMRQ = 35.68
# buyMR = buyPE / buyMRQ # MR = PE / MRQ
# nYear = 20
# cashRate = 3.9 # percentage
# growthRate = [100, 80, 40, 20, 10, 5, 5,5,5,5,5,5,5,5,5,5,5, 5, 5, 5,5,5,5,5,5,5,5,5,5,5, 5, 5, 5,5,5,5,5,5,5,5,5,5,5] # percentage

# # tsla
# targetPE = 0.0
# buyPE = 123.4
# buyMRQ = 12.0
# buyMR = buyPE / buyMRQ # MR = PE / MRQ
# nYear = 10
# cashRate = 3.9 # percentage
# growthRate = [-50.0, -20.0, 20.0, 100, 200, 150, 100,50,20,10,5,5,5,5,5,5,5, 5, 5, 5,5,5,5,5,5,5,5,5,5,5, 5, 5, 5,5,5,5,5,5,5,5,5,5,5] # percentage

# # ko
# targetPE = 0.0
# buyPE = 28.4
# buyMRQ = 12.145
# buyMR = buyPE / buyMRQ # MR = PE / MRQ
# nYear = 5
# cashRate = 3.9 # percentage
# growthRate = [13, 13, 13, 13, 13,13, 13,13, 13,13, 13,13, 13,13, 13,13, 13,13, 13,13, 13,13, 13] # percentage

# # meta
# targetPE = 0.0
# buyPE = 26.0
# buyMRQ = 8.88
# buyMR = buyPE / buyMRQ # MR = PE / MRQ
# nYear = 7
# cashRate = 3.9 # percentage
# growthRate = [25, 25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25] # percentage


# msft
targetPE = 0.0
buyPE = 31.15
buyMRQ = 9.54
buyMR = buyPE / buyMRQ # MR = PE / MRQ
nYear = 15
cashRate = 3.9 # percentage
growthRate = [20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20] # percentage

def calcNYearsByBuyPE():
    newret = 0.0
    ret = 999999.0
    growth = []
    cash = []
    years =[]
    maxYear = 40
    for i in range(1, maxYear):
        yearGrowth = 1.0
        totalGrowth = buyMR
        totalCash = buyPE
        for year in range(1, i):
            yearGrowth += yearGrowth * (growthRate[year - 1] / 100.0)
            totalGrowth +=  yearGrowth
            totalCash += totalCash * (cashRate / 100.0)
        growth.append(totalGrowth)
        cash.append(totalCash)
        years.append(i - 1)
        newret = abs(totalGrowth - totalCash)
        # print("nYear: %f, newret: %f, ret: %f" % (i, newret, ret))
        if ret <= newret:
            continue
        ret = newret
        nYear = i
    xp = years
    yp1 = growth
    yp2 = cash
    plt.plot(xp, yp1, label='stock')
    plt.plot(xp, yp2, label='cash')
    plt.legend()
    plt.show()
    return nYear,ret

def calcBuyPEByNYears():
    global growthRate
    newret = 0.0
    ret = 999999.0
    totalGrowth = 0.0
    totalCash = 0.0
    maxBuyPE = 100
    growth = []
    cash = []
    PEs =[]

    for i in range(maxBuyPE, 1, -1):
        totalCash = i
        totalGrowth = buyMR
        yearGrowth = 1
        for year in range(1, nYear):
            yearGrowth += yearGrowth * (growthRate[year - 1] / 100.0)
            totalGrowth +=  yearGrowth
            totalCash += totalCash * (cashRate / 100.0)
        growth.append(totalGrowth)
        cash.append(totalCash)
        PEs.append(i)
        newret = abs(totalGrowth - totalCash)
        # print("buyPE: %f, newret: %f, ret: %f" % (i, newret, ret))
        if ret <= newret:
            continue
        ret = newret
        buyPE = i
    xp = PEs
    yp1 = growth
    yp2 = cash
    plt.plot(xp, yp1, label='stock')
    plt.plot(xp, yp2, label='cash')
    plt.legend()
    plt.show()
    return buyPE,ret


def main():
    # year, retError = calcNYearsByBuyPE()
    # print("nYear: %f, retError: %f" % (year, retError))
    PE, retError = calcBuyPEByNYears()
    print("PE: %f, retError: %f" % (PE, retError))
main()
