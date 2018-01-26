#! python3
import sys
from html.parser import HTMLParser
from urllib import request

if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = raw_input("Website URL: ")

#remember that slice ranges have an excluded upper bound
if url[0:4] != "http":
    print("Invalid input; please pass a url in the form of http(s)://________")
    exit(0)

print("Site to scrape: \"" + url + "\"")

# download our top level webpage

class HTMLParser(HTMLParser):
    scrapedURLs = []
    scrapedEmails = []
    pageUrl = ""
    # this custom definiton will use the url to prepend to found subpaths
    def __init__(self, url):
        super().__init__()
        self.pageUrl = url

    def parseHref(self, h):
        #determine if we have a new path or a new email
        if h[0] == "/" or h[0:4] == "http":
            # print("path: " + h)
            self.addPathString(h)
        else:
            if h[0] != "#":
                # print("email: " + h)
                self.addEmailString(h)
                #we can now be fairly certain that this is a umich email

    def addEmailString(self, h):
        # note that the replace method does not affect original.
        # will return a new modified string
        h = h.replace("mailto:", "")
        h = h.split("?")[0]
        self.scrapedEmails.append(h)

    def addPathString(self, h):
        if h[0] == "/":
            h = self.pageUrl + h
        #careful to use .append instead of += to avoid splitting the string into chars
        self.scrapedURLs.append(h)

    def handle_starttag(self, tag, attrs):
        # print("START: " + tag)
        if tag == "a":
            for att in attrs:
                if "href" in att:
                    #get second item in attribute pair if we have an href
                    self.parseHref(att[1])

    # def handle_endtag(self, tag):
    #     pass

# main code
topPage = request.urlopen(url)
scrapeParser = HTMLParser(url)
scrapeParser.feed(str(topPage.read()))

print(scrapeParser.scrapedEmails)
print(scrapeParser.scrapedURLs)
# print(str(topPage.read()))
