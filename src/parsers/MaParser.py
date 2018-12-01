#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-11-29
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
ma
'''
class MaParser(BaseParser):
  _tag = 'MaParser'

  def __init__(self,parseDay,id = ''):
    BaseParser.__init__(self,parseDay) 


  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    idFile = '20日均线支撑/'+self._parseDay+'-MaParser.sel'
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


  # def calcuR(self,idList,num):
  #   vList = []
  #   for id in idList:
  #     path = Tools.getPriceDirPath()+'/'+str(id)
  #     res = open(path,'r').read()
      
  #     # am = self.getEntityAm(res,parseDay)
  #     # d = KdjParser.getD(parseDay,id)

  #     # r = am/d
  #     # r = d

  #     dayList = BaseParser.getPastTradingDayList(parseDay,5) 
  #     (v,v,ma) = self.getMAPrice(res,dayList)
  #     endPrice = self.getEndPriceOfDay(res,parseDay)

  #     r = ma/endPrice

  #     vList.append((id,r))

  #   # 排序
  #   sList = sorted(vList,key=lambda x: -x[1]) 
  #   # sList = sorted(vList,key=lambda x: x[1]) 
  #   print "sorted list:"
  #   print sList
  #   selectedList = sList[:num]

  #   print "\nselected list:"
  #   print selectedList
  #   l = []
  #   for item in selectedList:
  #     l.append(item[0])
  #   return l
  

  def isSupportByMa(self,res,parseDay,maDays):
    endPrice = self.getEndPriceOfDay(res,parseDay)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    if endPrice == 0 or minPrice == 0:
      return False

    dayList = BaseParser.getPastTradingDayList(parseDay,maDays) 
    (v,v,ma) = self.getMAPrice(res,dayList)
    if ma < 0:
      return False

    if not ((minPrice < ma) and (endPrice > ma)):
      return False

    return True

    


  
  def parse(self,res,parseDay,id=''):
    # 剔除新股（含复牌股）
    # if self.isNewStock(res,parseDay):
    #   return False

    # 均线支撑
    # maDays = 20
    # if not self.isSupportByMa(res,parseDay,maDays):
    #   return False
    
    # 阳线
    if not self.isYangXian(res,parseDay):
      return False

    # 均线向上
    # maDays = 20
    # if not self.isMaUpward(res,parseDay,maDays):
    #   return False

    # 昨日10日线不向上（今日向上反转）
    # dayList = BaseParser.getPastTradingDayList(parseDay,2) 
    # lastDay = dayList[0]
    # maDays = 10
    # if self.isMaUpward(res,lastDay,maDays):
    #   return False

    # 振幅
    am = self.getAm(res,parseDay)
    if am < 0.05:
      return False

    # ma10 > ma20
    # dayList = BaseParser.getPastTradingDayList(parseDay,2) 
    # lastDay = dayList[0]
    # dayList10 = BaseParser.getPastTradingDayList(lastDay,10) 
    # (v,v,ma10) = self.getMAPrice(res,dayList10)
    # dayList20 = BaseParser.getPastTradingDayList(lastDay,20) 
    # (v,v,ma20) = self.getMAPrice(res,dayList20)
    # if ma10 <= ma20:
    #   return False


    return True



if __name__ == '__main__':
  print 'MaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaParser(parseDay).getParseResult(True)
  print idList

















