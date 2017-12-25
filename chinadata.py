#-*- coding : utf -8 -*-
import pymysql
import re
import requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup

def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='wxy',
        passwd='wxy@2017',
        charset='utf8',
        use_unicode=False
    )
    return conn

pattern2 = re.compile('(id=)\d+')

url2 = "http://www.chinadatatrading.com/trade?bigType=1&smalltype=1"

listurl = "http://www.chinadatatrading.com/tradelistliebiao"
driver = webdriver.PhantomJS(executable_path='/Users/wangxiangyang/phantomjs-2.1.1-macosx/bin/phantomjs')

page = 0
while page < 74:
    page += 1
    payload = {"isFree":1,"dataPattern":0,"dataSource":0,"queryString":"","ishot":1,"isnew":9,"isprice":9,"btype":7,"stype":99,"curr":page}
    reponse = requests.post("http://www.chinadatatrading.com/tradelistliebiao",data=payload)
    datajson = json.loads(reponse.content)
    soup3 = BeautifulSoup(datajson['data'],'lxml')
    id_nums = soup3.find_all('a')
    for id_num in id_nums:
        task_id = pattern2.search(id_num['onclick'])
        #print task_id.group()

        url = "http://www.chinadatatrading.com/trade/detail?" + task_id.group()
        driver.get(url)
        data = driver.page_source
        driver.quit
        soup = BeautifulSoup(data,'lxml')
        title = soup.find('h1','dpart01p').find(text=True).strip()
        #print title
        sum_trade = soup.find("p","dpart_lp").span.find(text=True).strip()
        #print sum_trade
        trade_price2 = soup.find("p","dpart_rp").find_all("span",'dpart_rp_s3')
        trade_price = ''
        for trade_price1 in trade_price2:

            trade_price = trade_price + str(trade_price1.find(text=True).strip())
        #print trade_price
        data_industry = soup.find("div",'dpart02_right').find("h2").find('a').find(text=True).strip()
        #print data_industry
        publish_time = ""
        pv2 = soup.find("div",'dpart02_right').find_all("p","dpart_rp")
        k = 0
        for pv1 in pv2:
            k = k + 1
            if k == 4:
                publish_time = publish_time + pv1.get_text()
            else:
                pass
        #print publish_time
        data_introduce = soup.find("p","dparttabqh01div_p2").find(text=True)
        #print data_introduce
        comment_num = int(soup.find("p","dpar03_p").span.find(text=True))
        #print comment_num
        name_id = unicode(soup.find('div','dpart_right').p.find(text=True))
        #print name_id

        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE chinadata")
        sql = 'insert into music(title,sum_trade,trade_price,data_industry,publish_time,data_introduce,comment_num,name_id) values (%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (title,sum_trade,trade_price,data_industry,publish_time,data_introduce,comment_num,name_id))
            dbObject.commit()
        except Exception, e:
            print (">>>>>>>>>>", e, "<<<<<<<<<<<<<<<<<<")
            dbObject.rollback()
