#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-03
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
from operator import itemgetter 
from BaseHotPoint import BaseHotPoint

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools

'''
根据指定的板块集合预测个股
'''


class HotPointPredictor(BaseHotPoint): 
  _source = 'hot-point-predictor'
  def __init__(self): 
    self._dataPath = self._source
    self._failedDataPath = 'failed_' + self._source
  

  def getFilteredBkList(self,chooseAbleList):
    print 'getFilteredBkList...'
    d = self.getRootPath()+'/data/'+self._dataPath+'/'
    bkList = []
    predictBkList = []
    for bk,url in self._BKs.items():
      path = d + bk
      res = open(path,'r').read()
      l = re.findall('"(.*?)"', res)
      for item in l:
        arr = item.split(',')
        '''
        ['1', 'BK0458', '\xe4\xbb\xaa\xe5\x99\xa8\xe4\xbb\xaa\xe8\xa1\xa8', '1.95', '268981406042', '1.27', '38|2|3|2', '300007', '2', '\xe6\xb1\x89\xe5\xa8\x81\xe7\xa7\x91\xe6\x8a\x80', '15.97', '9.99', '300515', '2', '\xe4\xb8\x89\xe5\xbe\xb7\xe7\xa7\x91\xe6\x8a\x80', '11.00', '-2.65', '2', '7671.56', '146.92']
        '''
        if 'BK' != arr[1][:2]:
          continue

        if not (arr[2] in chooseAbleList): # 不在可选板块列表中
          continue
        
        bkData = (arr[1],arr[2],arr[3])  # 板块编码、板块名称、板块涨幅
        bkList.append(bkData)
    length = len(bkList)
    print "\n板块总数："+str(length)+"\n"
    self.dumpBkDict(bkList)  # 保存文件到本地方便后续查询
    bkList = sorted(bkList,key=lambda x: (-float(x[2])if('-'!=x[2])else(0)))
    predictBkList = bkList
    self.dumpFilteredBkDict(predictBkList)
    return predictBkList


  def getFilteredIdList(self,minBkNum=2):
    print 'getFilteredIdList...'
    count = {}
    d = self.getRootPath()+'/data/'+self._dataPath+'/'
    for root,dirs,files in os.walk(d):
      for f in files:
        try:
          if 'BK'== f[:2]:
            path = root + f
            res = open(path,'r').read()
            l = re.findall('"(.*?)"', res)
            for item in l:
              '''
              2018-05-03 
              2,002681,奋达科技,9.41,0.86,10.06%,9.71,165823,153715449,8.55,8.59,9.41,8.58,-,-,-,-,-,-,-,-,0.00%,2.99,2.28,64.40,2012-06-05
              
              1 代码  2 名称  3 价格  4 价格增长  5 涨幅  6 振幅  23 换手率
              '''
              arr = item.split(',')
              id = arr[1]

              # 统计个股的板块数
              if 6 == len(id):
                if count.has_key(id):
                  count[id]['bkList'].append(f)
                else:
                  count[id] = {}
                  count[id]['basicInfo'] = arr
                  count[id]['bkList'] = [f]
        except Exception, e:
          pass
          print repr(e)

    # 筛选
    filterdIdList = []
    for id,data in count.items():

      # 共振看涨板块数量
      if len(data['bkList']) < minBkNum: 
        continue

      # 不属于看跌板块


      filterdIdList.append((id,data))
    return filterdIdList
  

  def getIdListOfChoosedBkList(self,choosedBkList,resonanceNum=1):
    bkList = self.getFilteredBkList(choosedBkList)  
    self.genBkStockData(bkList)
    idList = self.getFilteredIdList(RESONANCE_NUM) 
    return idList

  def run(self):
    # 确定须排除个股
    # --------------------------------------------------------------------
    # 获取板块数据
    HotPointPredictor().initDir()
    self.genBKdata()

    # 须排除
    excludedIdList = self.getIdListOfChoosedBkList(MUST_NOT_CHOOSE_BK_LIST) 
    excludedCodeList = []
    for item in excludedIdList:
      excludedCodeList.append(item[0])
    print '须排除个股数：'+str(len(excludedIdList)) +"\n"

    # 确定初选个股
    # --------------------------------------------------------------------
    HotPointPredictor().initDir()
    self.genBKdata()

    # 选中
    choosedIdList = self.getIdListOfChoosedBkList(CHOOSEABLE_BK_LIST,RESONANCE_NUM)
    print '初选中个股数：'+str(len(choosedIdList)) +"\n" 


    # 过滤
    # --------------------------------------------------------------------
    idList = []
    # 过滤
    for item in choosedIdList:
      if not(item[0] in excludedCodeList):
        idList.append(item)

    print '排除后选中个股数：'+str(len(idList)) +"\n" 

    # 生成报告
    self.dumpReport(idList,RESONANCE_NUM)


# config
# ===============================================================
RESONANCE_NUM = 2 # Resonance atleast 2

# 可选板块
CHOOSEABLE_BK_LIST=[
  '二胎概念',
  '在线教育',
  '生态农业',
  '化工原料',
  '塑胶制品',
  '农药兽药',
  '网络安全',
  '甘肃板块',
  '新疆板块',
  '参股360',
  '网红直播',
  '化肥行业',
  '农牧饲鱼',
  '可燃冰',
  '页岩气',
  '油气设服',
  '油改概念',
  '海南板块',
  '次新股',
  '化纤行业',
  '石油行业',
  '昨日涨停',
  '昨日连板',
]

# 必不选板块
MUST_NOT_CHOOSE_BK_LIST=[
  '苹果概念',
  'OLED',
  '基因测序',
  '央视50_',
  '融资融券',
  '深证100R',
  '福建板块',
  '江西板块',
  '机构重仓',
  '健康中国',
  '转债标的',
  '珠宝首饰',
  '通讯行业',
  '万达概念',
  'QFII重仓',
  '阿里概念',
  '病毒防治',
  '医疗器械',
  '免疫治疗',
  '专用设备',
  '医药制造',
  '酿酒行业',
  '单抗概念',
  '精准医疗',
  '医疗行业',
  '北京东奥',
  '民航机场',
  '生物疫苗',
  '新零售',
  '基金重仓',
  '中超概念',
  '中药',
  '西藏板块',
  '银行',
  '木业家具',
  '特斯拉',
  '独家药品',
  '超级品牌',
  '人脑工程',
]


if __name__ == '__main__':
  print 'HotPointPredictor'
  sniffer = HotPointPredictor()
  sniffer.run()



