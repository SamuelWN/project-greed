import urllib2
import time
import csv
import pdb


class HistoricalData:
    def __init__(self):
        self.prefix = "http://ichart.finance.yahoo.com/table.csv?s="

    def get(self, symbol, syear, smonth, sday, eyear, emonth, eday):
        url = self.prefix + symbol + "&a=" + str(smonth) + "&b=" + str(sday)
        url = url + "&c=" + str(syear) + "&d=" + str(emonth) + "&e="
        url = url + str(eday) + "&f=" + str(eyear) + "&g=d"

        u = urllib2.urlopen(url)
        content = u.read()

        return content


if __name__ == "__main__":
    c = HistoricalData()

    '''NOTE:
        Month value = Month-1
        (i.e. Jan = 0, Feb = 1 ... Nov = 10, Dec = 11) '''
    #             SYMBL,  YEAR, M, D,  YEAR, M, D
    quote = c.get("MSFT", 2000, 2, 15, 2010, 0, 31)

    quotes = quote.splitlines()

    import re as regex

    quotelist = regex.findall('[0-9]{4}-[0|1][0-9]-[0-3][0-9],[0-9]{2}.[0-9]{2},[0-9]{2}.[0-9]{2},[0-9]{2}.[0-9]{2}', quote)
    #print quotelist

    retlist = []

    for aquote in quotelist:
        val = aquote.split(",")
        retlist.append((val[0], float(val[3])))

    print retlist