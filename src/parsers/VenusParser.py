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
“启明星”
'''
class VenusParser(BaseParser):
  _tag = 'VenusParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False
    dayList = BaseParser.getPastTradingDayList(parseDay,3)
    day1 = dayList[0]  # 第一天
    day2 = dayList[1]  # 第二天
    day3 = dayList[2]  # 第三天

    startPriceOfDay1 = self.getStartPriceOfDay(res,day1)
    endPriceOfDay1 = self.getEndPriceOfDay(res,day1)
    entityOfDay1 = abs(startPriceOfDay1 - endPriceOfDay1)
    startPriceOfDay2 = self.getStartPriceOfDay(res,day2)
    endPriceOfDay2 = self.getEndPriceOfDay(res,day2)
    entityOfDay2 = abs(startPriceOfDay2 - endPriceOfDay2)
    startPriceOfDay3 = self.getStartPriceOfDay(res,day3)
    endPriceOfDay3 = self.getEndPriceOfDay(res,day3)
    entityOfDay3 = abs(startPriceOfDay3 - endPriceOfDay3)

    # 去掉第1天不是阴线
    if endPriceOfDay1 >= startPriceOfDay1:
      return False

    # 去掉第3天不是阳线
    if endPriceOfDay3 <= startPriceOfDay3:
      return False

    # 第2天必须和前后两天形成实体跳空
    upperEntityPriceOfDay2 = max(startPriceOfDay2,endPriceOfDay2)
    if upperEntityPriceOfDay2 > min(endPriceOfDay1,startPriceOfDay3):
      return False

    # 第2天的实体长度应该小于另两天的1/4
    if entityOfDay2/min(entityOfDay1,entityOfDay3) > 0.25:
      return False

    return True



if __name__ == '__main__':
  print 'VenusParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = VenusParser(parseDay).getParseResult(True)
  print idList

















