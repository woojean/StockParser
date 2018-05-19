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
    for bk,url in self._BKs.items():
      path = d + bk
      res = open(path,'r').read()
      l = re.findall('"(.*?)"', res)
      for item in l:
        arr = item.split(',')
        if 'BK' != arr[1][:2]:
          continue

        if not (arr[2] in chooseAbleList): # 不在可选板块列表中
          continue
        
        bkData = (arr[1],arr[2],arr[3])  # 板块编码、板块名称、板块涨幅
        bkList.append(bkData)

    print "\n板块总数："+str(len(bkList))+"\n"
    self.dumpBkDict(bkList)  # 保存文件到本地方便后续生成报告时查询
    bkList = sorted(bkList,key=lambda x: (-float(x[2])if('-'!=x[2])else(0))) # 根据板块涨幅排序
    self.dumpFilteredBkDict(bkList)  # 用于渲染报告的头部
    return bkList


  def getFilteredIdList(self,minBkNum):
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

      # 共振板块数量
      if len(data['bkList']) < minBkNum: 
        continue

      filterdIdList.append((id,data))
    return filterdIdList
  

  def getIdListOfChoosedBkList(self,choosedBkList,resonanceNum):
    bkList = self.getFilteredBkList(choosedBkList)  
    self.genBkStockData(bkList)
    idList = self.getFilteredIdList(resonanceNum) 
    return idList

  def run(self):
    # 确定须排除个股
    # --------------------------------------------------------------------
    # 获取板块数据
    HotPointPredictor().initDir()
    self.genBKdata()

    # 须排除
    excludedIdList = self.getIdListOfChoosedBkList(MUST_NOT_CHOOSE_BK_LIST,LIMIT_OF_EXCLUDED) 
    excludedCodeList = []
    for item in excludedIdList:
      excludedCodeList.append(item[0])
    print '须排除个股数：'+str(len(excludedIdList)) +"\n"


    # 确定初选个股
    # --------------------------------------------------------------------
    HotPointPredictor().initDir()
    self.genBKdata()

    # 选中
    choosedIdList = self.getIdListOfChoosedBkList(CHOOSEABLE_BK_LIST,LIMIT_OF_CHOOSED)
    print '初选中个股数：'+str(len(choosedIdList)) +"\n" 


    # 过滤
    # --------------------------------------------------------------------
    num = 1
    for item in choosedIdList:
      if item[0] in excludedCodeList:
        print '排除：'+str(num)+' '+str(item[0])+" "+item[1]['basicInfo'][2]
        num +=1
        choosedIdList.remove(item)

    print "\n排除后选中个股数："+str(len(choosedIdList)) +"\n" 

    # 生成报告
    self.dumpReport(choosedIdList,LIMIT_OF_CHOOSED)


# config
# ===============================================================
LIMIT_OF_CHOOSED = 2 # Resonance atleast 2
LIMIT_OF_EXCLUDED = 2 # Resonance atleast 2

# 可选板块
CHOOSEABLE_BK_LIST=[
  '可燃冰',
  '文教休闲',
  '油价相关',
  '一带一路',
  '全息技术',
  '央视50_',
  '页岩气',
  '海工装备',
  '长株潭',
  '化工行业',
  '次新股',
  '银行',
  '化纤行业',
  '食品饮料',
  '工程建设',
]

# 必不选板块
MUST_NOT_CHOOSE_BK_LIST=[
  '新能源车',
  '单抗概念',
  '小米概念',
  '万达概念',
  '新零售',
  '养老金',
  '精准医疗',
  '软件服务',
  '医疗行业',
  '高送转',
  '北京东奥',
  '基金重仓',
  'AB股',
  '深证100R',
  '珠宝首饰',
  '虚拟现实',
  '健康中国',
  '航母概念',
  '5G概念',
  '人脑工程',
  '超级电容',
  '免疫治疗',
  '国产软件',
  '基因测序',
  '阿里概念',
  '国企改革',
  '超导概念',
  '独家药品',
  '病毒防治',
  '蓝宝石',
  '医疗器械',
  '国家安防',
  '苹果概念',
  '养老概念',
  '特斯拉',
  '智能穿戴',
  '互联金融',
  '大数据',
  '送转预期',
  '北斗导航',
  '中药',
  '太阳能',
  '触摸屏',
  '稀土永磁',
  '锂电池',
  '移动支付',
  '物联网',
  '生物疫苗',
  '航天航空',
  '保险',
  '医药制造',
  '交运物流',
  '民航机场',
  '西藏板块',
]


if __name__ == '__main__':
  print 'HotPointPredictor'
  sniffer = HotPointPredictor()
  sniffer.run()



