import functools
from pydoc import getpager
from bs4 import BeautifulSoup
import requests
import time
import os
from .common import HEARDERS
import re
import math


def toHtml(text):
    return BeautifulSoup(text, 'html.parser')


def getRequestBs4(url, params):
    data = requests.get(
        url=url,
        params=params,
        headers=HEARDERS
    )
    if data.status_code == 200:
        return toHtml(data.text)
    else:
        raise Exception('错误，网络错误码%d', data.status_code)


class directLinkCore:
    imgList = []
    num = 0
    currentPage = 1
    maxPage = 0

    def __init__(self) -> None:
        pass

    def getMaxPage(self):
        '''返回最大页数'''
        return self.maxPage

    def getNum(self):
        '''返回链接数'''
        return self.num

    def clearList(self):
        '''清空list列表'''
        self.imgList = []
        self.num = 0

    def _addList(self, imgURL, name, type='png'):
        self.imgList.append({
            "url": imgURL,
            "name": str(name),
            "type": type
        })
        self.num = self.num + 1

    def save(self, path, over_save=False):
        '''
        console方式保存 单线程 显示进度条\n
        path 保存的地址\n
        over_save=False 如果存在文件 是否覆盖
        '''
        if over_save:
            for i in range(self.num):
                download(
                    self.imgList[i]['url'],
                    os.path.join(
                        path, self.imgList[i]['name'] + '.' + self.imgList[i]['type'])
                )
        else:
            for i in range(self.num):
                name = self.imgList[i]['name']
                ntype = self.imgList[i]['type']
                targePath = os.path.join(path, name + '.' + ntype)
                if os.path.exists(targePath):
                    q = 1
                    while(os.path.exists(os.path.join(path, name + '_' + str(q) + '.' + ntype))):
                        q = q + 1
                    targePath = os.path.join(
                        path, name + '_' + str(q) + '.' + ntype)
                download(
                    self.imgList[i]['url'],
                    targePath
                )


class AlphacodersPage(directLinkCore):
    searchURL = 'https://wall.alphacoders.com/search.php'

    def __init__(self, keyWord) -> None:
        self.keyWord = keyWord
        self._getPageMax()

    def _getPageMax(self):
        html = getRequestBs4(url=self.searchURL, params={
                             "search": self.keyWord})
        num = html.find('h1', {"class": "center title"})
        for i in num.text.split(' '):
            if i.isnumeric():
                self.maxPage = (math.ceil(int(i) / 30))

    def _getUrl(self):
        html = getRequestBs4(url=self.searchURL, params={
                             "search": self.keyWord, "page": self.currentPage, "quickload": self.currentPage})
        self.currentPage = self.currentPage + 1
        spanList = html.find_all('span', {"title": "Download Wallpaper"})
        for i in spanList:
            self._addList(
                "https://initiate.alphacoders.com/download/wallpaper/%s/%s/%s/"
                % (str(i['data-id']), i['data-server'], i['data-type']), i['data-id'], i['data-type']
            )
        return self.currentPage <= self.maxPage

    def whileGetUrl(self, func=None):
        '''
        循环页数链接获取主函数\n
        func参数格式\n
        func(currentPage, maxPage)
        '''
        self.currentPage = 1
        while(self._getUrl()):
            if not func is None:
                func(self.currentPage, self.maxPage)


def download(url, path):
    """ 带进度条的下载函数 """
    start = time.time()  # 下载开始时间
    response = requests.get(url, stream=True, headers={
                            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})  # stream=True必须写上
    print(response.status_code)
    size = 0  # 初始化已下载大小
    chunk_size = 1024  # 每次下载的数据大小
    content_size = int(response.headers['content-length'])  # 下载文件总大小
    try:
        if response.status_code == 200:  # 判断是否响应成功
            print('[File size]:%.2f MB' %
                  (content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
            filepath = path
            with open(filepath, 'wb') as file:  # 显示进度条
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    print('\r'+'[下载进度]:%s%.2f%%' % ('>'*int(size*50 /
                          content_size), float(size / content_size * 100)), end=' ')
        end = time.time()  # 下载结束时间
        print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
    except:
        print("Exception occurs in Downloading...")
