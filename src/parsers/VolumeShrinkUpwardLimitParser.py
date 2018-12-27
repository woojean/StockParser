#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-12-19
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
缩量涨停板
'''
class VolumeShrinkUpwardLimitParser(BaseParser):
  _tag = 'VolumeShrinkUpwardLimitParser'

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def parse(self,res,parseDay,id=''):

    # 缩量（相对前一日）*
    # # -------------------------------------------------------
    # if not self.isVolumnShrink(res,parseDay):
    #   return False


    # 20日线向上，60日线向上，20日线在60日线上方
    # -------------------------------------------------------
    # if not self.isMaInUpTrend(res,parseDay,20,60):
    #   return False

    
    # 近20日有涨停 
    # -------------------------------------------------------
    # if not self.recentlyHaveUpwardLimit(res,parseDay,20):
    #   return False
    

    # 缩量至最近最小值 
    # -------------------------------------------------------
    # days = self.minVolumnOfDays(res,parseDay)
    # if not days >= 20:
    #   return False
  

    # 近10日有连板
    # -------------------------------------------------------
    # if not self.recentlyHaveContinusUpwardLimit(res,parseDay,20):
    #   return False
    

    # 近20日涨停板数超过5
    # -------------------------------------------------------
    upwardLimitNum = self.countUpwardLimits(res,parseDay,60)
    if not upwardLimitNum >= 6:
      return False
    print upwardLimitNum
    return True






if __name__ == '__main__':
  print 'VolumeShrinkUpwardLimitParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = VolumeShrinkUpwardLimitParser(parseDay).getParseResult(True)
  print idList

















