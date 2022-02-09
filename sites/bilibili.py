from webcore import directLinkCore
import os

class BilibiliPage(directLinkCore):
    name = 'Bilibili'
    def __init__(self, searchURL = 'https://search.bilibili.com/article') -> None:
        self.searchURL = searchURL

    def _getPageMax(self):
        '''
        获取页面数量
        '''
        html = self._getRequestBs4(url=self.searchURL, params={
                             "keyword": self.keyword})
        page = html.find(class_="pages")
        # 对页面请求，得到bs4页面
        if page is None:
            # 如果找不到底部页码 可能是没有文章，或者是只有1页
            if html.find(class_= "article-item") is None:
                self.maxPage = 0
            else:
                self.maxPage = 1
        else:
            # 通过页码按钮找到最大页码
            li = page.find_all("button")
            self.maxPage = int(li[-2].text)


    def _getUrlFormPage(self):
        if self.maxPage < 1:
            return False

        html = self._getRequestBs4(url=self.searchURL, params={
                             "keyword": self.keyWord, "page": self.currentPage})

        # 请求页面

        li_list = html.find_all(class_='poster')

        if len(li_list) == 0:
            return False
        # 找不到文章 进行返回

        for title in li_list:
            child_html = self._getRequestBs4(url="https:" + title["href"])
            # 进入每个页面
            img_attr = child_html.find_all("img")
            # 找到页面下的所有图片标签
            for i in img_attr:
                imgUrl = i["data-src"]
                if not (imgUrl.find("https://") != -1 or imgUrl.find("http://")) != -1:
                        imgUrl = "https:" + imgUrl
                # 获取图片链接
                imgUrl.split('.')
                name = os.path.basename(imgUrl)
                self._addList(
                    imgURL=imgUrl,
                    name=name.split('.')[-2],
                    _type=name.split('.')[-1]
                )
                print(name.split('.')[-2], name.split('.')[-1])
        self.currentPage = self.currentPage + 1
        return self.currentPage <= self.maxPage
            