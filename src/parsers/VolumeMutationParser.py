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
量突变
'''
class VolumeMutationParser(BaseParser):
  _tag = 'VolumeMutationParser'

  def __init__(self,parseDay):
    BaseParser.__init__(self,parseDay) 

  
  def parse(self,res,parseDay,id=''):
    # 近期有涨停（含当日）
    days = 10
    if not self.recentlyHaveUpwardLimit(res,parseDay,days):
      return False
    
    if not self.recentlyHaveDownwardLimit(res,parseDay,days):
      return False

    # 缩量至近期低点
    # recentShrinkDays = 10
    # days = self.minVolumnOfDays(res,parseDay)
    # if not days >= recentShrinkDays:
    #   return False

    # 相对前一日缩量程度
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # lastDay = dayList[0]
    # v1 = self.getVolumeOfDay(res,lastDay)
    # v2 = self.getVolumeOfDay(res,parseDay)
    # print v2/v1
    # if not (v2/v1 < 0.7) :
    #   return False
    

    # 涨停（排除一字板）
    # if not self.isUpwardLimit(res,parseDay):
    #   return False



    # 相对前一日缩量
    # dayList = BaseParser.getPastTradingDayList(parseDay,2)
    # lastDay = dayList[0]
    # v1 = self.getVolumeOfDay(res,lastDay)
    # v2 = self.getVolumeOfDay(res,parseDay)
    # if not v2 < v1 :
    #   return False


    # 近期有一字板涨停（含当日）
    # days = 10
    # if not self.recentlyHaveOneLineUpwardLimit(res,parseDay,days):
    #   return False

    

    # # 缩量（相对前一日）*
    # # -------------------------------------------------------
    # if not self.isVolumnShrink(res,parseDay):
    #   return False


    # # 20日线向上，60日线向上，20日线在60日线上方
    # # -------------------------------------------------------
    # if not self.isMaInUpTrend(res,parseDay,20,60):
    #   return False

    
    # # 近20日有涨停 
    # # -------------------------------------------------------
    # if not self.recentlyHaveUpwardLimit(res,parseDay,20):
    #   return False


    return True






if __name__ == '__main__':
  print 'VolumeMutationParser'

  parseDay = BaseParser.getParseDay()
  print parseDay

  idList = VolumeMutationParser(parseDay).getParseResult(True)
  print idList

















