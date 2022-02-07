from webcore import directLinkCore
import math

class AlphacodersPage(directLinkCore):
    def __init__(self, keyWord, searchURL = 'https://wall.alphacoders.com/search.php') -> None:
        self.keyWord = keyWord
        self.searchURL = searchURL
        self._getPageMax()

    def _getPageMax(self):
        html = self._getRequestBs4(url=self.searchURL, params={
                             "search": self.keyWord})
        num = html.find('h1', {"class": "center title"})
        for i in num.text.split(' '):
            if i.isnumeric():
                self.maxPage = (math.ceil(int(i) / 30))

    def _getUrlFormPage(self):
        html = self._getRequestBs4(url=self.searchURL, params={
                             "search": self.keyWord, "page": self.currentPage, "quickload": self.currentPage})
        self.currentPage = self.currentPage + 1
        spanList = html.find_all('span', {"title": "Download Wallpaper"})
        for i in spanList:
            self._addList(
                "https://initiate.alphacoders.com/download/wallpaper/%s/%s/%s/"
                % (str(i['data-id']), i['data-server'], i['data-type']), i['data-id'], i['data-type']
            )
        return self.currentPage <= self.maxPage