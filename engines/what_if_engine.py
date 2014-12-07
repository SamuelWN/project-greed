#!/usr/bin/python

import sys
import time
import datetime
import MySQLdb as mdb
import portfolio_engine
import HistoricalStockData


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    if((sys.argv[1:]) and (sys.argv[1:][0]
    in ['-a', '-f'])):
        opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-a':
        print create_new(int(sys.argv[1:][1]), sys.argv[1:][2],
                int(sys.argv[1:][1]), int(sys.argv[1:][1]),
                int(sys.argv[1:][1]), int(sys.argv[1:][1]),
                int(sys.argv[1:][1]), int(sys.argv[1:][1]))


def stock_sum(stocks):
    ret_sum = 0

    for val in stocks:
        ret_sum = ret_sum + int(val[1])

    return ret_sum

def create_new(pid, symbl, syear, smon, sday, eyear, emon, eday):
    val_sum = 0

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT unixtime, type
                FROM greed.transaction
                WHERE stock_symbol = """ + symbl + """
                ORDER BY unixtime DESC;"""

        cur.execute(stmt)
        preowned = cur.fetchall()


        smon += 1
        emon += 1

        startstr = str(smon) + "/" + str(sday) + "/" + str(syear)
        endstr = str(emon) + "/" + str(eday) + "/" + str(eyear)

        utcstart = time.mktime(datetime.datetime.strptime(startstr).timetuple())
        utcend = time.mktime(datetime.datetime.strptime(endstr).timetuple())

        if(preowned is not None):
            for trans in preowned:
                if(trans[0] < utcend):
                    if(trans[1] == 's'):
                        fetch = time.strftime("%D", time.unixtime(trans[0])).split("/")

                        todate = HistoricalStockData.main(symbl, int(fetch[2]), int(fetch[1]) - 1, fetch[0], eyear, emon, eday)

                        val_sum = val_sum + float(todate[-1][1]) - float(todate[0][1])
        else:
            stocklist = HistoricalStockData.main(symbl, syear, smon, sday, eyear,emon, eday)
            val_sum = val_sum + float(stocklist[-1][1]) - float(stocklist[0][1])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


if __name__ == "__main__":
    sys.exit(main())