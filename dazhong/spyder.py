#!/usr/bin/env python  
# encoding: utf-8  

import codecs
import csv
import requests
from pyquery import PyQuery as pq
import random
import time


headers = {
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'Accept-Encoding': 'gzip',
}

proxy_ip_list = []
with codecs.open("data/proxy_ip.txt", "r", "utf-8") as fr:
    for line in fr.readlines():
        line = line.strip()
        proxy_ip_list.append({"http": line})

#随机获取代理IP
def proxy_random():
    global proxy_ip_list
    index = random.randint(0, len(proxy_ip_list) - 1)
    return proxy_ip_list[index]


#从大众上获取点评数据
def spiderDazhong(ID):
    try:
        time.sleep(random.uniform(5,10))#防止访问太频繁
        html = requests.get("http://www.dianping.com/shop/%s/review_all"%(ID), headers=headers)
        doc = pq(html.text)
        if doc:
            # 存入csv文件
            out = codecs.open('./data/Stu_csv.csv', 'a', encoding="gbk")
            # 设定写入模式
            csv_write = csv.writer(out, dialect='excel')
            shopName = doc("div.review-list-header > h1 > a").text()
            shopurl = "http://www.dianping.com"+doc("div.review-list-header > h1 > a").attr("href")
            csv_write.writerow(["店铺名称","店铺网址"])
            csv_write.writerow([shopName,shopurl])
            csv_write.writerow(["用户名", "用户ID链接", "评定星级", "评论描述", "评论详情", "评论时间", "评论商铺", "评论图片"])
            # 解析评论
            pinglunLi = doc("div.reviews-items > ul > li").items()
            for data in pinglunLi:
                userName = data("div.main-review > div.dper-info > a").text()
                userID = "http://www.dianping.com"+data("div.main-review > div.dper-info > a").attr("href")
                startShop = str(data("div.review-rank > span").attr("class")).split(" ")[1].replace("sml-str","")
                describeShop = data("div.review-rank > span.score").text()
                pinglunShop = data("div > div.review-words").text().replace("收起评论","").replace(" ","").replace("\n","")
                timeShop = data("div.main-review > div.misc-info.clearfix > span.time").text()
                Shop = data("div.main-review > div.misc-info.clearfix > span.shop").text()
                imgShop = data("div > div.review-pictures > ul > li> a").items()
                imgList = []
                for img in imgShop:
                    imgList.append("http://www.dianping.com"+img.attr("href"))

                # 写入具体内容
                csv_write.writerow([userName,userID,startShop,describeShop,pinglunShop,timeShop,Shop,imgList])
                print("successful insert csv!")

    except Exception as e:
        print("error",str(e))


if __name__ == '__main__':
     # 代表各大商铺ID，可通过商铺列表页回去
    listShop = ["2972056"]
    for shop in listShop:
        spiderDazhong(shop)