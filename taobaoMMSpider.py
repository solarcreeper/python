import os
from time import sleep
from urllib import request, error

import re


class TBMMSP:
    def __init__(self):
        self.pageIndex = 1
        self.publicReferer = 'https://mm.taobao.com/json/request_top_list.htm'
        self.urlBase = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.userInfo = []

    def getPage(self, url, referer, decode, isReferer):
        user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        header = {'User-Agent': user_agent}

        try:
            url_request = request.Request(url, headers=header)
            if isReferer:
                url_request.add_header('Referer', referer)
            url_response = request.urlopen(url_request).read().decode(decode)
            if url_response:
                return url_response
            else:
                return None
        except (error.URLError, error.HTTPError) as e:
            if hasattr(e, 'reason'):
                print('获取地址失败', e.reson)
            else:
                print('unknown error')

    def getPageContent(self, page):
        content = []
        pattern = re.compile(
            '<div class="list-item">.*?<a class="lady-name" href="(.*?)" target="_blank">(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',
            re.S)
        items = re.findall(pattern, page)
        for item in items:
            mmUrl = 'https:' + item[0].strip()
            content.append([mmUrl, item[1].strip(), item[2].strip(), item[3].strip()])
        return content

    def getDomainUrl(self, contents):
        for content in contents:
            personInfoContent = self.getPage(content[0], self.urlBase + str(self.pageIndex), 'gbk', False)
            pattern = re.compile(
                'KISSY.ready.*?url:"(.*?),',
                re.S)
            personInfo = re.findall(pattern, personInfoContent)
            text = personInfo[0].replace('"+', '')
            personDetailInfoUrl = 'https://mm.taobao.com' + text
            personDetailInfoContent = self.getPage(personDetailInfoUrl, personInfoContent, 'gbk', False)
            pattern = re.compile(
                '<div class="mm-p-info mm-p-domain-info">.*?<span>(.*?)</span>',
                re.S)
            domainInfoUrls = re.findall(pattern, personDetailInfoContent)
            if len(domainInfoUrls) == 0:
                domainInfoUrl = None
            else:
                domainInfoUrl = 'https:' + domainInfoUrls[0]
                print(domainInfoUrl)
            content[0] = domainInfoUrl
        return contents

    def getPicUrlList(self, contents):
        for content in contents:
            if content[0] is not None:
                urlContent = self.getPage(content[0], self.publicReferer, 'gbk', False)
                pattern = re.compile(
                    '<img style="float.*?src="(.*?)tstar.jpg',
                    re.S)
                picUrls = re.findall(pattern, urlContent)
                if len(picUrls) > 0:
                    self.userInfo.append([picUrls, content[1], content[2], content[3]])
        return None

    def saveFile(self):
        for item in self.userInfo:
            foulderName = item[1]
            imageUrls = item[0]
            self.mkdir(foulderName)
            index = 1
            for imgurl in imageUrls:
                pattern = re.compile('png', re.S)
                isPng = re.search(pattern, imgurl)
                if isPng is None and len(imgurl) < 100:
                    url = 'https:' + imgurl + 'tstar.jpg'
                    path = foulderName + '/' + foulderName + '_' + str(index) + '.jpg'
                    print(path)
                    print(url)
                    self.saveImg(url, path)
                    index = index + 1
        return None

    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            print('exist')
            return False

    def saveImg(self, imageURL, filename):
        try:
            u = request.urlopen(imageURL)
            data = u.read()
            file = open(filename, 'wb')
            file.write(data)
            file.close()
        except(error.HTTPError, error.URLError) as e:
            if hasattr(e, 'reason'):
                print(e.reason)

    def start(self):
        while True:
            page = self.getPage(self.urlBase + str(self.pageIndex), self.publicReferer, 'gbk', True)
            content = self.getPageContent(page)
            content = self.getDomainUrl(content)
            self.getPicUrlList(content)
            self.saveFile()
            self.pageIndex = self.pageIndex + 1


sp = TBMMSP()
sp.start()
