#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-07-23
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
“近n天最低价大于MA”
'''
class MinPriceMoreThanMa(BaseParser):
  _tag = 'MinPriceMoreThanMa'

  def __init__(self,parseDay,days = 200):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = True
    dayList = self.getPastTradingDayList(parseDay,days)
    for day in dayList:
      maDayList = self.getPastTradingDayList(day,maDays)
      (v,v,ma) = self.getMAPrice(res,maDayList)
      minPrice = self.getMinPriceOfDay(res,day)

      if ma == -1:
        ret = False
        break
      if minPrice == 0:
        ret = False
        break

      if minPrice < ma:
        ret = False
        break
    
    return ret


days = 3
maDays = 5

if __name__ == '__main__':
  print 'MinPriceMoreThanMa'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MinPriceMoreThanMa(parseDay,days).getParseResult(True)
  print idList

















