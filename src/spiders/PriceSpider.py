#coding:utf-8
'''
woojean@2018-01-06
'''

import sys
import requests
from BaseSpider import BaseSpider
 
reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

# ============================================================================================
class PriceSpider(BaseSpider):  
  _source = 'price'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=$ID$'
    if str(id)[0] in ['0','3']:
      url += '2'
    else:
      url += '1'
    url +='&TYPE=k&js=fsDataTeacma((x))&rtntype=5&authorityType=fa&isCR=false&fsDataTeacma=fsDataTeacma'
    url = url.replace('$ID$',id)
    return url
  '''
  http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0027982&TYPE=k&js=fsDataTeacma((x))&rtntype=5&authorityType=fa&isCR=false&fsDataTeacma=fsDataTeacma
  '''

if __name__ == '__main__':

  threads = 50 # 线程数（不能少于任务数）
  idList = BaseSpider.getIdList() 
  # idList = Tools.get300IdList() 
  print idList

  PriceSpider().initDir()
  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = PriceSpider(subIdList,threadId)
    spider.start()














