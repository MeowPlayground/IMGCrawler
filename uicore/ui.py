from PyQt5.QtWidgets import (QWidget, QPushButton, QLabel,
                             QLineEdit, QTextBrowser, QToolButton, QHBoxLayout, QVBoxLayout)


class UI(QWidget):
    # def __init__(self):
    #     super().__init__()
    #     self.Init_UI()
    #     self.Init_Button()
    #     self.show()

    def Init_UI(self, MainWindow):
        # self.setGeometry(300,300,300,200)
        MainWindow.setWindowTitle('图片爬虫')
        self.formLayout = QVBoxLayout()

        # search layout
        self.keywordLine = QLineEdit()
        self.searchButton = QPushButton('搜索')
        self.searchButton.setEnabled(False)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(QLabel("关键词:"))
        searchLayout.addWidget(self.keywordLine)
        searchLayout.addWidget(self.searchButton)

        # savepath layout
        self.savepathLine = QLineEdit()
        self.savepathLine.setEnabled(False)
        self.savepathButton = QToolButton()
        self.savepathButton.setText('...')
        savepathLayout = QHBoxLayout()
        savepathLayout.addWidget(QLabel("保存地址:"))
        savepathLayout.addWidget(self.savepathLine)
        savepathLayout.addWidget(self.savepathButton)

        # engine layout
        self.engineLayout = QHBoxLayout()
        self.engineLayout.addWidget(QLabel('引擎:'))

        # start layout
        self.startButton = QPushButton('开始')
        self.startButton.setEnabled(False)
        self.stopButton = QPushButton('取消')
        self.stopButton.setEnabled(False)

        startLayout = QHBoxLayout()
        startLayout.addWidget(self.startButton)
        startLayout.addWidget(self.stopButton)

        self.textBrowser = QTextBrowser()

        self.formLayout.addLayout(searchLayout)
        self.formLayout.addLayout(savepathLayout)
        self.formLayout.addLayout(self.engineLayout)
        self.formLayout.addWidget(self.textBrowser)
        self.formLayout.addLayout(startLayout)

        MainWindow.setLayout(self.formLayout)
