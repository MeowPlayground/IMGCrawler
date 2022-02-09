from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QFormLayout, QLabel, QLineEdit, QTextEdit, QTextBrowser, QToolButton, QHBoxLayout, QVBoxLayout, QCheckBox, QProgressBar)
class UI(QWidget):
    # def __init__(self):
    #     super().__init__()
    #     self.Init_UI()
    #     self.Init_Button()
    #     self.show()
        
    def Init_UI(self, MainWindow):
        # self.setGeometry(300,300,300,200)
        MainWindow.setWindowTitle('图片爬虫')
        formLayout = QVBoxLayout()

        # search layout
        self.keywordLine = QLineEdit()
        self.searchButton = QPushButton('搜索')

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(QLabel("关键词:"))
        searchLayout.addWidget(self.keywordLine)
        searchLayout.addWidget(self.searchButton)

        # savepath layout
        self.savepathLine = QLineEdit()
        self.savepathButton = QToolButton()
        self.savepathButton.setText('...')

        savepathLayout = QHBoxLayout()
        savepathLayout.addWidget(QLabel("保存地址:"))
        savepathLayout.addWidget(self.savepathLine)
        savepathLayout.addWidget(self.savepathButton)
        

        # engine layout
        self.checkBoxList = [
            QCheckBox('Bilibili', objectName = 'Bilibili', checked = True),
            QCheckBox('Alphacoders',objectName = 'Alphacoders', checked = True)
        ]
        self.engineLayout = QHBoxLayout()
        self.engineLayout.addWidget(QLabel('引擎:'))
            

        # progress layout
        self.progressLabel = QLabel('进度条')
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 0)
        self.progressBar.setValue(0)
        
        progressLayout = QHBoxLayout()
        progressLayout.addSpacing(20)
        progressLayout.addWidget(self.progressLabel)
        progressLayout.addWidget(self.progressBar)
        progressLayout.addSpacing(0)

        # start layout
        self.startButton = QPushButton('开始')
        self.stopButton = QPushButton('取消')

        startLayout = QHBoxLayout()
        startLayout.addWidget(self.startButton)
        startLayout.addWidget(self.stopButton)

        self.textBrowser = QTextBrowser()

        formLayout.addLayout(searchLayout)
        formLayout.addLayout(savepathLayout)
        formLayout.addLayout(self.engineLayout)
        formLayout.addLayout(progressLayout)
        formLayout.addWidget(self.textBrowser)
        formLayout.addLayout(startLayout)
        
        MainWindow.setLayout(formLayout)