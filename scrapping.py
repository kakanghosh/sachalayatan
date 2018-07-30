from bs4 import BeautifulSoup
import urllib.request
import os

class Sachalayatan:
    sachDS = {}
    def __init__(self, BASE_URL):
        self.sachDS['BASE_URL'] = BASE_URL

    def getHtml(self, url=''):
        if len(url) > 0:
            source = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(source,'lxml')
            return soup
        else:
            source = urllib.request.urlopen(self.sachDS['BASE_URL']).read()
            soup = BeautifulSoup(source, 'lxml')
            return soup

    def getMainNavURL(self, html):
        urls = html.select("ul#subnavlist > li > a")
        urlList = []
        for url in urls:
            urlList.append(url.get('href'))
        self.sachDS['main_nav'] = urlList
        self.writeListInFile('main_nav.txt', 'a', urlList)
        return urlList

    def getPaginationFromMainURL(self):
        fileName  = 'navigationlink.txt'
        mainNavList = [line.rstrip('\n') for line in open('./main_nav.txt')]
        if os.path.isfile(fileName) and os.access(fileName, os.R_OK):
            open(fileName, "w").close()
        for nav in mainNavList:
            print('working with: ', nav)
            print(nav)
            self.writeLineInFile('navigationlink.txt', 'a', nav)
            html = self.getHtml(nav)
            urls = html.select('ul.pager > li.pager-item > a')

            for url in urls:
                print(url)
                self.writeLineInFile('navigationlink.txt', 'a', url.get('href'))
            self.writeLineInFile('navigationlink.txt', 'a', '')

    def writeListInFile(self, fileName, mode, writeList):
        # print(type(writeList))
        txtFile = open(fileName, mode, encoding="utf-8")
        for line in writeList:
            txtFile.write(line + "\n")
        txtFile.write("\n")
        txtFile.close()

    def writeLineInFile(self, fileName, mode, line):
        # print(type(writeList))
        txtFile = open(fileName, mode, encoding="utf-8")
        txtFile.write(line + "\n")
        txtFile.close()

    def showList(self, itemList):
        for iList in itemList:
            print(iList)

BASE_URL = 'http://www.sachalayatan.com/'
sachObj = Sachalayatan(BASE_URL=BASE_URL)
# html = sachObj.getHtml()
# sachObj.getMainNavURL(html)
sachObj.getPaginationFromMainURL()