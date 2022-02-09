from sites import BilibiliPage, AlphacodersPage
from threading import Thread
from PyQt5.QtWidgets import QWidget, QCheckBox
from PyQt5.QtCore import pyqtSignal
from .common import *

class Action:
    def __init__(self, signal : pyqtSignal, ui : QWidget) -> None:
        self.ms = signal
        self.ui = ui.ui

    def _addTread(self, func, args=()):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()
    
    def _checkBox_setChecked(self, n, v):
        self.ms.engine_setChecked.emit(n, v)
    

    def _searching_mode(self):
        self.ms.button_set.emit(SEARCH_DISABLE)
        self.ms.button_set.emit(START_DISABLE)
        self.ms.button_set.emit(STOP_DISABLE)
       


    def _searching_OK_mode(self):
        self.ms.button_set.emit(SEARCH_ENABLE)
        self.ms.button_set.emit(START_ENABLE)
        

    def _print(self, t):
        self.ms.print.emit(t)
    
    def _search_thread(self):
        self._searching_mode()
        
    
        for i in range(len(self.engineList)):
            engine = self.engineList[i]
            if self.checkBoxList[i].isChecked():
                try:
                    engine.setKeyword(self.keyword)
                    engine._getPageMax()
                    if engine.getMaxPage() > 0:
                        self._print('关键词%s,初始化%s成功,得到页数%d' % (self.keyword ,engine.name, engine.getMaxPage()))
                        self._checkBox_setChecked(i, True)
                    else:
                        self._checkBox_setChecked(i, False)
                        self._print('关键词%s,初始化%s失败,页数为0' % (self.keyword, engine.name))
                except Exception as e:
                    self._print('关键词%s,初始化%s失败,%s' % (self.keyword, engine.name, str(e)))
                    self._checkBox_setChecked(i, False)

        self._searching_OK_mode()

        
    def init_engine(self):
        self.engineList = [
            BilibiliPage(),
            AlphacodersPage()
        ]
        self.checkBoxList = []
        for i in self.engineList:
            self.checkBoxList.append(QCheckBox(i.name, checked = True))
        
        for i in self.checkBoxList:
            self.ui.engineLayout.addWidget(i)

    def search(self):
        self.keyword = self.ui.keywordLine.text()
        self._addTread(self._search_thread)

    def start(self):
        pass

    def stop(self):
        pass