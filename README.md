一些股票分析脚本，先运行爬虫抓取数据（东方财富接口），再运行各种Parser生成特定指标的选股结果：
![image](https://github.com/woojean/StockParser/blob/master/imgs/report.png)


python src/spiders/PriceSpider.py
python src/spiders/MacdSpider.py
python src/spiders/BasicInfoSpider.py

python src/Do.py 2018-03-07
python src/dumpers/XueqiuDumper.py 2018-03-07

