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
强者恒强
'''
class MinPriceContinuousRiseParser(BaseParser):
  _tag = 'MinPriceContinuousRiseParser'

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def parse(self,res,parseDay,id=''):

    # 连续n日最低价上涨
    # -------------------------------------------------------
    days = 5
    if not self.isMinPriceContinuousRise(res,parseDay,days,True):
      return False


    return True



if __name__ == '__main__':
  print 'MinPriceContinuousRiseParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MinPriceContinuousRiseParser(parseDay).getParseResult(True)
  print idList

















