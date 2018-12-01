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
from BaseParser import BaseParser
from common import Tools
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
“吞没线”
'''
class SwallowUpParser(BaseParser):
  _tag = 'SwallowUpParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 
  


  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    idFile = '吞没线/'+self._parseDay+'-SwallowUpParser.sel'
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
    # idList = self.calcuR(idList,1)

    if isDump:
      self.dumpIdList(idList)

    return idList


  def calcuR(self,idList,num):
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      # am = self.getEntityAm(res,parseDay)
      # d = KdjParser.getD(parseDay,id)

      # r = am/d
      # r = d

      dayList = BaseParser.getPastTradingDayList(parseDay,5) 
      (v,v,ma) = self.getMAPrice(res,dayList)
      endPrice = self.getEndPriceOfDay(res,parseDay)

      r = ma/endPrice

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
    dayList = BaseParser.getPastTradingDayList(parseDay,5) # 5日线
    lastDay = dayList[-2]
    startPriceOfLastDay = self.getStartPriceOfDay(res,lastDay)
    endPriceOfLastDay = self.getEndPriceOfDay(res,lastDay)
    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if startPrice == 0 or startPriceOfLastDay == 0:
      return False


    # 吞没线
    # -----------------------------------------------------------------------------
    # 第一天非阳线
    if endPriceOfLastDay > startPriceOfLastDay:
      return False

    # 第二天阳线
    if endPrice <= startPrice:
      return False

    # 第二天吞没第一天
    if not ((startPrice < endPriceOfLastDay) and (endPrice > startPriceOfLastDay)):
      return False


    # 第二天收盘价低于5日线
    # -----------------------------------------------------------------------------
    (v,v,ma5) = self.getMAPrice(res,dayList)
    if endPrice >= ma5:
      return False

    return True



if __name__ == '__main__':
  print 'SwallowUpParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = SwallowUpParser(parseDay).getParseResult(True)
  print idList

















