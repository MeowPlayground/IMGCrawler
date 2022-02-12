#coding = 'utf-8'
from tkinter.messagebox import NO
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget
from functools import partial
from PyQt5.QtGui import QIcon

from .action import Action
from .ui import UI
from .common import *
import uicore.window_icon


class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    print = pyqtSignal(str)

    button_set = pyqtSignal(int)
    engine_setChecked = pyqtSignal(int, bool)
    engine_enable = pyqtSignal(bool)
    progressBar_setHide = pyqtSignal(int, bool)
    progressBar_setRange = pyqtSignal(int, int, int)
    progressBar_setValue = pyqtSignal(int, int)


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
        self.Init_Button()

    def Init_Button(self):
        """
            初始化所有的按钮的信号与槽
        """
        self.ui.searchButton.clicked.connect(self.action.search)
        self.ui.startButton.clicked.connect(self.action.start)
        self.ui.stopButton.clicked.connect(self.action.stop)
        self.ui.savepathButton.clicked.connect(self.action.setSavepath)
        self.ui.openFolderButton.clicked.connect(self.action.openSavepath)

        self.ui.keywordLine.textChanged.connect(self.action.keywordTextChanged)
        for i in self.action.checkBoxList:
            i.clicked.connect(partial(self.action.progressShow, i))

        signals.progressBar_setHide.connect(self.action.progressBar_setHide)
        signals.progressBar_setRange.connect(self.action.progressBar_setRange)
        signals.progressBar_setValue.connect(self.action.progressBar_setValue)

        signals.button_set.connect(self.button_set)
        signals.print.connect(self.print)
        signals.engine_setChecked.connect(self.engine_setChecked)
        signals.engine_enable.connect(self.engine_enable)

    def print(self, t):
        """
        text browser 打印函数
        """
        self.ui.textBrowser.append(str(t))
        self.ui.textBrowser.ensureCursorVisible()

    def engine_setChecked(self, n, v):
        self.action.checkBoxList[n].setChecked(v)

    def engine_enable(self, b):
        for i in self.action.checkBoxList:
            i.setEnabled(b)

    def button_set(self, n):
        if n == SEARCH_ENABLE:
            if not (self.ui.keywordLine.text() == "" or self.ui.keywordLine.text() is None):
                self.ui.searchButton.setEnabled(True)
        elif n == START_ENABLE:
            self.ui.startButton.setEnabled(True)
        elif n == STOP_ENABLE:
            self.ui.stopButton.setEnabled(True)
        elif n == SAVE_ENABLE:
            self.ui.savepathButton.setEnabled(True)
        elif n == SEARCH_DISABLE:
            self.ui.searchButton.setEnabled(False)
        elif n == START_DISABLE:
            self.ui.startButton.setEnabled(False)
        elif n == STOP_DISABLE:
            self.ui.stopButton.setEnabled(False)
        elif n == SAVE_DISABLE:
            self.ui.savepathButton.setEnabled(False)
        elif n == KEYWORDLINE_ENABLE:
            self.ui.keywordLine.setEnabled(True)
        elif n == KEYWORDLINE_DISABLE:
            self.ui.keywordLine.setEnabled(False)


app = QApplication([])
signals = MySignals()
mainw = MainWindow()
mainw.setWindowIcon(QIcon(':/icon.ico'))
