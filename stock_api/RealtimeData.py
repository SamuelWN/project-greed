import urllib2
import time

class RealtimeData:
    def __init__(self):
        self.prefix = "http://finance.yahoo.com/d/quotes.csv?s="

    def get(self):
        for filenum in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15"]:
            url = self.prefix

            s = open("./stocklists/stock" + filenum, "r")
            for stock in s.readlines():
                url += str(stock).strip() + '+'

            url = url[:-1] + "&f=ap"

            content = (urllib2.urlopen(url)).read()

            retlist = ''
            splicelist = content.split("\n")

            for quote in splicelist:
                quotelist = quote.split(',')
                if quote:
                    if (quotelist[0] != 'N/A'):
                        retlist += quotelist[0]
                    else:
                        retlist += quotelist[1].strip()

                    retlist += ','

            time.sleep(5)

            print retlist[:-1]
        return


if __name__ == "__main__":
    c = RealtimeData()

    c.get()