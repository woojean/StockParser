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
RGB
'''
class RgbParser(BaseParser):
  _tag = 'RgbParser'
  
  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 
  

  def isRgb(self,res,day):
    R = 5
    G = 8
    B = 13

    dayList = self.getPastTradingDayList(day,R)
    (v,v,maR) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,G)
    (v,v,maG) = self.getMAPrice(res,dayList)

    dayList = self.getPastTradingDayList(day,B)
    (v,v,maB) = self.getMAPrice(res,dayList)

    if not ((maR > maG) and (maG > maB)):
      return False

    return True


  def parse(self,res,parseDay,id=''):
    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]

    # 今天是RGB，但昨天不是
    if not self.isRgb(res,parseDay) :
      return False

    if self.isRgb(res,lastDay):
      return False

    # 换手率大于1%
    '''
    basicInfo = BaseParser.getBasicInfoById(id)
    changeRate = float(basicInfo[37])
    if changeRate <= 2.0:
      return False
    '''

    return True
    



if __name__ == '__main__':
  print 'RgbParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = RgbParser(parseDay).getParseResult(True)
  print idList

















