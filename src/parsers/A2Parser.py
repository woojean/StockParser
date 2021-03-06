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
5日线下阳线，振幅前n
'''
class A2Parser(BaseParser):
  _tag = 'A2Parser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

  def calcuR(self,idList,num):
    num = topNum # 前n
    vList = []
    for id in idList:
      path = Tools.getPriceDirPath()+'/'+str(id)
      res = open(path,'r').read()
      
      # 振幅
      am = self.getAm(res,parseDay)
      print am

      r = am
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


topNum = 10

if __name__ == '__main__':
  print 'A2Parser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = A2Parser(parseDay).getParseResult(True)
  print idList


