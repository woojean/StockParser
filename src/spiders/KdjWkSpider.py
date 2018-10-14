#coding:utf-8
'''
woojean@2018-10-11
'''

import sys
import requests
import time

from BaseSpider import BaseSpider

reload(sys)
sys.setdefaultencoding('utf-8')

# ============================================================================================
class KdjWkSpider(BaseSpider):  
  _source = 'kdjwk'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    endTime = str(int(round(time.time() * 1000))) 
    url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=$ID$1&TYPE='
    if ('3' == str(id)[0])  or ('0' == str(id)[0]):
      url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=$ID$2&TYPE='
    url +='wk&js=$FUN$((x))&rtntype=4&extend=kdj&check=kte&authorityType=fa&$FUN$=$FUN$'
    url = url.replace('$ID$',id).replace('$FUN$','fsDataTeacma' + endTime)
    print url
    return url
    '''
    http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?token=4f1862fc3b5e77c150a2b985b12db0fd&rtntype=6&id=0000022&type=wk&authorityType=fa&cb=jsonp1539234497088
    http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000022&TYPE=k&js=fsDataTeacma((x))&rtntype=4&extend=kdj&check=kte&authorityType=fa&fsDataTeacma=fsDataTeacma
    '''

if __name__ == '__main__':

  threads = 50 # 线程数（不能少于任务数）
  idList = BaseSpider.getIdList() 

  KdjWkSpider().initDir()

  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = KdjWkSpider(subIdList,threadId)
    spider.start()














