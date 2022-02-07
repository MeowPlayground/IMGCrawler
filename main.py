from WebCore import AlphacodersPage

def code(c, m):
    print("c = %d, m = %d" % (c, m))

if __name__ == "__main__":
    myPage = AlphacodersPage("urara 迷路贴")
    myPage.getMaxPage()
    myPage.whileGetUrl(code)
    myPage.save('E:\\OneDrive\\Temp\\tet')
