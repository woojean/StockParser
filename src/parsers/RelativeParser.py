#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-17
'''

import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime
from BaseParser import BaseParser
from KdjParser import KdjParser
from BiasParser import BiasParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
相对解析
'''
class RelativeParser(BaseParser):
  _tag = 'RelativeParser'

  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 


  # def getParseResult(self,isDump=False):
  #   print '***************************************************************************'
  #   print 'In custom mode'
  #   print '***************************************************************************'
  #   idFile = '两年5日线下阳线/'+self._parseDay+'-RelativeParser.sel'
  #   allIdList = Tools.getIdListOfFile(idFile)
  #   idList = []
  #   num = 0
  #   parsedNum = 0
  #   total = len(allIdList)
  #   for id in allIdList:
  #     try:
  #       self.printProcess(parsedNum,total)
  #       f = Tools.getPriceDirPath()+'/'+id
  #       res = open(f,'r').read()
  #       ret = self.parse(res,self._parseDay,id)
  #       if ret:
  #         idList.append(id)
  #         num += 1
  #         print str(num) + ' ↗'
  #       parsedNum += 1
  #     except Exception, e:
  #       pass
  #       print repr(e)
      
  #   print idList

  #   # 根据打分结果过滤
  #   # idList = self.calcuR(idList,3)

  #   if isDump:
  #     self.dumpIdList(idList)

  #   return idList


  # 均线距离
  # def calcuR(self,idList,num):
  #   vList = []
  #   for id in idList:
  #     path = Tools.getPriceDirPath()+'/'+str(id)
  #     res = open(path,'r').read()
      
  #     # 近10日跌幅最大
  #     dayList = BaseParser.getPastTradingDayList(self._parseDay,10)
  #     startDay = dayList[0]
  #     endPrice = self.getEndPriceOfDay(res,self._parseDay)
  #     endPriceS = self.getEndPriceOfDay(res,startDay)
  #     r = (endPrice - endPriceS)/endPriceS

  #     vList.append((id,r))

  #   # 排序
  #   sList = sorted(vList,key=lambda x: x[1]) 
  #   print "sorted list:"
  #   print sList
  #   selectedList = sList[:num]

  #   print "\nselected list:"
  #   print selectedList
  #   l = []
  #   for item in selectedList:
  #     l.append(item[0])
  #   return l



  def parse(self,res,parseDay,id=''):
    # D向上反转
    # -----------------------------------------------------------------
    # if not KdjParser.isDDeclineDeceleration(parseDay,id):
    #   return False


    # 5日线下K线
    # -----------------------------------------------------------------
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
    # lastDay = dayList[-2]
    # startPrice = self.getStartPriceOfDay(res,parseDay)
    # endPrice = self.getEndPriceOfDay(res,parseDay)
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if startPrice ==0 or endPrice ==0 or minPrice ==0 or maxPrice ==0:
    #   return False

    # 阳线
    # if endPrice <= startPrice:
    #   return False

    # 最高价位于ma之下
    # (v,v,ma5) = self.getMAPrice(res,dayList)
    # if maxPrice >= ma5:
    #   return False


    # 振幅大于n%
    # minP = minPrice
    # r = (maxPrice - minP)/minP
    # if (r <= 0.05):
    #   return False

    # D低于20
    # d = KdjParser.getD(parseDay,id)
    # if d >= 20:
    #   return False

    #  D向上反转
    # if not KdjParser.isDBottomReversal(parseDay,id):
    #   return False

    # KD金叉
    if not KdjParser.isKdGoldCross(parseDay,id):
      return False


    # 5日量比
    # dayList = BaseParser.getPastTradingDayList(parseDay,5)
    # mv5 = self.getMv(res,dayList)
    # v = self.getVolumeOfDay(res,parseDay)
    # if v <= mv5:
    #   return False

    # BIAS为正
    # if not BiasParser.isBiasNegative(parseDay,id):
    #   return False

    return True


if __name__ == '__main__':
  print 'RelativeParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = RelativeParser(parseDay).getParseResult(True)
  print idList

















