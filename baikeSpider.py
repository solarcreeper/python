from time import sleep
from urllib import request,error,parse
import re


class BKSP:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        self.header = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = True
        self.filename = "save.txt"

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            url_request = request.Request(url, headers=self.header)
            url_request.add_header('Referer', 'http://www.qiushibaike.com/hot/page/1/')
            response = request.urlopen(url_request).read().decode('utf-8')
            return response
        except (error.HTTPError, error.URLError) as e:
            if hasattr(e, "reason"):
                print('链接失败：', e.reason)
            else:
                print('unknown error')
            return None

    def getPageItems(self, pageIndex):
        page = self.getPage(self.pageIndex)
        if not page:
            print('获取页面失败')
            return None
        pattern = re.compile(
            '<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?</div>(.*?)<div class="stats">.*?<i class="number">(.*?)</i>(.*?)</span>.*?<i class="number">(.*?)</i>(.*?)</a>',
            re.S)
        pageStories = []
        items = re.findall(pattern, page)
        for item in items:
            img = re.search(re.compile('jpg'), item[2])
            if not img:
                replaceBr = re.compile('</br>')
                text = re.sub(replaceBr, "\n", item[1])
                replaceBr = re.compile('<br/>')
                text = re.sub(replaceBr, "\n", text)
                pageStories.append([item[0].strip(), text.strip(), item[3].strip(), item[4].strip(), item[5].strip(), item[6].strip()])
            else:
                pass
        return pageStories

    def loadPage(self):
        if self.enable == True:
                pageStories = self.getPageItems(self.pageIndex)

                while pageStories is not None and len(pageStories) == 0:
                    self.pageIndex = self.pageIndex + 1
                    pageStories = self.getPageItems(self.pageIndex)
                self.stories.append(pageStories)
        return None

    def printStory(self, pageStories):
        index = 1
        for story in pageStories:
            print("第%d页\t第%d条\t发布人:%s\t发布时间:%s\t赞:%s\n%s" %(self.pageIndex,index,story[0],story[2],story[3],story[1]))
            index = index + 1
            print("--------------------------------------------------------")
        return None

    def saveStory(self, pageStories, filename, level):
        index = 1
        file = open(filename, "a", encoding="utf-8")
        for story in pageStories:
            if int(story[2]) > level:
                content = "第%d页\t第%d条\t发布人:%s\t发布时间:%s\t赞:%s\n%s" %(self.pageIndex,index,story[0],story[2],story[3],story[1])
                file.write(content)
                file.write('\n')
                file.write("-----------------------------------------------------------\n")
                index = index + 1
                print(content)
        return None

    def start(self):
        self.enable = True
        while self.enable:
            self.loadPage()
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                self.printStory(pageStories)
                del self.stories[0]
                print('press c to continue')
                comand = input().strip()
                if comand != "C" and comand != "c":
                    self.enable = False
                else:
                    self.pageIndex = self.pageIndex + 1
        return None

    def startAndSave(self, level):
        self.enable = True
        while self.enable:
            self.loadPage()
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                self.saveStory(pageStories, self.filename, level)
                sleep(2)
                del self.stories[0]
                if self.pageIndex == 10000:
                    self.enable = False
                else:
                    self.pageIndex = self.pageIndex + 1
        return None

spider = BKSP()
# spider.start()
spider.startAndSave(5000)

