#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-12-20
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
活跃股（基于一定时间内涨停板个数）
'''
class ActiveStockParser(BaseParser):
  _tag = 'ActiveStockParser'

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def parse(self,res,parseDay,id=''):

    # 近n日涨停板数超过m
    # -------------------------------------------------------
    days = 60
    minUpwardLimits = 3
    upwardLimitNum = self.countUpwardLimits(res,parseDay,days)
    if not upwardLimitNum >= minUpwardLimits:
      return False
    return True



if __name__ == '__main__':
  print 'ActiveStockParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = ActiveStockParser(parseDay).getParseResult(True)
  print idList

















