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
“近n天最高价”
'''
class MaxPriceParser(BaseParser):
  _tag = 'MaxPriceParser'
  
  _days = 200

  def __init__(self,parseDay,days = 200):
    self._days = days
    BaseParser.__init__(self,parseDay) 


  def parse(self,res,parseDay,id=''):
    ret = False

    if not self.isMaxPriceOfDays(res,parseDay,self._days):
      return False

    return True



if __name__ == '__main__':
  print 'MaxPriceParser'

  days = 233

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = MaxPriceParser(parseDay,days).getParseResult(True)
  print idList

















