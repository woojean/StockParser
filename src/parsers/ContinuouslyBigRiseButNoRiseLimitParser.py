#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-07
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
连板的变种：
连续两天（含两天以上）大涨，但未涨停
'''
class ContinuouslyBigRiseButNoRiseLimitParser(BaseParser):
  _tag = 'ContinuouslyBigRiseButNoRiseLimitParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  def parse(self,res,parseDay,id=''):
    ret = False

    dayList = self.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]
    day2 = dayList[1]
    day3 = dayList[2]

    endPrice1 = self.getEndPriceOfDay(res,day1)
    endPrice2 = self.getEndPriceOfDay(res,day2)
    endPrice3 = self.getEndPriceOfDay(res,day3)

    rise1 = (endPrice2 - endPrice1)/endPrice1 if (endPrice1!=0) else (0)
    rise2 = (endPrice3 - endPrice2)/endPrice2 if (endPrice2!=0) else (0)
    
    if rise1 < 0.05 or rise1 > 0.099:
      return False
    if rise2 < 0.05 or rise2 > 0.099:
      return False

    return True


if __name__ == '__main__':
  print 'ContinuouslyBigRiseButNoRiseLimitParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = ContinuouslyBigRiseButNoRiseLimitParser(parseDay).getParseResult(True)
  print idList

















