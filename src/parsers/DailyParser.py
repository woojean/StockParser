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

    # D向上
    # -------------------------------------------------------
    if not KdjParser.isDUpward(parseDay,id):
      return False


    # D低于20 
    # -------------------------------------------------------
    d = KdjParser.getD(parseDay,id)
    if not (d < 20):
      return False


    # 近n日涨停数达到一定值（至少2个月有一个涨停）
    # -------------------------------------------------------
    days = 120
    minUpwardLimitNum = 3
    upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
    if not upwardLimitNum >= minUpwardLimitNum:
      return False


    return True


if __name__ == '__main__':
  print 'DailyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList


