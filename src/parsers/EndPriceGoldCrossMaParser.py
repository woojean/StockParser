#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-03
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

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools


'''
'''
class EndPriceGoldCrossMaParser(BaseParser):
  _tag = 'EndPriceGoldCrossMaParser'
  
  def __init__(self,parseDay,id=''):
    BaseParser.__init__(self,parseDay) 
  

  def parse(self,res,parseDay,id=''):
    maDays = 20
    if not self.isMaUpward(res,parseDay,maDays):
      return False

    dayList = self.getPastTradingDayList(parseDay,2)
    lastDay = dayList[0]
    

    return True



if __name__ == '__main__':
  print 'EndPriceGoldCrossMaParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = EndPriceGoldCrossMaParser(parseDay).getParseResult(True)
  print idList

