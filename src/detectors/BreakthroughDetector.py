#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-10-04
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers.BaseParser import BaseParser

'''
startDay -leftInterval- peakDay -rightInterval- breakDay

'''
class BreakthroughDetector:
    _parseDay = ''
    _parser = None

    def __init__(self,parseDay): 
        self._parseDay = parseDay
        self._parser = BaseParser(parseDay)


    def dumpReport(self,data):
        s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
        s += '''
<style>
font-size:0.8em;

td{
  font-size:0.8em;
  padding: 6px 6px 6px 12px;
  text-align: center;
  border: 1px solid black;
}

table {
  width: 100%;
  padding-top: 20px;
  padding-bottom: 20px;
  margin-top: 20px;
  margin-bottom: 20px;
  cellspacing="0";
  background: #fff;
  color: #4f6b72;
  text-align: center;
  border: 1px solid gold;
}

v{
	border: 1px solid gold;
}

</style>
'''
        s += '</head><body>'
        table = '<table>'
        tr = '<tr>'
        tr += '<td class="v">代码</td>'
        tr += '<td class="v">名称</td>'
        tr += '<td class="v">开始日期</td>'
        tr += '<td class="v">左区间</td>'
        tr += '<td class="v">最高日</td>'
        tr += '<td class="v">右区间</td>'
        tr += '<td class="v">突破日</td>'
        tr += '<td class="v">总区间</td>'
        tr += '</tr>'
        table += tr

        for item in data: # 按天遍历
            tr = '<tr>'
            tr += '<td>'+str(item['id'])+'</td>'
            tr += '<td>'+str(item['name'])+'</td>'
            tr += '<td>'+str(item['startDay'])+'</td>'
            tr += '<td>'+str(item['leftInterval'])+'</td>'
            tr += '<td>'+str(item['peakDay'])+'</td>'
            tr += '<td>'+str(item['rightInterval'])+'</td>'
            tr += '<td>'+str(item['breakDay'])+'</td>'
            tr += '<td>'+str(int(item['leftInterval']) + int(item['rightInterval']))+'</td>'
            tr += '</tr>'
            table += tr
        
        s += table
        path = Tools.getReportDirPath()+'/breakthrough-detector-report.html'
        open(path,'w').write(s)
        os.system('open '+path)
    

    def parse(self,res,id=''):
    	print id
    	data = {}
        dayList = BaseParser.getPastTradingDayList(self._parseDay,100)

        endPrice = self._parser.getEndPriceOfDay(res,self._parseDay)
        # lastDayMaxPrice = self._parser.getMaxPriceOfDay(res,dayList[-2])
        lastDayEndPrice = self._parser.getMaxPriceOfDay(res,dayList[-2])

        startDay = ''
        peakDay = ''
        leftInterval = 0
        rightInterval = 0
        total = len(dayList)

        # 寻找区间顶
        for i in xrange(3,total-1):  # 从-3开始
            maxPrice = self._parser.getMaxPriceOfDay(res,dayList[-i])
            if maxPrice >= endPrice:  # 最高价已超过当日收盘价，突破已不存在
                break
            if maxPrice > lastDayEndPrice:
                peakDay = dayList[-i] # 区间顶
                rightInterval = i-1
                break
        if '' == peakDay:
            return False

        # 确定左边区间
        peakDayMaxPrice = self._parser.getMaxPriceOfDay(res,peakDay)
        dayList = BaseParser.getPastTradingDayList(peakDay,100)
        total = len(dayList)
        for i in xrange(2,total-1): 
            maxPrice = self._parser.getMaxPriceOfDay(res,dayList[-i])
            if maxPrice > peakDayMaxPrice:
                startDay = dayList[-i]
                leftInterval = i
                break
        if '' == startDay:
        	return False

        if leftInterval < minLeftInterval:
        	return False

        if rightInterval < minRightInterval:
        	return False
        
        data = {
          "id":id,
          "name":Tools.getNameById(id),
          "startDay":startDay,
          "leftInterval":leftInterval,
          "peakDay":peakDay,
          "rightInterval":rightInterval,
          "breakDay":self._parseDay
        }
        return data


    def detect(self):
    	data = []
    	priceFileList = BaseParser.getPriceFileList()
        parsedNum = 0
        priceFileList = BaseParser.getPriceFileList()
        total = len(priceFileList)
        for f in priceFileList:
            try:
                self._parser.printProcess(parsedNum,total)
                id = f[-6:]
                res = open(f,'r').read()
                ret = self.parse(res,id)
                if not ret:
                    continue
                data.append(ret)
                parsedNum += 1
            except Exception, e:
                pass
                print repr(e)
        return data


minLeftInterval = 10
minRightInterval = 10

    

if __name__ == '__main__':
    print 'BreakthroughDetector'

    parseDay = BaseParser.getParseDay()
    print parseDay
  
    detecter = BreakthroughDetector(parseDay)
    data = detecter.detect()
    detecter.dumpReport(data)












