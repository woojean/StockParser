#coding:utf-8
'''
woojean@2018-01-06
'''

import sys
import requests
from BaseSpider import BaseSpider
 
reload(sys)
sys.setdefaultencoding('utf-8')

# ============================================================================================
class WeekDataSpider(BaseSpider):  
  _source = 'week'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?rtntype=5&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305567214349641154_1528190496077&id=$ID$'
    if str(id)[0] in ['0','3']:
      url += '2'
    else:
      url += '1'
    url +='&type=wk&authorityType=&_=1528190512807'
    url = url.replace('$ID$',id)
    return url


if __name__ == '__main__':

  threads = 50 # 线程数（不能少于任务数）
  idList = BaseSpider.getIdList() 

  WeekDataSpider().initDir()
  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = WeekDataSpider(subIdList,threadId)
    spider.start()














