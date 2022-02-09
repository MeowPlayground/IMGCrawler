from typing import final
from sites import BilibiliPage, AlphacodersPage
from threading import Thread
from PyQt5.QtWidgets import QWidget, QCheckBox, QFileDialog, QLabel, QProgressBar, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from .common import *
import requests
import os


def _addTread(func, args=()):
    t = Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


class Action:
    def __init__(self, signal: pyqtSignal, ui: QWidget) -> None:
        self.progressBarList = []
        self.checkBoxList = []
        self.engineNameList = []
        self.engineList = [
            BilibiliPage(),
            AlphacodersPage()
        ]
        self.ms = signal
        self.ui = ui.ui
        self.savepath = ''
        self.stopFlag = False

    def _checkBox_setChecked(self, n, v):
        self.ms.engine_setChecked.emit(n, v)

    def progressBar_setHide(self, n, v):
        if v:
            self.progressBarList[n]['label'].hide()
            self.progressBarList[n]['progressBar'].hide()
        else:
            self.progressBarList[n]['label'].show()
            self.progressBarList[n]['progressBar'].show()

    def progressBarReset(self, i):
        self.ms.progressBar_setRange.emit(i, 0, 0)
        self.ms.progressBar_setValue.emit(i, 0)

    def _start_mode(self):
        self.ms.engine_enable.emit(False)
        self.ms.button_set.emit(SEARCH_DISABLE)
        self.ms.button_set.emit(START_DISABLE)
        self.ms.button_set.emit(STOP_ENABLE)
        self.ms.button_set.emit(SAVE_DISABLE)

    def _stop_mode(self):
        self.ms.engine_enable.emit(True)
        self.ms.button_set.emit(SEARCH_ENABLE)
        self.ms.button_set.emit(START_DISABLE)
        self.ms.button_set.emit(STOP_DISABLE)
        self.ms.button_set.emit(SAVE_ENABLE)

    def _searching_mode(self):
        self.ms.engine_enable.emit(False)
        self.ms.button_set.emit(SEARCH_DISABLE)
        self.ms.button_set.emit(START_DISABLE)
        self.ms.button_set.emit(STOP_DISABLE)

    def _searching_OK_mode(self):
        self.ms.engine_enable.emit(True)
        self.ms.button_set.emit(SEARCH_ENABLE)
        self.ms.button_set.emit(START_ENABLE)
        self.ms.button_set.emit(STOP_ENABLE)
        self.ms.button_set.emit(SAVE_ENABLE)

    def _print(self, t):
        self.ms.print.emit(t)

    def _search_thread(self):
        self._searching_mode()
        for i in range(len(self.engineList)):
            engine = self.engineList[i]
            engine.clearList()
            if self.checkBoxList[i].isChecked():
                try:
                    engine.setKeyword(self.keyword)
                    engine.getPageMax()
                    if engine.getMaxPage() > 0:
                        self._print('关键词%s,初始化%s成功,得到页数%d' % (
                            self.keyword, engine.name, engine.getMaxPage()))
                    else:
                        self._checkBox_setChecked(i, False)
                        self.ms.progressBar_setHide.emit(i, True)
                        self._print('关键词%s,初始化%s失败,页数为0' %
                                    (self.keyword, engine.name))
                except Exception as e:
                    self._print('关键词%s,初始化%s失败,%s' %
                                (self.keyword, engine.name, str(e)))
                    self.ms.progressBar_setHide.emit(i, True)
                    self._checkBox_setChecked(i, False)
        self._searching_OK_mode()

    def init_engine(self):
        for i in self.engineList:
            self.engineNameList.append(i.name)
            self.checkBoxList.append(
                QCheckBox(i.name, objectName=i.name, checked=True))
            self.progressBarList.append({
                "label": QLabel(i.name),
                "progressBar": QProgressBar()
            })

        for i in self.checkBoxList:
            self.ui.engineLayout.addWidget(i)

        for i in self.progressBarList:
            progressLayout = QHBoxLayout()
            progressLayout.addWidget(i['label'])
            progressLayout.addWidget(i['progressBar'])
            self.ui.formLayout.addLayout(
                progressLayout
            )

    def search(self):
        self.engineEnableCount = 0
        self.keyword = self.ui.keywordLine.text()
        _addTread(self._search_thread)

    def setSavepath(self):
        self.savepath = QFileDialog.getExistingDirectory()
        self.ui.savepathLine.setText(self.savepath)

    def _start_thread_(self, i):
        path = os.path.join(self.savepath, self.keyword +
                            '-' + self.engineList[i].name)
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            k = 1
            while os.path.exists(os.path.join(self.savepath, self.keyword + '-' + self.engineList[i].name) + '_' + str(k)):
                k = k + 1
            path = os.path.join(self.savepath, self.keyword +
                                '-' + self.engineList[i].name + '_' + str(k))
            os.makedirs(path)

        self._print('创建目录%s' % path)

        def _func_whileGetUrl(current):
            if self.stopFlag:
                self._stop_mode()
                self.progressBarReset()
                raise Exception("%s强制停止!" % self.engineList[i].name)
            self.ms.progressBar_setValue.emit(i, current)
        self.ms.progressBar_setRange.emit(
            i, 0, self.engineList[i].getMaxPage())
        try:
            self.engineList[i].whileGetUrl(_func_whileGetUrl)
        except Exception as e:
            self._print(self.engineList[i].name + '---' + str(e))
            self._print("引擎%s链接爬取失败" %
                    (self.engineList[i].name))
            self.progressBarReset(i)
            self._stop_mode()
            return

        self.ms.progressBar_setValue.emit(i, self.engineList[i].getMaxPage())
        self._print("引擎%s链接爬取已结束,获得链接%d" %
                    (self.engineList[i].name, self.engineList[i].num))
        self.ms.progressBar_setRange.emit(
            i, 0, self.engineList[i].num)
        try:
            self.engineList[i].save(path, self._download)
        except Exception as e:
            self._print(str(e))

    def _start_(self):
        
        if self.savepath == '' or self.savepath is None or (not os.path.exists(self.savepath)):
            self._print('地址%s不存在' % self.savepath)
            self._searching_OK_mode()
            return
        
        for i in range(len(self.engineList)):
            if self.engineList[i].getMaxPage() > 0:
                _addTread(self._start_thread_, args=(i,))
                self._print("引擎%s已激活" % self.engineList[i].name)
                
            else:
                self._print("引擎%s未激活" % self.engineList[i].name)
                self.engineEnableCount = self.engineEnableCount + 1
                
            if self.engineEnableCount > len(self.engineNameList):
                self._print("没有任务")
                self._stop_mode()

    def progressShow(self, c):
        index = self.engineNameList.index(c.objectName())
        self.ms.progressBar_setHide.emit(index, not c.isChecked())
        self.ms.button_set.emit(START_DISABLE)

    def progressBar_setRange(self, i, a, b):
        self.progressBarList[i]['progressBar'].setRange(a, b)

    def progressBar_setValue(self, i, n):
        self.progressBarList[i]['progressBar'].setValue(n)

    def start(self):
        self._start_mode()
        self.stopFlag = False
        self._start_()

    def stop(self):
        self.stopFlag = True

    
    def _download(self, url, path, count, name):
        count[0] = count[0] + 1
        self.ms.progressBar_setValue.emit(self.engineNameList.index(name), count[0])

        if self.stopFlag:
            # self._print('%s取消完成' % name)
            self.ms.progressBar_setRange.emit(self.engineNameList.index(name), 0, 0)
            self.ms.progressBar_setValue.emit(self.engineNameList.index(name), 0)
            self._stop_mode()
            self.progressBarReset()
            raise Exception("%s强制停止! 下载到%d" % (name, count[0]))

        try:
            response = requests.get(url, stream=True)  # stream=True必须写上
            size = 0  # 初始化已下载大小
            chunk_size = 1024  # 每次下载的数据大小
            
            if response.status_code == 200:  # 判断是否响应成功
                filepath = path
                with open(filepath, 'wb') as file:  # 显示进度条
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                
                return 200
            else:
                self._print("%s一个网络错误码" % (path, ))
                return 2
        except Exception as e:
            self._print(str(e))
            return 1
        finally:
            if count[0] >= self.engineList[self.engineNameList.index(name)].num:
                self._print('%s下载完成' % name)
                self.progressBarReset(self.engineNameList.index(name))
                self._stop_mode()
            

    



