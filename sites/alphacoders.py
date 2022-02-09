from webcore import directLinkCore
import math

class AlphacodersPage(directLinkCore):
    name = 'Alphacoders'
    def __init__(self, searchURL = 'https://wall.alphacoders.com/search.php') -> None:
        self.searchURL = searchURL

    def _getPageMax(self):
        html = self._getRequestBs4(url=self.searchURL, params={
                             "search": self.keyword})
        num = html.find('h1', {"class": "center title"})
        for i in num.text.split(' '):
            if i.isnumeric():
                self.maxPage = (math.ceil(int(i) / 30))

    def _getUrlFormPage(self):
        html = self._getRequestBs4(url=self.searchURL, params={
                             "search": self.keyword, "page": self.currentPage, "quickload": self.currentPage})
        self.currentPage = self.currentPage + 1
        spanList = html.find_all('span', {"title": "Download Wallpaper"})
        for i in spanList:
            self._addList(
                "https://initiate.alphacoders.com/download/wallpaper/%s/%s/%s/"
                % (str(i['data-id']), i['data-server'], i['data-type']), i['data-id'], i['data-type']
            )
        return self.currentPage <= self.maxPage