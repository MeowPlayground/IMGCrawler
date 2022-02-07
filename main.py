from traceback import print_tb
from sites import AlphacodersPage
from sites.bilibili import BilibiliPage

def code(c, m):
    print("c = %d, m = %d" % (c, m))

if __name__ == "__main__":
    myPage = BilibiliPage("七宫智音")
    myPage.whileGetUrl()
    print(len(myPage.imgList))
    myPage._removeSame()
    print(len(myPage.imgList))