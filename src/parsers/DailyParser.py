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
from KdjParser import KdjParser
from BiasParser import BiasParser
from MaxPriceUnderMaParser import MaxPriceUnderMaParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
5日线下阳线，涨停数前20
'''
class DailyParser(BaseParser):
  _tag = 'DailyParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

  def calcuR(self,idList,num):
    num = topNum # 前n
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      # 近60日涨停数
      upwardLimitNum = self.countUpwardLimits(res,parseDay,60)
      if upwardLimitNum < 1:
        continue
      print str(upwardLimitNum)

      r = upwardLimitNum
      vList.append((id,r))

    # 排序
    sList = sorted(vList,key=lambda x: -x[1]) 
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

    # 阳线
    # -------------------------------------------------------
    if not self.isYangXian(res,parseDay):
      return False

    # 最高价低于5日线
    # -------------------------------------------------------
    if not self.isMaxPriceUnderMa(res,parseDay,5):
      return False
    
    return True


topNum = 20

if __name__ == '__main__':
  print 'DailyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList


