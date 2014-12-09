#!/usr/bin/python

import urllib2
import sys
#import pdb
import re as regex

################################################################################
# Stock Fetching Error:                                                        #
#    Turns out that the errors were not due to improperly regex-ing (albeit,   #
#    I did find some regex-errors during testing), but were instead caused by  #
#    data not being available for certain stocks at certain times. (Error 404) #
#                                                                              #
# Note:                                                                        #
#    Queries for:                                                              #
#    GOOG    don't work for dates prior to: 2014-03-27                         #
#    ZZ      don't work for dates after:    2013-03-18                         #
#                                                                              #
#    (MSFT stock seems to work properly for every query I did... so I should   #
#    probably use a different ticker symbol for testing...)                    #
################################################################################


class HistoricalData:
    def __init__(self):
        self.prefix = "http://ichart.finance.yahoo.com/table.csv?s="

    def get(self, symbol, syear, smonth, sday, eyear, emonth, eday):
        url = self.prefix + symbol + "&a=" + str(smonth) + "&b=" + str(sday)
        url = url + "&c=" + str(syear) + "&d=" + str(emonth) + "&e="
        url = url + str(eday) + "&f=" + str(eyear) + "&g=d"

        print "url:\n %s \n" % (url)

        try:
            u = urllib2.urlopen(url)
            content = u.read()
        except urllib2.HTTPError as e:
            print "Error " + str(e.code)
            content = None
        finally:
            return content


def main(symbl, syear, smon, sday, eyear, emon, eday):
    c = HistoricalData()

    quote = c.get(symbl, syear, smon, sday, eyear, emon, eday)

    if (quote is None):
        sys.exit(1)

    quotelist = regex.findall('[0-9]{4}-[0|1][0-9]-[0-3][0-9],[0-9]+.[0-9]{2},[0-9]+.[0-9]{2},[0-9]+.[0-9]{2}', quote)

    retcsv = ""

    for dayprice in quotelist:
        val = dayprice.split(",")
        retcsv += val[0] + "," + val[3] + "\n"

    return retcsv


if __name__ == "__main__":
    if(len(sys.argv[1:]) == 7):
        symbl = sys.argv[1:][0]
        syear = int(sys.argv[1:][1])
        smon = int(sys.argv[1:][2]) - 1
        sday = int(sys.argv[1:][3])
        eyear = int(sys.argv[1:][4])
        emon = int(sys.argv[1:][5]) - 1
        eday = int(sys.argv[1:][6])

        print main(symbl, syear, smon, sday, eyear, emon, eday)
        sys.exit(1)

    elif(len(sys.argv[1:]) == 4):
        symbl = sys.argv[1:][0]
        year = int(sys.argv[1:][1])
        mon = int(sys.argv[1:][2]) - 1
        day = int(sys.argv[1:][3])

        print main(symbl, year, mon, day, year, mon, day)
    else:
        print """Syntax:
    To query a specific date:
        HistoricalStockData.py SYMBL YEAR MONTH DAY

    To query a range:
        HistoricalStockData.py SYMBL SYEAR SMONTH SDAY EYEAR EMONTH EDAY

Symbol Meaning:
    SYMBL             Stock ticker symbol
    SYEAR             Year at which to begin getting stock data
    SMONTH              Month at which to begin getting stock data
    SDAY              Day at which to begin getting stock data
    EYEAR             Year at which to stop getting stock data
    EMONTH              Month at which to stop getting stock data
    EDAY              Day at which to stop getting stock data
"""
    sys.exit(1)