#coding:utf-8
'''
woojean@2018-01-06
'''

import sys
import requests
import time

from BaseSpider import BaseSpider

reload(sys)
sys.setdefaultencoding('utf-8')

# ============================================================================================
class MacdSpider(BaseSpider):  
  _source = 'macd'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    endTime = str(int(round(time.time() * 1000))) 
    url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=$ID$1&TYPE='
    if '3' == str(id)[0]:
      url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=$ID$2&TYPE='
    url +='k&js=$FUN$((x))&rtntype=4&extend=macd&check=kte&authorityType=fa&$FUN$=$FUN$'
    url = url.replace('$ID$',id).replace('$FUN$','fsDataTeacma' + endTime)
    return url


if __name__ == '__main__':

  threads = 50 # 线程数（不能少于任务数）
  idList = BaseSpider.getIdList() 

  MacdSpider().initDir()

  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = MacdSpider(subIdList,threadId)
    spider.start()














