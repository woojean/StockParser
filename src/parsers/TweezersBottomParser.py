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
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
镊形底
'''
class TweezersBottomParser(BaseParser):
  _tag = 'TweezersBottomParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False
    
    dayList = self.getPastTradingDayList(parseDay,2)
    day1 = dayList[0]  # 前一天
    day2 = dayList[1]  # 后一天
    
    # 前一天触及10日最低价
    if not self.isTouchMinPriceOfDays(res,day1,10):
      return False

    # 两天的最低价“接近或一致”
    minPriceOfDay1 = self.getMinPriceOfDay(res,day1)
    minPriceOfDay2 = self.getMinPriceOfDay(res,day2)
    rate = abs((minPriceOfDay2- minPriceOfDay1)/minPriceOfDay1)
    if rate > 0.001:
      return False

    '''
    # 第二天是阳线
    startPrice = self.getStartPriceOfDay(res,day2)
    endPrice = self.getEndPriceOfDay(res,day2)
    if startPrice > endPrice:
      return False
    '''

    return True



if __name__ == '__main__':
  print 'TweezersBottomParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = TweezersBottomParser(parseDay).getParseResult(True)
  print idList

















