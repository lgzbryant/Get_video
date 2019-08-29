# -*-coding:utf-8-*-

from bs4 import BeautifulSoup
import lxml
import Queue
import requests
import re, os, sys,random
import threading
import logging
import json, hashlib, urllib
from requests.exceptions import ConnectTimeout,ConnectionError,ReadTimeout,SSLError,MissingSchema,ChunkedEncodingError
import random

reload(sys)
sys.setdefaultencoding('gbk')

# 日志模块
logger = logging.getLogger("AppName")
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

q = Queue.Queue()   # url队列
page_q = Queue.Queue()  # 页面
vurls = []

def get_page(keyword,page_q):
    while True:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }
        page = page_q.get()
        url = "https://www.youtube.com/results?search_query=" + keyword + "&page=" + str(page)
        try:
            html = requests.get(url, headers=headers).text
        except (ConnectTimeout,ConnectionError):
            print u"不能访问youtube 检查是否已翻墙"
            os._exit(0)
        reg = re.compile(r'"url":"/watch\?v=(.*?)","webPageType"', re.S)
        result = reg.findall(html)
        logger.info(u"第 %s 页" % page)
        for x in result:
            vurl = "https://www.youtube.com/watch?v=" + x

            try:
                res = requests.get(vurl).text
            except (ConnectionError, ChunkedEncodingError):
                logger.info(u"网络不稳定 正在重试")
                try:
                    res = requests.get(vurl).text
                except SSLError:
                    continue
            reg2 = re.compile(r"<title>(.*?)YouTube",re.S)
            name = reg2.findall(res)[0].replace("-","")
            # print name
            if u'\u4e00' <= keyword <= u'\u9fff':
                q.put([vurl, name])
                vurls.append(vurl)
            else:
                # 调用金山词霸
                logger.info(u"正在翻译")
                url_js = "http://www.iciba.com/" + name
                html2 = requests.get(url_js).text
                soup = BeautifulSoup(html2, "lxml")
                try:
                    res2 = soup.select('.clearfix')[0].get_text()
                    title = res2.split("\n")[2]
                except IndexError:
                    title = u'IndexError %s' % random.randint(1, 9999)
                q.put([vurl, title])
                vurls.append(vurl)
                # print vurl, title

        page_q.task_done()


def down_video(start_index, end_index, path):
    down_range = vurls[start_index:end_index]
    for each_url in down_range:
        os.system('you-get -o %s  %s' % (path, each_url))

'''

bloodymoment
Bloodyselfabuse  
selfharm 
Another Top 10 MOST VIOLENT Video Games
VIOLENT


'''
def main():

    keyword = (u"血腥片段集合").decode("gbk")
    threads = int(5)


    # 判断目录
    path = 'D:\multi_download_youtu_videos\%s' % keyword
    if os.path.exists(path) == False:
        os.makedirs(path)


    # 解析网页
    logger.info(u"开始解析网页")
    for page in range(1, 6):
        page_q.put(page)
    for y in range(threads):
        t = threading.Thread(target=get_page, args=(keyword, page_q))
        t.setDaemon(True)
        t.start()
    page_q.join()
    logger.info(u"共 %s 视频" % q.qsize())

    total = len(vurls)
    each_number = total/threads

    start_index = []
    end_index = []

    for i in range(threads):
        index1 = 0 + i * each_number
        index2 = 0 + (i + 1) * each_number
        start_index.append(index1)
        end_index.append(index2)

    logger.info(u"开始下载视频")
    for i in range(threads):
        t = threading.Thread(target=down_video, args=(start_index[i], end_index[i], path))
        t.setDaemon(True)
        t.start()
    q.join()
    logger.info(u"全部视频下载完成！")

    # 多线程下载
    # logger.info(u"开始下载视频")
    # for x in range(threads):
    #     t = threading.Thread(target=downlaod,args=(q,x,path))
    #     t.setDaemon(True)
    #     t.start()
    # q.join()
    # logger.info(u"全部视频下载完成！")

main()