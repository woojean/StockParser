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
class MaSpider(BaseSpider):  
  _source = 'ma'

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
    url +='&TYPE=k&js=$FUN$((x))&rtntype=4&extend=ma&check=kte&authorityType=fa&$FUN$=$FUN$'
    url = url.replace('$ID$',id).replace('$FUN$','fsDataTeacma' + endTime)
    return url
    '''
    http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000022&TYPE=k&js=fsDataTeacma((x))&rtntype=4&extend=ma&check=kte&authorityType=fa&fsDataTeacma=fsDataTeacma
    '''

if __name__ == '__main__':

  threads = 50 # 线程数（不能少于任务数）
  idList = BaseSpider.getIdList() 

  MaSpider().initDir()

  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = MaSpider(subIdList,threadId)
    spider.start()














