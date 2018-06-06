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
周最低价接近
+ 比例：
    - 1 - 1/1.01 = 0.0099 = 0.99%
    - 1 - 2/2.01 = 0.004975 = 0.4975%
    - 1 - 5/5.01 = 0.001996 = 0.1996%
    - 1 - 10/10.01 = 0.000999 = 0.099%
'''
class IntervalParser(BaseParser):
  _tag = 'IntervalParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    dayList1 = self.getPastTradingDayList(interval1[0],interval1[1])
    dayList2 = self.getPastTradingDayList(interval2[0],interval2[1])

    minPrice1 = self.getMinPriceOfDays(res,dayList1)
    minPrice2 = self.getMinPriceOfDays(res,dayList2)

    maxPrice1 = self.getMaxPriceOfDays(res,dayList1)
    maxPrice2 = self.getMaxPriceOfDays(res,dayList2)

    startPrice1 = self.getStartPriceOfDay(res,dayList1[0])
    startPrice2 = self.getStartPriceOfDay(res,dayList2[0])

    endPrice1 = self.getEndPriceOfDay(res,dayList1[-1])
    endPrice2 = self.getEndPriceOfDay(res,dayList2[-1])

    if 0==minPrice1*minPrice2*maxPrice1*maxPrice2*startPrice1*startPrice2*endPrice1*endPrice2:
      return False

    downLineLength1 = (min(startPrice1,endPrice1) - minPrice1)
    downLineLength2 = (min(startPrice2,endPrice2) - minPrice2)

    entity1 = maxPrice1-minPrice1
    entity2 = maxPrice2-minPrice2
    # print entity1,entity2

    rate1 = abs(downLineLength1/entity1)
    rate2 = abs(downLineLength2/entity2)

    # print downLineLength2,entity2
    # print rate2

    if rate1 < 0.5:
      return False

    if rate2 < 0.5:
      return False

    return True



# --------------------------------------------------------
# config
# --------------------------------------------------------
interval1 = ('2018-05-25',5)
interval2 = ('2018-06-01',5)

# interval1 = ('2017-04-21',5)
# interval2 = ('2017-04-28',5)

if __name__ == '__main__':
  print 'IntervalParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = IntervalParser(parseDay).getParseResult(True)
  print idList

















