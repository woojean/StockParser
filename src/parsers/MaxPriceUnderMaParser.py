#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-06
'''

import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime
import random
from BaseParser import BaseParser
from KdjParser import KdjParser
from BiasParser import BiasParser
from common import Tools
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
最高价低于5日线的大阳线
'''
class MaxPriceUnderMaParser(BaseParser):
  _tag = 'MaxPriceUnderMaParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    # idFile = '最高价低于5日线的阳线且剔除新股/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
    # idFile = 'D<20且剔除新股/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
    # idFile = 'D<20阳线振幅>5%/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
    allIdList = Tools.getIdListOfFile(idFile)
    idList = []
    num = 0
    parsedNum = 0
    total = len(allIdList)
    for id in allIdList:
      try:
        self.printProcess(parsedNum,total)
        f = Tools.getPriceDirPath()+'/'+id
        res = open(f,'r').read()
        ret = self.parse(res,self._parseDay,id)
        if ret:
          idList.append(id)
          num += 1
          print str(num) + ' ↗'
        parsedNum += 1
      except Exception, e:
        pass
        print repr(e)
      
    print idList

    # 根据打分结果过滤
    # idList = self.calcuR(idList,5)

    if isDump:
      self.dumpIdList(idList)

    return idList


  def calcuR(self,idList,num):
    vList = []
    for id in idList:
      # path = Tools.getPriceDirPath()+'/'+str(id)
      # res = open(path,'r').read()
      
      # am = self.getAm(res,parseDay)
      # r = am

      r = random.random()

      vList.append((id,r))

    # 排序
    sList = sorted(vList,key=lambda x: -x[1]) 
    # sList = sorted(vList,key=lambda x: x[1]) 
    print "sorted list:"
    print sList
    selectedList = sList[:num]

    print "\nselected list:"
    print selectedList
    l = []
    for item in selectedList:
      l.append(item[0])
    return l



  def parse(self,res,parseDay,id=''):
    # 剔除新股
    # if self.isNewStock(res,parseDay):
    #   return False

    # 阳线
    if not self.isYangXian(res,parseDay):
      return False

    # # 最高价低于5日线
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if maxPrice > ma:
    #   return False

    # 振幅
    # am = self.getAm(res,parseDay)
    # if am < 0.05:
    #   return False


    
    # -----------------------------------------------------------------------------
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
    # lastDay = dayList[-2]
    # startPriceOfLastDay = self.getStartPriceOfDay(res,lastDay)
    # endPriceOfLastDay = self.getEndPriceOfDay(res,lastDay)
    # startPrice = self.getStartPriceOfDay(res,parseDay)
    # endPrice = self.getEndPriceOfDay(res,parseDay)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if startPrice == 0 or startPriceOfLastDay == 0:
    #   return False


    # 吞没线
    # if endPriceOfLastDay > startPriceOfLastDay: # 第一天非阳线
    #   return False
    # if endPrice <= startPrice: # 第二天阳线
    #   return False
    # if not ((startPrice < endPriceOfLastDay) and (endPrice > startPriceOfLastDay)): # 第二天吞没第一天
    #   return False

    # 秃顶秃底
    # if maxPrice > endPrice:
    #   return False
    # if minPrice < startPrice:
    #   return False

    # 长下引线
    # kLength = maxPrice - minPrice
    # downLineLength = startPrice - minPrice
    # r = downLineLength/kLength
    # if r <= 0.5:
    #   return False
    

    # 近n日跌停
    # haveDownwardLimit = False
    # dayList = BaseParser.getPastTradingDayList(parseDay,5)
    # for day in dayList:
    #   if self.isDownwardLimit(res,parseDay):
    #     haveDownwardLimit = True
    #     break
    # if haveDownwardLimit:
    #   return False


    # 近n日涨停
    # haveUpwardLimit = False
    # dayList = BaseParser.getPastTradingDayList(parseDay,10)
    # for day in dayList:
    #   if self.isUpwardLimit(res,parseDay):
    #     haveUpwardLimit = True
    #     break
    # if not haveUpwardLimit:
    #   return False


    # D低于
    # d = KdjParser.getD(parseDay,id)
    # if False == d:
    #   return False
    # if d >= 20:
    #   return False


    return True



if __name__ == '__main__':
  print 'MaxPriceUnderMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaxPriceUnderMaParser(parseDay).getParseResult(True)
  print idList

















