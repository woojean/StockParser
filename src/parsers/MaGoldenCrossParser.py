#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-17
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
20日线上穿60日线
'''
class MaGoldenCrossParser(BaseParser):
  _tag = 'MaGoldenCrossParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  


  def parse(self,res,parseDay,id=''):
    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]

    R = 20
    B = 60

    dayListR_1 = self.getPastTradingDayList(lastDay,R)
    dayListB_1 = self.getPastTradingDayList(lastDay,B)
    (v,v,maR_1) = self.getMAPrice(res,dayListR_1)
    (v,v,maB_1) = self.getMAPrice(res,dayListB_1)

    dayListR_2 = self.getPastTradingDayList(parseDay,R)
    dayListB_2 = self.getPastTradingDayList(parseDay,B)
    (v,v,maR_2) = self.getMAPrice(res,dayListR_2)
    (v,v,maB_2) = self.getMAPrice(res,dayListB_2)

    # print maR_1,maB_1,maR_2,maB_2
    if maR_1 == -1 or maB_1 == -1 or maR_2 == -1 or maB_2 ==-1:
      return False

    if maR_1 > maB_1:
      return False

    if maR_2 < maB_2:
      return False

    return True
    



if __name__ == '__main__':
  print 'MaGoldenCrossParser'
  
  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaGoldenCrossParser(parseDay).getParseResult(True)
  print idList

















