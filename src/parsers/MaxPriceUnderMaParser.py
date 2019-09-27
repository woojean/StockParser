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
最高价低于5日线
'''
class MaxPriceUnderMaParser(BaseParser):
  _tag = 'MaxPriceUnderMaParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 

  def getParseResult(self,isDump=False):
    print '***************************************************************************'
    print 'In custom mode'
    print '***************************************************************************'
    # idFile = '最高价低于5日线，振幅大于5%，D值小于20/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
    idFile = '最高价低于5日线，振幅大于5%，阳线/'+self._parseDay+'-MaxPriceUnderMaParser.sel'
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


  # def calcuR(self,idList,num):
  #   vList = []
  #   for id in idList:
  #     # path = Tools.getPriceDirPath()+'/'+str(id)
  #     # res = open(path,'r').read()
      
  #     # am = self.getAm(res,parseDay)
  #     # r = am

  #     r = random.random()

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



  def parse(self,res,parseDay,id=''):
    # 剔除新股
    # if self.isNewStock(res,parseDay):
    #   return False

    # 阳线
    # if not self.isYangXian(res,parseDay):
    #   return False

    # 最高价低于5日线
    # dayList = BaseParser.getPastTradingDayList(parseDay,5) 
    # (v,v,ma) = self.getMAPrice(res,dayList)
    # maxPrice = self.getMaxPriceOfDay(res,parseDay)
    # if maxPrice >= ma:
    #   return False

    # 振幅
    # am = self.getAm(res,parseDay)
    # if am < 0.05:
    #   return False


    # D低于
    # d = KdjParser.getD(parseDay,id)
    # if False == d:
    #   return False
    # if d >= 20:
    #   return False

    # D大于
    d = KdjParser.getD(parseDay,id)
    if False == d:
      return False
    if d <= 70:
      return False


    # 近10日有跌停
    # days = 10
    # recentlyHaveDownLimit = self.recentlyHaveDownwardLimit(res,parseDay,days)
    # if recentlyHaveDownLimit:
    #   return False




    return True



if __name__ == '__main__':
  print 'MaxPriceUnderMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaxPriceUnderMaParser(parseDay).getParseResult(True)
  print idList

















