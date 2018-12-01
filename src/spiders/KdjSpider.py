#coding:utf-8
'''
woojean@2018-10-10
'''

import sys
import requests
import time

from BaseSpider import BaseSpider

reload(sys)
sys.setdefaultencoding('utf-8')

# ============================================================================================
class KdjSpider(BaseSpider):  
  _source = 'kdj'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    endTime = str(int(round(time.time() * 1000)))
    url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=$ID$'
    if '000001' == id: # 上证指数
      url += '1'
    elif str(id)[0] in ['0','3']:
      url += '2'
    else:
      url += '1'

    url +='k&js=$FUN$((x))&rtntype=4&extend=kdj&check=kte&authorityType=fa&$FUN$=$FUN$'
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

  KdjSpider().initDir()

  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = KdjSpider(subIdList,threadId)
    spider.start()














