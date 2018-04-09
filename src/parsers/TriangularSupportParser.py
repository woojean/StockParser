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
“三角托”
'''
class TriangularSupportParser(BaseParser):
  _tag = 'TriangularSupportParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False

    dayList5 = BaseParser.getPastTradingDayList(parseDay,5)
    dayList10 = BaseParser.getPastTradingDayList(parseDay,10)
    dayList20 = BaseParser.getPastTradingDayList(parseDay,20)

    (v1,v2,ma5) = self.getMAPrice(res,dayList5)
    (v1,v2,ma10) = self.getMAPrice(res,dayList10)
    (v1,v2,ma20) = self.getMAPrice(res,dayList20)
    
    # 当日 ma5 > ma20 > ma10
    if not ((ma5 > ma20) and (ma20 > ma10)):
      return False

    if abs(ma20-ma5) < abs(ma20-ma10):
      return False

    dayList = BaseParser.getPastTradingDayList(parseDay,2)
    parseDay = dayList[0]
    dayList5 = BaseParser.getPastTradingDayList(parseDay,5)
    dayList10 = BaseParser.getPastTradingDayList(parseDay,10)
    dayList20 = BaseParser.getPastTradingDayList(parseDay,20)
    (v1,v2,ma5) = self.getMAPrice(res,dayList5)
    (v1,v2,ma10) = self.getMAPrice(res,dayList10)
    (v1,v2,ma20) = self.getMAPrice(res,dayList20)

    # 2日前 ma20 > ma5 > ma10
    if not ((ma20 > ma5) and (ma5 > ma10)):
      return False

    return True



if __name__ == '__main__':
  print 'TriangularSupportParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = TriangularSupportParser(parseDay).getParseResult(True)
  print idList

















