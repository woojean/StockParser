#coding:utf-8
'''
woojean@2018-09-10
'''

import sys
import requests
import time
import re
import datetime

from BaseSpider import BaseSpider

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

# ============================================================================================
class MonitorSpider(BaseSpider):  
  _source = 'monitor'

  def __init__(self,idList=[],threadId=0): 
    BaseSpider.__init__(self,idList,threadId) 
    
  def genUrl(self,id):
    endTime = str(int(round(time.time() * 1000))) 
    url = 'http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?token=4f1862fc3b5e77c150a2b985b12db0fd&rtntype=6&id=$ID$'
    if str(id)[0] in ['0','3']:
      url += '2'
    else:
      url += '1'
    url +='&type=m5k&authorityType=fa&cb=jsonp1536580250828'
    url = url.replace('$ID$',id)
    return url
  

  def getPrevTime(self,parseTime):
    prevTime = (datetime.datetime.strptime(parseTime, "%Y-%m-%d %H:%M")-datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')
    return prevTime


  # def getDataMap(self,res):
  #   dataMap = {}
  #   index = res.index('data')
  #   res = res[index:]
  #   index = res.index('flow')
  #   res = res[:index]
  #   print res
  #   # itemList = re.findall(r'(\d{4}-\d{1,2}-\d{1,2})\S(.*?)",', res)
  #   itemList = re.findall(r'"2018-09-10 10:40(.*?)",', res)
  #   print itemList
  #   for item in itemList:
  #     arr = item[1].split(',') 
  #     dataMap[item[0]+' '+arr[0]] = arr
  #   return dataMap


  def getTimeData(self,res,time):
    '''
                    0      0开    1收    2最高    3最低    4量   5额 
    (u'2018-09-1', u'13:20,3.61,3.61,3.61,3.61,586,211436,0%')
    '''
    p = r'"'+time+',(.*?)",'
    ret = re.findall(p, res)
    return ret[0].split(',')


  def isMutation(self,id,res):
    print '.'
    # 取参
    date = parseTime[0:10]
    t1 = date +' 09:35'
    t2 = date +' 09:40'
    t3 = date +' 09:45'
    prevT = self.getPrevTime(parseTime) # 前一根
    prevPrevT = self.getPrevTime(prevT) # 前前一根

    data = self.getTimeData(res,parseTime)
    t1data = self.getTimeData(res,t1)
    t2data = self.getTimeData(res,t2)
    t3data = self.getTimeData(res,t3)
    prevTdata = self.getTimeData(res,prevT)
    prevPrevTdata = self.getTimeData(res,prevPrevT)
    
    v = int(data[4])
    v1 = int(t1data[4])
    v2 = int(t2data[4])
    v3 = int(t3data[4])
    vp = int(prevTdata[4])
    vpp = int(prevPrevTdata[4])
    if v==0 or v1==0 or v2==0 or v3==0:
      # print '参数错误'
      return False
    

    # 当前量超过"前3个"量
    if v<v1 or v<v2 or v<v3:
      # print 'X 当前量超过前3个量'
      return False


    # 爆量
    if v < vp:
      return False

    rate = v/vpp
    if rate < 5:  
      # print 'X 爆量'
      return False

    # 阳柱
    startPrice = float(data[0])
    endPrice = float(data[1])
    if startPrice == 0 or endPrice == 0:
      return False
    
    if endPrice <= startPrice:
      return False

    self.dumpId(id)
    return True
  
  def dumpId(self,id):
    monitorDirPath = Tools.getMonitorDirPath()
    #open('data/golden-pin-bottom/'+ confirmDay +'.sel','w').write(','.join(idList))
    open(monitorDirPath + '/' +id,'w').write(id)


  def run(self):
    for id in self._idList:
      idType = str(id)[0]
      if idType not in ['6','0','3']: # 只看A股 0 深，6 沪，3 创业板，5 基金权证， 1 深市基金
        continue
      try:
        url = self.genUrl(id)
        print str(self._threadId) + ' ·-> ' +str(id)
        res = requests.get(url,verify=False).text
        # res = ''
        ret = self.isMutation(id,res)
        if ret: # 发出信号
          print str(id)
      except Exception, e:
        pass
        # print repr(e)


def getFilteredIdList(date):
  # http://quote.eastmoney.com/stocklist.html
  fp = Tools.getRootPath()+'/data/enterList/'+date+'-FilterParser.sel'
  print fp
  f = open(fp,'r')
  data = f.read()
  idList = data.split(',')
  return idList


def printTime(parseTime,filteredDate):
  print "当前时间："+parseTime
  print "过滤文件日期："+filteredDate
  minutes = parseTime[11:]
  if minutes < '09:35':
    print "开盘时间不够！"
  if minutes > '15:30':
    print "已收盘！"

  minute = parseTime[-1]
  if int(minute) < 5:
    parseTime = parseTime[:-1]+'0'
  if int(minute) > 5:
    parseTime = parseTime[:-1]+'5'
  print "实际解析时间："+ parseTime



if __name__ == '__main__':
  # config
  parseTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
  

  filteredDate = "2018-09-07"  # 过滤文件
  parseTime = "2018-09-10 11:10"  # 自定义时间

  printTime(parseTime,filteredDate)
  
  threads = 50 # 线程数（不能少于任务数）
  idList = getFilteredIdList(filteredDate)

  # threads = 1
  # idList = ['002076'] 

  # MonitorSpider().initDir()
  # Tools.initDir('monitor')
  

  print "\n================================================\n"
  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = MonitorSpider(subIdList,threadId)
    spider.start()

  '''
  http://pdfm.eastmoney.com/EM_UBG_PDTI_Fast/api/js?token=4f1862fc3b5e77c150a2b985b12db0fd&rtntype=6&id=0020762&type=m5k&authorityType=fa&cb=jsonp1536580250828
  '''

  








