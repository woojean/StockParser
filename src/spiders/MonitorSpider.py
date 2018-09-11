#coding:utf-8
'''
woojean@2018-09-10
'''

import sys
import requests
import time
import re
import datetime
import os

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
    # print url
    return url
  
  def run(self):
    for id in self._idList:
      idType = str(id)[0]
      if idType not in ['6','0','3']: # 只看A股 0 深，6 沪，3 创业板，5 基金权证， 1 深市基金
        continue
      # if idExist(id): # id已存在
      #   print "exists!"
      #   continue
      try:
        url = self.genUrl(id)
        if log:
          print str(self._threadId) + ' ·-> ' +str(id)
        res = requests.get(url,verify=False).text
        # res = ''
        ret = hasSignal(parseTime,id,res)
        if ret: # 发出信号
          dumpId(id)
      except Exception, e:
        pass
        print repr(e)


# 开盘平静判断
def isOpeningPeaceful(id,res,timeList,nowTime):
  data = getTimeData(res,nowTime)
  t1Data = getTimeData(res,timeList[0])
  t2Data = getTimeData(res,timeList[1])
  t3Data = getTimeData(res,timeList[2])
    
  v = int(data[4])
  v1 = int(t1Data[4])
  v2 = int(t2Data[4])
  v3 = int(t3Data[4])
  if v == 0 or v1 == 0 or v2 == 0 or v3 == 0:
    return False
  if v<=v1 or v<=v2 or v<=v3:
    return False
  return True

# 量突变判断
def haveBigVolume(id,res,time1,time2,time3):
  data1 = getTimeData(res,time1)
  data2 = getTimeData(res,time2)
  data3 = getTimeData(res,time3)
  v1 = int(data1[4])
  v2 = int(data2[4])
  v3 = int(data3[4])
  
  # print res

  # 当前量大于前一个量
  if v2 > v3:
    return False

  # 当前量是前前量的5倍以上
  rate = v3/v1
  if rate < 5:
    return False
  return True


# 阳柱判断
def isUpWard(id,res,nowTime):
  data = getTimeData(res,nowTime)
  startPrice = float(data[0])
  endPrice = float(data[1])
  if startPrice == 0 or endPrice == 0:
    return False
  if endPrice <= startPrice:
    return False
  return True


def isInTheRise(id,res,timeList,nowTime):
  data1 = getTimeData(res,timeList[0])
  endPrice1 = float(data1[1])
  data = getTimeData(res,nowTime)
  endPrice = float(data[1])
  return endPrice > endPrice1


def hasSignal(parseTime,id,res):
  timeList = getTimeList(parseTime)

  ret = False
  timeNums = len(timeList)
  for i in xrange(0,timeNums-1): 
    nowTime = timeList[i]
    prevTime = timeList[i-1]
    prevPrevTime = timeList[i-2]
    
    # 开盘走势相对平静
    if not isOpeningPeaceful(id,res,timeList,nowTime):
      if log:
        print "not isOpeningPeaceful"
      continue

    # 爆量
    if not haveBigVolume(id,res,prevPrevTime,prevTime,nowTime):
      if log:
        print "not haveBigVolume"
      continue

    # 阳柱
    if not isUpWard(id,res,nowTime):
      if log:
        print "not isUpWard"
      continue

    # 分时上涨中
    if not isInTheRise(id,res,timeList,nowTime):
      if log:
        print "not isInTheRise"
      continue

    ret = True
    break
  return ret

  


# ===================================================================================
def idExist(id):
  path = Tools.getMonitorDirPath()+'/'+id
  return os.path.exists(path)

def getTimeData(res,time):
  '''
               0      0开    1收    2最高    3最低    4量   5额 
  (u'2018-09-1', u'13:20,3.61,3.61,3.61,3.61,586,211436,0%')
  '''
  p = r'"'+time+',(.*?)",'
  ret = re.findall(p, res)
  return ret[0].split(',')

def dumpId(id):
  print "dumpId:"+str(id)
  monitorDirPath = Tools.getMonitorIdListDirPath()
  #open('data/golden-pin-bottom/'+ confirmDay +'.sel','w').write(','.join(idList))
  open(monitorDirPath + '/' +id,'w').write(id)

def getPrevTime(parseTime):
    prevTime = (datetime.datetime.strptime(parseTime, "%Y-%m-%d %H:%M")-datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')
    return prevTime

def getNextTime(parseTime):
    nextTime = (datetime.datetime.strptime(parseTime, "%Y-%m-%d %H:%M")+datetime.timedelta(minutes=5)).strftime('%Y-%m-%d %H:%M')
    return nextTime


def getTimeList(parseTime):
  date = parseTime[0:10]
  time = date +' 09:35'
  l = []
  while time < parseTime:
    l.append(time)
    time = getNextTime(time)

  # 剔除午间休盘
  time1 = date +' 11:31'
  time2 = date +' 13:04'
  timeList = []
  for t in l:
    if t > time1 and t < time2:
      continue
    timeList.append(t)
  return timeList


def getFilteredIdList(date):
  # http://quote.eastmoney.com/stocklist.html
  fp = Tools.getRootPath()+'/data/enterList/'+date+'-FilterParser.sel'
  f = open(fp,'r')
  data = f.read()
  idList = data.split(',')
  if len(idList) < 1:
    print "\n候选id列表为空！\n"
  return idList


def getPrevTradingDay(today):
  allDayList = Tools.getAllTradeDayList()
  idx = allDayList.index(today)
  allDayList = allDayList[:idx]
  return allDayList[-1]


def printTime(parseTime,filteredDate):
  print "\n================================================\n"
  print "当前时间："+parseTime
  print "过滤文件日期："+filteredDate
  minutes = parseTime[11:]
  if minutes <= '09:35':
    print "开盘时间不够！"
    os._exit()
  if minutes >= '15:30':
    print "已收盘！"
    os._exit()

  minute = parseTime[-1]
  if int(minute) < 5:
    parseTime = parseTime[:-1]+'0'
  if int(minute) > 5:
    parseTime = parseTime[:-1]+'5'
  print "实际解析时间："+ parseTime


'''
python src/Prepare.py
python src/spiders/MonitorSpider.py
python src/tools/MonitorIdList.py

ps -ef |grep python |awk '{print $2}'|xargs kill -9
'''

log = True
if __name__ == '__main__':
  # 取参
  # ============================================================
  Tools.initDir('monitor')
  Tools.initDir('monitor-idList')
  parseTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
  filteredDate = getPrevTradingDay(parseTime[:10])  # 过滤文件
  idList = getFilteredIdList(filteredDate)
  threads = 32 # 线程数（不能少于任务数）
  
  
  # 自定义参数
  # ============================================================ 
  filteredDate = "2018-09-07"  # 过滤文件
  parseTime = "2018-09-10 10:01"  # 自定义时间
  # idList = ['300076'] 
  # threads = 1

  
  # 执行
  # ============================================================
  printTime(parseTime,filteredDate)
  print "\n================================================\n"
  step = len(idList)/threads  # total > threads
  for threadId in xrange(1,threads+1):
    subIdList = idList[((threadId-1)*step):(threadId*step)]
    spider = MonitorSpider(subIdList,threadId)
    spider.start()
  








