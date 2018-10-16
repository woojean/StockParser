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
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
上升趋势，大均线支撑
'''
class MaSupportParser(BaseParser):
  _tag = 'MaSupportParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 


  def isMaSupport(self,res,parseDay,maDays):
    dayList = BaseParser.getPastTradingDayList(parseDay,maDays)
    (v,v,ma) = self.getMAPrice(res,dayList)
    minPrice = self.getMinPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)
    if ((minPrice < ma) and (endPrice > ma)):
      return True
    return False



  def parse(self,res,parseDay,id=''):
    
    # 5日线金叉10日线
    # =========================================================================
    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    dayList = BaseParser.getPastTradingDayList(lastDay,5)
    (v,v,ma5_1) = self.getMAPrice(res,dayList)

    dayList = BaseParser.getPastTradingDayList(parseDay,5)
    (v,v,ma5_2) = self.getMAPrice(res,dayList)

    dayList = BaseParser.getPastTradingDayList(parseDay,10)
    (v,v,ma10) = self.getMAPrice(res,dayList)

    if (ma5_1 < ma10) and (ma5_2 > ma10):
      return True

    return False



    # 取参
    # =========================================================================
    # minPrice = self.getMinPriceOfDay(res,parseDay)
    # endPrice = self.getEndPriceOfDay(res,parseDay)

    # dayList = BaseParser.getPastTradingDayList(parseDay,20)
    # (v,v,ma20) = self.getMAPrice(res,dayList)

    # dayList = BaseParser.getPastTradingDayList(parseDay,60)
    # (v,v,ma60) = self.getMAPrice(res,dayList)


    # 初筛
    # =========================================================================
    # 月线在季线之上
    # if ma20 < ma60:
    #   return False

    # 排除均线缠绕
    # gapRate = ma20/ma60
    # if gapRate < 1.05:  
    #   return False

    # SLOWKD近期有死叉
    # if KdjParser.haveDeathCross(parseDay,id,5,5):
    #   return False


    # # 找信号
    # # =========================================================================
    # # 月线支撑
    # if ((minPrice < ma20) and (endPrice > ma20)):
    #   return True

    # # # 季线支撑
    # if ((minPrice < ma60) and (endPrice > ma60)):
    #   return True


    # # # 年线支撑
    # dayList = BaseParser.getPastTradingDayList(parseDay,250)
    # (v,v,ma250) = self.getMAPrice(res,dayList)
    # if ((minPrice < ma250) and (endPrice > ma250)):
    #   return True


    # return False



if __name__ == '__main__':
  print 'MaSupportParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaSupportParser(parseDay).getParseResult(True)
  print idList

















