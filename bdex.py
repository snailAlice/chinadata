#-*- coding : utf -8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import pymysql

def dbHandle():
    conn = pymysql.connect(
        host='localhost',
        user='wxy',
        passwd='wxy@2017',
        charset='utf8',
        use_unicode=False
    )
    return conn

page = 0
while page<1:
    page += 1
    payload = {'paramJson': {"areaId":"0","areaSubId":"0","proFileType":"0","proFree":"1","proSort":"0","proType":"3","proSubType":"0","keyword":""} ,'pageSize':20,'currentPage':str(page)}
    reponse = requests.post("http://www.bigdatahd.com/product/ajaxList",data=payload)

    urlpre = "http://www.bigdatahd.com/product/detail/"

    data = json.loads(reponse.content)
    p = re.compile('<[^>]+>')

    #print (data['resultList'])
    for data3 in data['resultList']:
        data_scale = data3['data_scale']
        star_level = data3['star_level']
        institution = data3['institution']
        introduce = p.sub("",data3['introduce'])
        url = urlpre + str(data3['id']) + "/0"

        rep2 = requests.get(url)
        soup = BeautifulSoup(rep2.content,'lxml')
        title = soup.find('h1').find(text=True)
        body = soup.find_all('dl','pro-info')
        deal2 = soup.find('div','pro-dec').find('div','qj-det-pic t2').find('div','shu-ju').find_all('span')
        deal_num = ''
        h = 0
        for deal1 in deal2:
            h = h + 1
            if h == 2:
                 deal_num = deal_num + deal1.find(text=True)

            else:
                pass
        #print deal


        comments_num2 = soup.find_all('div','pl')
        for comments_num1 in comments_num2:
            pass
        comments_num = comments_num1.find(text=True)
        file_type = ''
        price = ''
        service_merchant = ''
        date_time = ''
        for content1 in body:
            content2 = content1.find_all('dd')
            j = 0
            for content3 in content2:
                j = j + 1
                if j == 1:
                    file_type2 = content3.find_all(text=True)
                    k = 0
                    for file_type1 in file_type2:
                        k = k + 1
                        if k > 1:
                            file_type = file_type + file_type1.strip()
                        else:
                            pass
                elif j == 3:
                    price2 = content3.find_all(text=True)
                    k = 0
                    for price1 in price2:
                        # print (file_type1.strip())
                        k = k + 1
                        if k > 1:
                            price = price + price1.strip()
                        else:
                            pass
                elif j == 4:
                    date_time2 = content3.find_all(text=True)
                    for date_time1 in date_time2:
                        date_time = date_time + date_time1
                else:
                    pass



        #print (title)
        #print (star_level)
        #print (file_type)
        #print (data_scale)
        #print (price)
        #print (date_time)
        #print (institution)
        #print (introduce)
        #print (comments_num)
        #print ("====================================")

        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE bdex")
        sql = 'insert into bdex_policy_tab(title,star_level,deal_num,file_type,data_scale,price,date_time,institution,introduce,comments_num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (title, star_level, deal_num,file_type, data_scale, price,date_time, institution,introduce,comments_num))
            dbObject.commit()
        except Exception, e:
            print (">>>>>>>>>>", e, "<<<<<<<<<<<<<<<<<<")
            dbObject.rollback()









