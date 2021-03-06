#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-09-10
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
 
reload(sys)
sys.setdefaultencoding('utf-8')


rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools


'''
打首板过滤
'''
class FilterParser(BaseParser):
  _tag = 'FilterParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def isUpwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPriceOfDay1 = self.getEndPriceOfDay(res,dayList[0])
    endPriceOfDay2 = self.getEndPriceOfDay(res,dayList[1])
    if 0 == endPriceOfDay1 or  0 == endPriceOfDay2:
      return False
    gr =  (endPriceOfDay2-endPriceOfDay1)/endPriceOfDay1
    if gr > 0.09:
      return True
    return False

  def isDownwardLimit(self,res,parseDay):
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    endPriceOfDay1 = self.getEndPriceOfDay(res,dayList[0])
    endPriceOfDay2 = self.getEndPriceOfDay(res,dayList[1])
    if 0 == endPriceOfDay1 or  0 == endPriceOfDay2:
      return False
    gr =  (endPriceOfDay2-endPriceOfDay1)/endPriceOfDay1
    if gr < -0.09:
      return True
    return False


  def parse(self,res,parseDay,id=''):
    # 近几日无涨停、跌停行情，排除基于获利和解套的
    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    for day in dayList:
      if self.isUpwardLimit(res,day):
        return False
      if self.isDownwardLimit(res,day):
        return False

    
    # 流通市值小于50亿
    basicInfo = BaseParser.getBasicInfoById(id)
    mvc = float(basicInfo[45])
    if mvc < 1:
      return False # 错误数据
    
    if mvc > 5000000000:
      return False
    

    # 去掉ST，涨停有限
    name = Tools.getNameById(id)
    if 'st' in name or 'ST' in name:
      return False

    # # 换手率大于1%
    # changeRate = float(self.geChangeRateOfDay(res,parseDay))
    # if changeRate < 1.0:
    #   return False
      

    return True


if __name__ == '__main__':
  print 'FilterParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = FilterParser(parseDay).getParseResult(True)
  print idList

















