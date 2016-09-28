__author__ = 'Sasa2905'
# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse
import pandas as pd

unique_words_main = {}
unique_words_websites = {}
# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):
    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        if tag == "a" :
            for (key, value) in attrs:
                if key == 'href':
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    newUrl = parse.urljoin(self.baseUrl, value)
                    # And add it to our colection of links:
                    self.links = self.links + [newUrl]

    def handle_data(self, data):
        if "\n" not in data and "\r" not in data and "function" not in data:
            stripped = data.strip().lower().replace("!", "").replace("?", "").replace(".","");
            for e in stripped.split(" "):
                if len(e) > 4:
                    value = unique_words_websites.get(e)
                    if value is None:
                        unique_words_websites[e] = 1



    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.links = []
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        # JavaScript files, CSS, or .PDFs for example)
        htmlBytes = response.read()
        # Note that feed() handles Strings well, but not bytes
        # (A change from Python 2.x to Python 3.x)
        htmlString = htmlBytes.decode("utf-8")
        self.feed(htmlString)
        return htmlString, self.links

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, maxPages):
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    listlinks = url
    parser = LinkParser()
    dataframe = pd.DataFrame()
    for i in listlinks:
        pagesToVisit = [i]
        numberVisited = 0
        while numberVisited < maxPages and pagesToVisit != []:
            numberVisited = numberVisited + 1
            # Start from the beginning of our collection of pages to visit:
            url = pagesToVisit[0]
            pagesToVisit = pagesToVisit[1:]
            try:
                print(numberVisited, "Visiting:", url)
                data, links = parser.getLinks(url[0])
                #print(data.replace("\n", "").split(">"))
                # Add the pages that we visited to the end of our collection
                # of pages to visit:
                pagesToVisit = pagesToVisit + links
                print(" **Success!**")
            except Exception as e:
                print(e)
        converttomain()
        unique_words_websites.clear()
    dataframe = pd.DataFrame.from_dict(unique_words_main,orient='index')
    print(dataframe.sort_values(0,ascending=False))

def converttomain():
       if len(unique_words_main) is 0:
            unique_words_main.update(unique_words_websites)
       else:
            for e in unique_words_websites:
                value = unique_words_main.get(e)
                if value is not None:
                    value = value + 1
                    unique_words_main[e] = value
                else:
                    unique_words_main[e] = 1





#linklist = ["http://www.digitalspy.com/fun/news/a444700/longest-word-has-189819-letters-takes-three-hours-to-pronounce/","https://www.mediamarkt.nl", "https://www.bol.com","https://www.thuisbezorgd.nl","https://www.hotels.nl","https://www.weekendjeweg.nl"]
data = pd.read_csv("webshops.csv")
linklist = data[::50].as_matrix()
#print(len(linklist))
spider(linklist, 1)