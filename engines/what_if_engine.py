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
    pid = int(sys.argv[1:][1])
    symbl = sys.argv[1:][2]
    syear = int(sys.argv[1:][3])
    smon = int(sys.argv[1:][4])
    sday = int(sys.argv[1:][5])

    if(len(sys.argv) == 8):
        eyear = int(sys.argv[1:][6])
        emon = int(sys.argv[1:][7])
        eday = int(sys.argv[1:][8])
    elif (len(sys.argv) == 5):
        eyear = emon = eday = None
    else:
        print "Improper Input"
        sys.exit(0)

    print create_new(pid, symbl, syear, smon, sday, eyear, emon, eday)


def create_new(pid, symbl, syear, smon, sday, eyear, emon, eday):
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT value_stock, value_cash, value_total
                FROM greed.portfolio_value_total
                WHERE id = %i;""" % (pid)

        cur.execute(stmt)
        folio = cur.fetchone()
        pstocks = folio[0]
        pcash = folio[1]
        ptotal = folio[2]

        buy = HistoricalStockData.main(symbl, syear, smon, sday).split(',')[1]

        if ((eyear is not None) and (emon is not None) and (eday is not None)):
            sell = HistoricalStockData.main(symbl, eyear, emon, eday).split(',')[1]

            valsale = float(sell) - float(buy)
            pcash = pcash + valsale
            ptotal = ptotal + valsale

        else:
            stmt = """SELECT value
                      FROM greed.stock_current
                      WHERE stock_symbol = '%s';""" % (symbl)

            cur.execute(stmt)
            valstocks = float(cur.fetchone()[0])
            pstocks = pstocks + valstocks

        return str(pstocks) + ',' + str(pcash) + ',' + str(ptotal)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


if __name__ == "__main__":
    sys.exit(main())