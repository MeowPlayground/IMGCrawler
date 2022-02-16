import requests
import os
from bs4 import BeautifulSoup
from .common import HEADERS
from threading import Thread
import time

class DirectLinkCore:
    name = ''
    imgList = []
    num = 0
    currentPage = 0
    currentNum = 0
    maxPage = 0
    keyword = ''


    def __init__(self) -> None:
        pass

    def setKeyword(self, k):
        self.keyword = k
    def setName(self, name):
        self.name = name
    def _getRequestBs4(self, url, params=None):
        data = requests.get(
            url=url,
            params=params,
            headers=HEADERS,
            timeout=(5, 20)
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
        self.num = len(self.imgList)

    def getMaxPage(self):
        """返回最大页数"""
        return self.maxPage

    def getNum(self):
        """返回链接数"""
        return self.num

    def clearList(self):
        """清空list列表"""
        self.imgList = []
        self.maxPage = 0
        self.num = 0

    def _addList(self, imgURL, name, _type='png'):
        self.imgList.append({
            "url": imgURL,
            "name": str(name),
            "type": _type
        })
        self.num = self.num + 1

    def whileGetUrl(self, func=None):
        """
        循环页数链接获取主函数\n
        func参数格式\n
        func(currentPage, maxPage)
        """
        self.currentPage = 0
        while self._getUrlFormPage():
            if not func is None:
                func(self.currentPage)
        func(self.currentPage)

    def _getUrlFormPage(self):
        """
        子类中重写该方法
        """
        return False
        
    def _3threadDownload(self, th, _download, path):
        """
        该函数将作为1个单独的线程运行
        """
        for i in range(th, self.num, 3):
            name = self.imgList[i]['name']
            ntype = self.imgList[i]['type']
            targetPath = os.path.join(path, name + '.' + ntype)
            if os.path.exists(targetPath):
                q = 1
                while os.path.exists(os.path.join(path, name + '_' + str(q) + '.' + ntype)):
                    q = q + 1
                targetPath = os.path.join(
                    path, name + '_' + str(q) + '.' + ntype)
            if _download(self.imgList[i]['url'], targetPath, self.name, self.currentNum ,self._currentPass) == -1:
                return
            
    def _currentPass(self):
        self.currentNum = self.currentNum + 1

    def save(self, path, eList, _download):
        """
        console方式保存 单线程 显示进度条\n
        path 保存的地址\n
        """
        # 搜索线程已退出
        eList[0] = 0
        t_list = []
        for j in range(3):
            t = Thread(target=self._3threadDownload, args=(j, _download, path))
            t.setDaemon(True)
            t.start()
            t_list.append(t)

        eList[1] = 3
        for i in t_list:
            while(i.is_alive()):
                time.sleep(1)

        # 三个下载线程
        
        