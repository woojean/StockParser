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
“均线汇合于实体”
'''
class MaConvergenceParser(BaseParser):
  _tag = 'MaConvergenceParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False

    startPrice = self.getStartPriceOfDay(res,parseDay)
    endPrice = self.getEndPriceOfDay(res,parseDay)

    dayList5 = BaseParser.getPastTradingDayList(parseDay,5)
    dayList10 = BaseParser.getPastTradingDayList(parseDay,10)
    dayList20 = BaseParser.getPastTradingDayList(parseDay,20)
    dayList60 = BaseParser.getPastTradingDayList(parseDay,60)

    (v1,v2,ma5) = self.getMAPrice(res,dayList5)
    (v1,v2,ma10) = self.getMAPrice(res,dayList10)
    (v1,v2,ma20) = self.getMAPrice(res,dayList20)
    (v1,v2,ma60) = self.getMAPrice(res,dayList60)

    minMa = min(ma5,ma10,ma20,ma60)
    maxMa = max(ma5,ma10,ma20,ma60)

    if minMa <= min(startPrice,endPrice):
      return False
    
    if maxMa >= max(startPrice,endPrice):
      return False

    return True



if __name__ == '__main__':
  print 'MaConvergenceParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaConvergenceParser(parseDay).getParseResult(True)
  print idList

















