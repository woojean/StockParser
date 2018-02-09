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
class BasicSpider(BaseSpider):  
  _source = 'basic'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    url = 'http://nuff.eastmoney.com/EM_Finance2015TradeInterface/JS.ashx?id='
    url += str(id)
    if '0' == str(id)[0]:
      url +='2' 
    elif '6' == str(id)[0]:
      url +='1'
    url += '&token=4f1862fc3b5e77c150a2b985b12db0fd&cb=jQuery18305417846252412646_1515934547783&_=1515934547840'
    return url


if __name__ == '__main__':

  threads = 50 # 线程数（不能少于任务数）
  idList = BaseSpider.getIdList() 

  BasicSpider().initDir()

  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = BasicSpider(subIdList,threadId)
    spider.start()














