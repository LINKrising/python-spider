# -*- coding: utf-8 -*-
from selenium import webdriver
import io
import time
from bs4 import BeautifulSoup
import os
import lxml
import xlwt
from datetime import datetime
from makeExcel import write_excel
# 封装p

# selenium>webdriver.chrome->获取完整网页
# io->爬取数据写入
# time->定时爬取+文件名字
# BeautifulSoup+lxml->网页解析
# xlwt->excel操作

def p(arg):
    print(arg)


class Crawl():
    # 初始化,数据容器
    bigContainer = []
    # 初始化,构造容器

    def __init__(self, url):
        self.url = url
        self.forpage()

    # 循环分页url函数
    def forpage(self):
        urlList = [self.url, ]
        # 循环生成分页url
        for page in range(2, 36):
            urlList.append(
                f'http://piao.qunar.com/ticket/list.htm?from=mpshouye_hotdest_more&keyword=%E5%9B%9B%E5%B7%9D&page={page}&sort=pd')
        p(urlList)
        self.crawl(urlList)
    # 循环分页url函数

    # 调动webdiver,进行js完整解析,返回浏览器解析好的静态化页面,并写入html,sleep定时24小时爬取一次数据
    def crawl(self, urlList):

        while True:
            for url in urlList:
                htmlName = time.time()
                p(url)
                browser = webdriver.Chrome()
                browser.get(url)
                html = browser.page_source.encode('utf-8')
                browser.close()
                self.crawl_data(html)
                # p(browser.page_source)
                fp = open(f'html_file/{htmlName}.html', 'wb')
                fp.write(html)
                fp.close()
            time.sleep(86400)
    # 调动webdiver,进行js完整解析,返回浏览器解析好的静态化页面,并写入html,sleep定时24小时爬取一次数据

    # 分析seletor
    #     title
    #         search-list > div > div > div.sight_item_about > h3 > a  ->第一页
    #         search-list > div > div > div.sight_item_about > h3 > a  ->第二页
    #         search-list > div > div > div.sight_item_about > h3 > a  ->第三页
    #     level
    #         search-list > div:nth-child(1) > div > div.sight_item_about > div > div.clrfix > div > span.product_star_level > em > span  ->第一页
    #         search-list > div:nth-child(1) > div > div.sight_item_about > div > div.clrfix > div > span.product_star_level > em > span ->第二页
    #         search-list > div:nth-child(1) > div > div.sight_item_about > div > div.clrfix > div > span.product_star_level > em > span ->第三页
    #     area
    #         search-list > div > div > div.sight_item_about > div > div.clrfix > span.area > a  ->第一页
    #         search-list > div > div > div.sight_item_about > div > div.clrfix > span.area > a ->第二页
    #         search-list > div > div > div.sight_item_about > div > div.clrfix > span.area > a  ->第三页
    #     prices
    #         #search-list > div:nth-child(1) > div > div.sight_item_pop > table > tbody > tr:nth-child(1) > td > span > em  ->第一页
    #         search-list > div:nth-child(3) > div > div.sight_item_pop > table > tbody > tr:nth-child(1) > td > span > em
    #         #search-list > div:nth-child(1) > div > div.sight_item_pop > table > tbody > tr:nth-child(1) > td > span > em ->第二页
    #         #search-list > div:nth-child(1) > div > div.sight_item_pop > table > tbody > tr:nth-child(1) > td > span > em  ->第三页
    # 结论:dom结构稳定,较好爬取
    # http: // piao.qunar.com/ticket/list.htm?from = mpshouye_hotdest_more & keyword = %E5 % 9B % 9B % E5 % B7 % 9D & page = 1 & sort = pd
    # http: // piao.qunar.com/ticket/list.htm?from = mpshouye_hotdest_more & keyword = %E5 % 9B % 9B % E5 % B7 % 9D & page = 2 & sort = pd
    # 分页url分析page参数为分页参数

# 分别爬取数据

    def crawl_data(self, html):
        # p(html)
        soup = BeautifulSoup(html, 'lxml')
        # 标题数据

        title_data = soup.select(
            '#search-list > div > div > div.sight_item_about > h3 > a')
        # 标题数据

        # level
        level_data = soup.select(
            '#search-list > div > div > div.sight_item_about > div > div.clrfix > div > span.product_star_level > em > span')

        # level

        # area
        area_data = soup.select(
            '#search-list > div > div > div.sight_item_about > div > div.clrfix > span.area > a')

        # area

        # price
        # for nums in range(1,16):
        #     try :
        #         price_data = soup.select(
        #             f'#search-list > div:nth-of-type({nums}) > div > div.sight_item_pop > table > tbody > tr:nth-of-type(1) > td')
        #     except AttributeError:
        #         new_tag = soup.new_tag("span")
        #         soup.select(
        #             '#search-list > div > div > div.sight_item_pop > table > tbody > tr:nth-of-type(1) > td').append(new_tag)
        #         new_tag.string = "未知"
        #         p(price_data)
        price_data = soup.select(
            '#search-list > div > div > div.sight_item_pop > table > tbody > tr:nth-of-type(1) > td > span > em')
        # sold_num
        sold_data = soup.select(
            '#search-list > div > div > div.sight_item_pop > table > tbody > tr:nth-of-type(4) > td > span')

        for item in range(len(sold_data)):
            container = []
            container = [title_data[item].text, level_data[item].text[2:], area_data[item].text,
                         price_data[item].text, sold_data[item].text]
            self.bigContainer.append(container)

        mydata = self.bigContainer
        write_excel(mydata)
        # print('创建data.xlsx文件成功')


if __name__ == "__main__":
    myCrawl = Crawl(
        "http://piao.qunar.com/ticket/list.htm?from=mpshouye_hotdest_more&keyword=%E5%9B%9B%E5%B7%9D&page=1&sort=pd")
