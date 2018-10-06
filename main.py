from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

#creating a class called WebCrawler
class WebCrawler(HTMLParser):
    #Overloading this function in HTMLParese
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    self.links = self.links + [newUrl]
    
    def getLinks(self, url):
        self.links = []
        self.baseUrl = url
        response = urlopen(url)
        htmlBytes = response.read()
        htmlString = htmlBytes.decode("utf-8") #We need to decode to string to be able to use feed
        self.feed(htmlString)
        return htmlString, self.links

    #creating the spider
    def spider(self, url, word, maxPages):
        pagesToVisit = [url]
        numberVisited = 0
        foundWord = False
        #searching the page for word or string and only look at maxPages number of pages to limit scope
        while numberVisited < maxPages and pagesToVisit != [] and not foundWord:
            numberVisited = numberVisited + 1
            url = pagesToVisit[0]
            pagesToVisit = pagesToVisit[1:]
            try:
                print(numberVisited, "Visiting:", url)
                parser = WebCrawler()
                data, links = parser.getLinks(url)
                if data.find(word) > -1:
                    foundWord = True
                    pagesToVisit = pagesToVisit + links
                    print("Success")
            except:
                print("Failed")
        if foundWord:
            print("The word ", word, " was found at ", url)
        else:
            print("Word never found")

crawler = WebCrawler()
crawler.spider("https://www.huffingtonpost.com/", "politics", 10)