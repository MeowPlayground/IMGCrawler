from socket import timeout
from webcore import DirectLinkCore
import math

class AlphacodersPage(DirectLinkCore):
    
    def __init__(self, searchURL = 'https://wall.alphacoders.com/search.php') -> None:
        self.searchURL = searchURL
        self.setName('Alphacoders')

    def getPageMax(self):
        html = self._getRequestBs4(url=self.searchURL, params={
                             "search": self.keyword})
        num = html.find('h1', {"class": "center title"})
        for i in num.text.split(' '):
            if i.isnumeric():
                self.maxPage = (math.ceil(int(i) / 30))

    def _getUrlFormPage(self):
        self.currentPage = self.currentPage + 1
        html = self._getRequestBs4(url=self.searchURL, params={
                             "search": self.keyword, "page": self.currentPage, "quickload": self.currentPage})
        
        spanList = html.find_all('span', {"title": "Download Wallpaper"})
        for i in spanList:
            self._addList(
                "https://initiate.alphacoders.com/download/wallpaper/%s/%s/%s/"
                % (str(i['data-id']), i['data-server'], i['data-type']), i['data-id'], i['data-type']
            )
        return self.currentPage < self.maxPage