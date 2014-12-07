import urllib2
import sys
#import pdb


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
    if(len(sys.argv[1:]) != 7):
        if(len(sys.argv[1:]) < 7):
            print "\nNot Enough Arguments!!!"
        else:
            print "\nToo Many Arguments!!!"

        print """
Syntax:
    HistoricalStockData.py SYMBL SYEAR SMON SDAY EYEAR EMON EDAY
Symbol Meaning:
    SYMBL             Stock ticker symbol
    SYEAR             Year at which to begin getting stock data
    SMON              Month at which to begin getting stock data
    SDAY              Day at which to begin getting stock data
    EYEAR             Year at which to stop getting stock data
    EMON              Month at which to stop getting stock data
    EDAY              Day at which to stop getting stock data


!!!NOTE!!!
For SMON & EMON:
    Value = Month# - 1
    (i.e. Jan = 0, Feb = 1 ... Nov = 10, Dec = 11)
    """
        sys.exit(1)
    ##################################################
    ###############       END IF       ###############
    ##################################################

    c = HistoricalData()

    symbl = sys.argv[1:][0]
    syear = int(sys.argv[1:][1])
    smon = int(sys.argv[1:][2])
    sday = int(sys.argv[1:][3])
    eyear = int(sys.argv[1:][4])
    emon = int(sys.argv[1:][5])
    eday = int(sys.argv[1:][6])

    prefix = "http://ichart.finance.yahoo.com/table.csv?s="

    url = prefix + symbl + "&a=" + str(smon) + "&b=" + str(sday)
    url = url + "&c=" + str(syear) + "&d=" + str(emon) + "&e="
    url = url + str(eday) + "&f=" + str(eyear) + "&g=d"

    u = urllib2.urlopen(url)
    quotes = u.read()

    #quote = c.get(symbl, syear, smon, sday, eyear, emon, eday)

    quotes = quotes.splitlines()

    import re as regex

    print quotes
    quotelist = regex.findall('[0-9]{4}-[0|1][0-9]-[0-3][0-9],[0-9]{2}.[0-9]{2},[0-9]{2}.[0-9]{2},[0-9]{2}.[0-9]{2}', quotes)

    retcsv = ""

    for dayprice in quotelist:
        val = dayprice.split(",")
        retcsv += val[0] + "," + val[3] + "\n"

    #print retcsv