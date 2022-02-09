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
        self.engineWorkList = []
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

    def init_engine(self):
        """
        引擎初始化函数
        """
        for i in self.engineList:
            self.engineNameList.append(i.name)
            self.checkBoxList.append(
                QCheckBox(i.name, objectName=i.name, checked=True))
            self.progressBarList.append({
                "label": QLabel(i.name),
                "progressBar": QProgressBar()
            })
            self.engineWorkList.append([0, 0])

        for i in self.checkBoxList:
            self.ui.engineLayout.addWidget(i)

        for i in self.progressBarList:
            progressLayout = QHBoxLayout()
            progressLayout.addWidget(i['label'])
            progressLayout.addWidget(i['progressBar'])
            self.ui.formLayout.addLayout(
                progressLayout
            )
        self.engineNum = len(self.engineList)

    def _checkBox_setChecked(self, n, v):
        """
        引擎选项框选择状态设置
        """
        self.ms.engine_setChecked.emit(n, v)

    def progressBar_setHide(self, n, v: bool):
        """
        进度条显示型设置
        n 第n的进度条，对应引擎
        v:bool 
        """
        if v:
            self.progressBarList[n]['label'].hide()
            self.progressBarList[n]['progressBar'].hide()
        else:
            self.progressBarList[n]['label'].show()
            self.progressBarList[n]['progressBar'].show()

    def progressBarReset(self, i):
        """
        进度条重置函数
        """
        self.ms.progressBar_setRange.emit(i, 0, 0)
        self.ms.progressBar_setValue.emit(i, 0)

    def setSavepath(self):
        """
        储存位置设置函数
        绑定按钮
        """
        self.savepath = QFileDialog.getExistingDirectory()
        self.ui.savepathLine.setText(self.savepath)

    def search(self):
        """
        搜索入口函数
        """
        self.engineEnableCount = 0
        self.keyword = self.ui.keywordLine.text()
        _addTread(self._search_thread)

    def _search_thread(self):
        """
        搜索线程函数
        该函数在新线程下执行
        """
        # 将按钮模式设置搜索模式
        self._searching_mode()

        for i in range(self.engineNum):
            # 遍历所有引擎
            # 该函数工作在单线程下
            # 按顺序进行引擎关键词搜索
            # 欲得到最大页数
            engine = self.engineList[i]

            engine.clearList()
            # 清除之前的缓存
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

    def start(self):
        """
        开始入口函数
        """

        # 清除停止Flasg
        self.stopFlag = False

        # 检查一下savepath有没有被设置了，
        if self.savepath == '' or self.savepath is None or (not os.path.exists(self.savepath)):
            self._print('地址%s不存在' % self.savepath)
            return

        # 设置按钮状态为开始模式
        self.ms.engine_enable.emit(False)
        self.ms.button_set.emit(SEARCH_DISABLE)
        self.ms.button_set.emit(START_DISABLE)
        self.ms.button_set.emit(STOP_ENABLE)
        self.ms.button_set.emit(SAVE_DISABLE)

        # 重置工作状态
        for i in range(self.engineNum):
            self.engineWorkList[i][0] = 0
            self.engineWorkList[i][1] = 0

        # 引擎遍历
        # 和之前的搜索页数不同的是，这里的链接搜索是一个引擎分一个线程执行
        for i in range(self.engineNum):

            # 该引擎下的最大页数不为0，意味着该引擎完成了页数搜索，激活该引擎
            if self.engineList[i].getMaxPage() > 0:
                self.engineWorkList[i][0] = 1
                _addTread(self._start_thread_, args=(i,))
                self._print("引擎%s已激活" % self.engineList[i].name)

            else:
                self._print("引擎%s未激活" % self.engineList[i].name)
                self.engineEnableCount = self.engineEnableCount + 1

        # 工作状态 [0, 0]，第一个代表链接搜索线程数，第二个是下载线程数
        # 这意味着所有的链接搜索线程数都为0
        if self._allThreadNotWork():
            self._print("所有引擎%s均未激活" % self.engineList[i].name)
            self._searching_OK_mode()
            for j in range(self.engineNum):
                self.progressBarReset(j)

    def _allThreadNotWork(self):
        # 工作状态 [0, 0]，第一个代表链接搜索线程数，第二个是下载线程数
        # 这意味着所有的链接搜索线程数都为0
        for i in self.engineWorkList:
            if not (i[0] == 0 and i[1] == 0):
                return False

        return True

    def _start_thread_(self, i):
        """
        搜索线程函数
        参数 i 目前运行的引擎id
        """
        # 当运行到这个函数时，意味着不同的引擎目前进入了不同的线程

        # 合成当前引擎的目录
        # 保存目录 + 关键词和引擎名
        path = os.path.join(self.savepath, self.keyword +
                            '-' + self.engineList[i].name)

        # 如果存在了这个目录，进行文件夹名后面增加 _? 的操作来避免重名
        if os.path.exists(path):
            k = 1
            while os.path.exists(os.path.join(self.savepath, self.keyword + '-' + self.engineList[i].name) + '_' + str(k)):
                k = k + 1
            path = os.path.join(self.savepath, self.keyword +
                                '-' + self.engineList[i].name + '_' + str(k))
        os.makedirs(path)
        self._print('创建目录%s' % path)

        # 该函数在完成一个页数链接爬取会被调用一次

        def _func_whileGetUrl(current):

            # 这里是一个关键的stopflag处理
            if self.stopFlag:
                # 将该线程工作状态设置为停止
                self.engineWorkList[i][0] = 0

                raise Exception("%s强制停止!" % (self.engineList[i].name))

            # 通常情况下这个函数负责更新进度条
            self.ms.progressBar_setValue.emit(i, current)

        # 设置该引擎进度条范围
        self.ms.progressBar_setRange.emit(
            i, 0, self.engineList[i].getMaxPage())

        # try检测异常
        try:
            self.engineList[i].whileGetUrl(_func_whileGetUrl)
        except Exception as e:
            self._print(self.engineList[i].name + '---' + str(e))
            self._print("引擎%s链接爬取失败" %
                        (self.engineList[i].name))

            # 如果所有的协程都不在工作了，则初始化按钮
            if self._allThreadNotWork():
                self._stop_mode()
                self.progressBarReset(i)
                self._print("所有引擎已停止")
            return

        # 视觉效果 设置100%的进度条
        self.ms.progressBar_setValue.emit(i, self.engineList[i].getMaxPage())
        self._print("引擎%s链接爬取已结束,获得链接%d" %
                    (self.engineList[i].name, self.engineList[i].num))

        # 设置进度条 最大为链接数
        self.ms.progressBar_setRange.emit(
            i, 0, self.engineList[i].num)

        try:
            # 引擎保存函数
            # 将目前引擎工作状态传入
            self.engineList[i].save(
                path, self.engineWorkList[i], self._download)
        except Exception as e:
            self._print(str(e))

    def _download(self, url, path, count, name):
        """
        这个一个基础下载函数
        """
        index = self.engineNameList.index(name)
        # 增加一个下载值
        count[0] = count[0] + 1
        self.ms.progressBar_setValue.emit(index, count[0])

        if self.stopFlag:
            # 减少一个下载线程
            self.engineWorkList[index][1] = self.engineWorkList[index][1] - 1

            # 如果所有的线程不在工作, 重置按钮
            if self._allThreadNotWork():
                self._print('全部已停止,共%d实际下载完成%d' % (count[0], count[1]))
                self.ms.progressBar_setRange.emit(
                    self.engineNameList.index(name), 0, 0)
                self.ms.progressBar_setValue.emit(
                    self.engineNameList.index(name), 0)
                self._stop_mode()
                for j in range(self.engineNum):
                    self.progressBarReset(j)
            return -1

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
                count[1] = count[1] + 1
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
                self._print('共%d实际下载完成%d' % (count[0], count[1]))
                self.progressBarReset(self.engineNameList.index(name))
                self._stop_mode()

    def progressShow(self, c):
        index = self.engineNameList.index(c.objectName())
        self.ms.progressBar_setHide.emit(index, not c.isChecked())
        self.ms.button_set.emit(START_DISABLE)

    def progressBar_setRange(self, i, a, b):
        self.progressBarList[i]['progressBar'].setRange(a, b)

    def progressBar_setValue(self, i, n):
        self.progressBarList[i]['progressBar'].setValue(n)

    def stop(self):
        self.stopFlag = True

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
