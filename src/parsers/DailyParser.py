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
from KdjParser import KdjParser
from BiasParser import BiasParser
from MaxPriceUnderMaParser import MaxPriceUnderMaParser
 
reload(sys)
sys.setdefaultencoding('utf-8')

'''
弱水三千，只取一瓢
'''
class DailyParser(BaseParser):
  _tag = 'DailyParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

  def parse(self,res,parseDay,id=''):
    # 阳线
    # -------------------------------------------------------
    if not self.isYangXian(res,parseDay):
      return False

    # 最高价低于5日线
    # -------------------------------------------------------
    if not self.isMaxPriceUnderMa(res,parseDay,5):
      return False
    

    # 振幅
    # -------------------------------------------------------
    am = self.getAm(res,parseDay)
    # if not am >= 0.05:
    #   return False

    
    # 近n日涨停数
    # -------------------------------------------------------
    days = 60
    minUpwardLimitNum = 1
    upwardLimitNum = self.countUpwardLimits(res,parseDay,days)


    if (not upwardLimitNum >= minUpwardLimitNum) and (not am >= 0.05):
      return False


    return True



if __name__ == '__main__':
  print 'DailyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList


