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
“最大成交量判断”
'''
class VolumeMutationParser(BaseParser):
  _tag = 'VolumeMutationParser'
  _days = 30

  def __init__(self,parseDay,days = 30):
    self._days = days
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False

    # 是阳线
    if not self.isRise(res,parseDay):
      return False

    # 成交量最大
    if not self.isMaxVolumeOfDays(res,parseDay,self._days):
     return False

    # 之前的成交量比较小

    parseDayVolume = self.getVolumeOfDay(res,parseDay)

    pastDayList = BaseParser.getPastTradingDayList(parseDay,self._days)[:-1]
    for day in pastDayList:
      volume = self.getVolumeOfDay(res,day)
      rate = volume/parseDayVolume
      if (rate > 0.5) or (rate == 0):
        return False
    return True



if __name__ == '__main__':
  print 'VolumeMutationParser'

  days = 20

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = VolumeMutationParser(parseDay,days).getParseResult(True)
  print idList

















