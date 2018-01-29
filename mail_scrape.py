#! python3
import sys
from html.parser import HTMLParser
from urllib import request

class HTMLParser(HTMLParser):
    scrapedURLs = set()
    scrapedEmails = set()
    pageUrl = ""
    # this custom definiton will use the url to prepend to found subpaths
    def __init__(self, url):
        super().__init__()
        self.pageUrl = url

    def parseHref(self, h):
        #determine if we have a new path or a new email
        if not h:
            return
        if h[0] == "/" or (len(h) > 3 and h[0:4] == "http"):
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
        if "@" not in h:
            return
        h = h.replace("mailto:", "")
        h = h.split("?")[0]
        self.scrapedEmails.add(h)

    def addPathString(self, h):
        if h[0] == "/":
            h = self.pageUrl + h
        #careful to use .append instead of += to avoid splitting the string into chars
        self.scrapedURLs.add(h)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for att in attrs:
                if "href" in att:
                    #get second item in attribute pair if we have an href
                    self.parseHref(att[1])

def scrapeSubPages(_url, _depth, _superUrlSet = set()):
    #perform scraping given the url
    try:
        page = request.urlopen(_url)
    except:
        #may catch a unauthorized error 401
        return
    scrapeParser = HTMLParser(_url)
    scrapeParser.feed(str(page.read()))

    # print(scrapeParser.scrapedEmails)

    # iterate through all newly found urls in this webpage
    if _depth != 0:
        for newURL in list(scrapeParser.scrapedURLs):
            if newURL not in _superUrlSet:
                # print("url enumerated: " + newURL)
                # get new scraped emails and add to this specific parser's set
                _superUrlSet.add(newURL)
                newEmails = scrapeSubPages(newURL, _depth - 1, _superUrlSet)
                if newEmails:
                    for e in newEmails:
                        scrapeParser.scrapedEmails.add(e)


    return scrapeParser.scrapedEmails

depth = 0
# main program
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input("Website URL: ")

if len(sys.argv) > 2:
    depth = sys.arg[2]
else:
    depth = int(input("Search Depth: "))

#remember that slice ranges have an excluded upper bound
if url[0:4] != "http":
    print("Invalid input; please pass a url in the form of http(s)://________")
    exit(0)

print("Site to scrape: \"" + url + "\"" + "...\n")

# this will go in "depth" levels deep into subdirectories and add to list of emails
emails = scrapeSubPages(url, depth)
print(emails)
