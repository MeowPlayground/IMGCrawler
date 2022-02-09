#coding = 'utf-8'

import sys
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget

from .action import Action
from .ui import UI
from .common import *


class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    print = pyqtSignal(str)
    update_pb = pyqtSignal(int)
    update_range = pyqtSignal(int)
    button_set = pyqtSignal(int)
    engine_setChecked = pyqtSignal(int, bool)
    engine_setCheckable = pyqtSignal(int, bool)

class MainWindow(QWidget):
    def __init__(self):
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = UI()
        self.ui.Init_UI(self)
        self.action = Action(signal=signals, ui=self)
        self.action.init_engine()
        self.Init_Button()
        

    def Init_Button(self):
        '''
            初始化所有的按钮的信号与槽
        '''
        self.ui.searchButton.clicked.connect(self.action.search)
        self.ui.startButton.clicked.connect(self.action.start)
        self.ui.stopButton.clicked.connect(self.action.stop)
        signals.button_set.connect(self.button_set)
        signals.print.connect(self.print)
        signals.engine_setChecked.connect(self.engine_setChecked)

    
    def print(self, t):
        '''
        text browser 打印函数
        '''
        self.ui.textBrowser.append(str(t))
        self.ui.textBrowser.ensureCursorVisible()

    def engine_setChecked(self, n, v):
        self.action.checkBoxList[n].setChecked(v)


    def button_set(self, n):
        if n == SEARCH_ENABLE:
            self.ui.searchButton.setEnabled(True)
        elif n == START_ENABLE:
            self.ui.startButton.setEnabled(True)
        elif n == STOP_ENABLE:
            self.ui.stopButton.setEnabled(True)
        elif n == SAVE_ENABLE:
            self.ui.savepathButton.setEnabled(True)
        elif n == SEARCH_DISABLE:
            self.ui.searchButton.setEnabled(False)
        elif n == SAVE_DISABLE:
            self.ui.startButton.setEnabled(False)
        elif n == START_DISABLE:
            self.ui.stopButton.setEnabled(False)
        elif n == SAVE_DISABLE:
            self.ui.savepathButton.setEnabled(False)


app = QApplication([])
signals = MySignals()
mainw = MainWindow()
