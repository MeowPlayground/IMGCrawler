from traceback import print_tb
from sites import AlphacodersPage
from sites.bilibili import BilibiliPage
from uicore import mainw, app
import sys

def code(c, m):
    print("c = %d, m = %d" % (c, m))

if __name__ == "__main__":
    # myPage = BilibiliPage("夏洛特 p charlotte")
    # myPage.whileGetUrl()
    # myPage._removeSame()
    # myPage.save("E:\\OneDrive\\Temp\\tet")
    
    mainw.show()
    app.exec_()
