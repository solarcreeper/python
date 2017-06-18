#!/usr/bin/python
# coding:utf-8
import re
import logging
from urllib import request, error
from MySQL import *


class DBSP:
    def __init__(self):
        self.url = 'https://book.douban.com/subject/'
        self.user_agent = "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        # self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
        self.header = {'User-Agent': self.user_agent}
        self.pageIndex = 100000
        self.booklist = []
        self.retryCount = 0
        self.OK = 1000
        self.MUSIC_URL = 405
        self.PAGE_NOT_FOUND = 404
        self.PARSE_ERROR = 406
        self.INDEX_OUT_OF_RANGE = 407
        pass

    def getPageContent(self, pageIndex, encode):
        response = {}
        url = self.url + str(pageIndex) + '/'
        url_request = request.Request(url=url, headers=self.header)
        try:
            url_respose = request.urlopen(url_request).read().decode(encode)
            response['content'] = url_respose
            response['error_code'] = self.OK
        except (error.HTTPError, error.URLError) as e:
            logging.error(e)
            response['content'] = None
            response['error_code'] = self.PAGE_NOT_FOUND
        return response

    def getPageData(self, pageIndex, encode):
        response = self.getPageContent(pageIndex, encode)
        result = {}
        if response['error_code'] == self.PAGE_NOT_FOUND:
            result['error_code'] = self.PAGE_NOT_FOUND
            return result

        pageContent = response['content']
        isBook = re.compile('豆瓣音乐', re.S)
        if re.search(isBook, pageContent) is not None:
            logging.info('this page is a music page')
            result['error_code'] = self.MUSIC_URL
            return result

        bookInfoPattern = re.compile('<span property="v:itemreviewed">(.*?)</span>'
                                     '.*?<img src="(.*?)" title="'
                                     '.*?<div id="info"(.*?)<div id="interest_sectl"'
                                     '.*?property="v:average">(.*?)</strong>'
                                     '.*?class="related_info">(.*?)db-tags-section', re.S)

        try:
            bookinfo = re.findall(bookInfoPattern, pageContent)[0]
            bookInfoDetail = bookinfo[2].strip()
            introduction = bookinfo[4].strip()

        except (IndexError, ValueError) as e:
            logging.debug(e)
            result['error_code'] = self.INDEX_OUT_OF_RANGE
            return result

        try:
            result['name'] = bookinfo[0]
            result['img'] = bookinfo[1]

        except (IndexError, ValueError) as e:
            logging.debug(e)
            result['error_code'] = self.INDEX_OUT_OF_RANGE
            return result

        try:
            result['average'] = bookinfo[3]
        except (IndexError, ValueError) as e:
            logging.info('average is not found')
            result['average'] = 0

        try:
            authorPattern = re.compile('作者</span>.*?>(.*?)</a>', re.S)
            result['author'] = re.findall(authorPattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('author is not found')
            result['author'] = None

        try:
            subtitlePattern = re.compile('副标题.*?>(.*?)<br/>', re.S)
            result['subtitle'] = re.findall(subtitlePattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('subtitle is not found')
            result['subtitle'] = None

        try:
            bindingPattern = re.compile('装帧.*?>(.*?)<br/>', re.S)
            result['binding'] = re.findall(bindingPattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('binding is not found')
            result['binding'] = None

        try:
            isbnPattern = re.compile('ISBN.*?>(.*?)<br/>', re.S)
            result['isbn'] = re.findall(isbnPattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('isbn is not found')
            result['isbn'] = None
        try:
            publishPattern = re.compile('出版社.*?>(.*?)<br/>', re.S)
            result['publish'] = re.findall(publishPattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('publish is not found')
            result['publish'] = None

        try:
            publishYearPattern = re.compile('出版年.*?>(.*?)<br/>', re.S)
            result['publish_year'] = re.findall(publishYearPattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('publish_year is not found')
            result['publish_year'] = None

        try:
            pageNumPattern = re.compile('页数.*?>(.*?)<br/>', re.S)
            result['page_num'] = re.findall(pageNumPattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('page_num is not found')
            result['page_num'] = None

        try:
            pricePattern = re.compile('定价.*?>(.*?)<br/>', re.S)
            result['price'] = re.findall(pricePattern, bookInfoDetail)[0]
        except (IndexError, ValueError) as e:
            logging.info('price is not found')
            result['price'] = None

        try:
            contentItdPattern = re.compile('内容简介.*?class="intro">(.*?)</div>', re.S)
            contentIntroduction = re.findall(contentItdPattern, introduction)[0]
            replaceBr = re.compile('<br/>')
            contentIntroduction = re.sub(replaceBr, "\n", contentIntroduction)
            replaceBr = re.compile('</br>')
            contentIntroduction = re.sub(replaceBr, "\n", contentIntroduction)
            result['content_introduction'] = contentIntroduction
        except (IndexError, ValueError) as e:
            logging.info('content_introduction is not found')
            result['content_introduction'] = None

        try:
            authorItdPattern = re.compile('作者简介.*?class="intro">(.*?)</div>', re.S)
            authorIntroduction = re.findall(authorItdPattern, introduction)[0]
            replaceBr = re.compile('<br/>')
            authorIntroduction = re.sub(replaceBr, "\n", authorIntroduction)
            replaceBr = re.compile('</br>')
            authorIntroduction = re.sub(replaceBr, "\n", authorIntroduction)
            result['author_introduction'] = authorIntroduction
        except (IndexError, ValueError) as e:
            logging.info('author_introduction is not found')
            result['author_introduction'] = None

        try:
            catalogPattern = re.compile('目录.*?_full" style=.*?>(.*?)\(<a href=', re.S)
            bookCatalog = re.findall(catalogPattern, introduction)[0]
            replaceBr = re.compile('<br/>')
            bookCatalog = re.sub(replaceBr, "\n", bookCatalog)
            replaceBr = re.compile('</br>')
            bookCatalog = re.sub(replaceBr, "\n", bookCatalog)
            result['catalog'] = bookCatalog
        except (IndexError, ValueError) as e:
            logging.info('catalog is not found')
            result['catalog'] = None

        result['error_code'] = self.OK
        return result

    def save(self):
        pass

    def start(self, num):
        result = self.getPageData(num, 'utf-8')
        if result['error_code'] != self.OK:
            print(result['error_code'])
            return
        pairs = self.getKeyValues(result)
        db = MySQL('booklist')
        db.insert(pairs['keys'], pairs['values'], 'book')
        return

    def getKeyValues(self, result):
        pairs = {}
        keys = []
        values = []
        items = result.copy()
        del items['error_code']
        for (key, value) in items.items():
            keys.append(key)
            values.append(value)
        pairs['keys'] = keys
        pairs['values'] = values
        return pairs


dbsp = DBSP()
num = 27029497
for x in range(10000):
    dbsp.start(num)
    print('current page is' + str(x) + 'page num:' + str(num))
    num = num + 1
