import urllib2
#import pdb

class RealtimeData:
    def __init__(self):
        self.prefix = "http://finance.yahoo.com/d/quotes.csv?s="

    def get(self, symbol):
        url = self.prefix + symbol + "&f=na"

        content = (urllib2.urlopen(url)).read()

        retlist = content.split(",")
        retlist[1] = (retlist[1].strip())

        return retlist


if __name__ == "__main__":
    c = RealtimeData()

    ret = c.get("MSFT")

    print ret