import urllib2

class RealtimeData:
    def __init__(self):
        self.prefix = "http://finance.yahoo.com/d/quotes.csv?s="

    def get(self):
        i = 1

        while i < 16:
            url = self.prefix

            s = open("./stocklists/stock" + str(i), "r")
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

            print retlist[:-1]

            i = i + 1
        return


if __name__ == "__main__":
    c = RealtimeData()

    c.get()