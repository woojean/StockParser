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
    if not self.isYangXian(res,parseDay):
      return False

    # 振幅
    am = self.getAm(res,parseDay)
    minAm = 0.05
    if am < minAm:
      return False


    # J、D低位
    j = KdjParser.getJ(parseDay,id)
    d = KdjParser.getD(parseDay,id)
    if False == j or False == d:
      return False
    if ((not j<30) and (not d<20)):
      return False


    return True


if __name__ == '__main__':
  print 'DailyParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = DailyParser(parseDay).getParseResult(True)
  print idList


