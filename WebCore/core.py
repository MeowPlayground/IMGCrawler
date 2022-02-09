import requests
import os
from bs4 import BeautifulSoup
from .common import HEADERS, download


class directLinkCore:
    imgList = []
    num = 0
    currentPage = 1
    maxPage = 0
    keyword = ''

    def __init__(self) -> None:
        pass
    
    def setKeyword(self, k):
        self.keyword = k
        
    def _getRequestBs4(self, url, params={}):
        data = requests.get(
            url=url,
            params=params,
            headers=HEADERS
        )
        if data.status_code == 200:
            return self._toHtml(data.text)
        else:
            raise Exception('网络错误码%d' % data.status_code)

    def _toHtml(self, text):
        return BeautifulSoup(text, 'html.parser')

    def _removeSame(self):
        tempList = []
        for id in self.imgList:
            if id not in tempList:
                tempList.append(id)
        self.imgList = tempList[:]

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

    def _addList(self, imgURL, name, _type='png'):
        self.imgList.append({
            "url": imgURL,
            "name": str(name),
            "type": _type
        })
        self.num = self.num + 1

    
    def whileGetUrl(self, func=None):
        '''
        循环页数链接获取主函数\n
        func参数格式\n
        func(currentPage, maxPage)
        '''
        self.currentPage = 1
        while(self._getUrlFormPage()):
            if not func is None:
                func(self.currentPage, self.maxPage)
    
    def _getUrlFormPage():
        '''
        子类中重写该方法
        '''
        return False
    
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
