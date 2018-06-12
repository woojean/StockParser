#coding:utf-8
#!/usr/bin/env python
import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser

def getAllIdList():
  idList = []
  priceFileList = BaseParser.BaseParser.getPriceFileList()
  total = len(priceFileList)
  for f in priceFileList:
    try:
      id = f[-6:]
      if 6 != len(id):
        continue
      idList.append(id)
    except Exception, e:
      pass
      #print repr(e)
  return idList


def getAllRightIdList(dayList):
  allList = []
  day1 = dayList[0]
  day2 = dayList[-1]
  idList = getAllIdList()

  for id in idList:
    path = Tools.getPriceDirPath()+'/'+str(id)
    res = open(path,'r').read()
    parser = BaseParser.BaseParser(dayList[0])
    endPrice1 = parser.getEndPriceOfDay(res,day1)
    endPrice2 = parser.getEndPriceOfDay(res,day2)

    if 0 == endPrice1 or 0 == endPrice2:
      rate = -1
      continue
    else:
      rate = round((endPrice2 - endPrice1)/endPrice1,5)
    allList.append((id,rate))
  return allList


# 获取某一日的截止前一日强势股
def getTopGrowthIdListOfDayList(dayList):
  allList = []
  day1 = dayList[0]
  day2 = dayList[-1]
  idList = getAllIdList()
  parser = BaseParser.BaseParser(dayList[0])

  for id in idList:
    path = Tools.getPriceDirPath()+'/'+str(id)
    res = open(path,'r').read()
    endPrice1 = parser.getEndPriceOfDay(res,day1)
    endPrice2 = parser.getEndPriceOfDay(res,day2)

    # print day1,day2
    # print endPrice1,endPrice2

    if 0 == endPrice1:
      rate = -1
    else:
      rate = round((endPrice2 - endPrice1)/endPrice1,5)
    allList.append((id,rate))

  # 排序
  allList = sorted(allList,key=lambda i: i[1])
  l = len(allList)
  # print allList[0]
  # print allList[-1]
  #allList = allList[l-topNum:]
  allList = allList[traceDays:traceDays*2]
  return allList


# 获取指数在某一日的涨幅
def getGrowthRate(parseDay,days,id):
  dayList = BaseParser.BaseParser.getPastTradingDayList(parseDay,2)
  dayList = BaseParser.BaseParser.getNextTradingDayList(dayList[0],traceDays+1)
  path = Tools.getPriceDirPath()+'/'+str(id)
  res = open(path,'r').read()
  day1 = dayList[0]
  day2 = dayList[-1]

  parser = BaseParser.BaseParser(parseDay)
  endPrice1 = parser.getEndPriceOfDay(res,day1)
  endPrice2 = parser.getEndPriceOfDay(res,day2)

  # print day1,day2
  # print endPrice1,endPrice2
  
  if 0 == endPrice1:
    rate = -99999
  else:
    rate = round((endPrice2 - endPrice1)/endPrice1,5)*100.0
  # print rate
  return rate


# 获取指定个股在某一强于大盘的概率
def getStrongRate(parseDay,indexRate,stockList,traceDays):
  totalNum = len(stockList)
  strongNum = 0
  parser = BaseParser.BaseParser(parseDay)
  for item in stockList:
    id = item[0]    
    growthRate = getGrowthRate(parseDay,traceDays,id)
    if growthRate == -99999:
      totalNum -= 1
    if growthRate > indexRate:
      strongNum +=1
  # print 'totalNum:'+str(totalNum)
  # print 'strongNum:'+str(strongNum)
  rate = round(strongNum*1.0/totalNum,5)*100.0
  return rate


def getStayRate(stockList1,stockList2):
  idList1 = []
  idList2 = []
  for item in stockList1:
    idList1.append(item[0])
  for item in stockList2:
    idList2.append(item[0])
  totalNum = len(stockList1)
  inter = list(set(idList1).intersection(set(idList2)))
  interNum = len(inter)
  # print 'totalNum:'+str(totalNum)
  # print 'interNum:'+str(interNum)
  rate = round(interNum*1.0/totalNum,5)*100.0
  return rate

# ----------------------------------------------------------------------------
countDays = 60
traceDays = 10
topNum = 300

'''
2018-05-25 10 -2.77
'''

'''
                    all       200      300    500
2017/9/7    -0.23   49.951   40.5   42.333     46
2018/4/27    3.57   40.697     38   37.333   36.8
2018/5/25   -2.77   27.828   31.5   30.667   28.2
'''

if __name__ == '__main__':
  parseDay = '2018-05-25'  # 2018-06-08
  indexRate = -2.77


  # parseDay = '2018-06-07'
  # indexRate = -0.182
  
  print '比较日：'+parseDay
  dayList = BaseParser.BaseParser.getPastTradingDayList(parseDay,2)
  dayList = BaseParser.BaseParser.getNextTradingDayList(dayList[0],traceDays+1)
  allStockList = getAllRightIdList(dayList)
  print '参与跟踪的个股总数：'+str(len(allStockList))

  strongRate = getStrongRate(parseDay,indexRate,allStockList,traceDays)
  print '在'+str(traceDays)+'天后，整个市场个股涨幅超过大盘的概率为：'+str(strongRate) +'%'

  print '前'+str(countDays)+'日涨幅居前'+str(topNum)+'位的个股，'

  # compareStockList = getTopGrowthIdListOfDayList(dayList)

  dayList = BaseParser.BaseParser.getPastTradingDayList(parseDay,countDays+1)
  stockList = getTopGrowthIdListOfDayList(dayList)
  print '参与统计的个股总数：'+str(len(stockList))
  #print stockList
  

  # interRate = getStayRate(compareStockList,stockList)  # 仍然处于top的概率

  # 强于大盘
  strongRate = getStrongRate(parseDay,indexRate,stockList,traceDays)
  print '在'+str(traceDays)+'天后涨幅超过大盘的概率为：'+str(strongRate) +'%'

  











