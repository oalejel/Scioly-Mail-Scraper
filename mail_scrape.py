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

    def handle_starttag(self, tag, attrs):
        print("encountered a start tag: " + tag)

    def handle_endtag(self, tag):
        print("end of tag: " + tag)

    def handle_data(self, data):
        print("data: " + data)

def parsePage(page):
    for line in page.readlines():
        print(line)
    pass

#main code
scrapeParser = HTMLParser()
topPage = request.urlopen(url)

parsePage(topPage)
# scrapeParser.feed(str(topPage.read()))4

# print(str(topPage.read()))
