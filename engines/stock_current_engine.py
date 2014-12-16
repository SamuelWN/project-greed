#!/usr/bin/python

import MySQLdb as mdb
import urllib2
import time


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    i = 1
    price = 0.0
    prefix = "http://finance.yahoo.com/d/quotes.csv?s="
    stmt = """INSERT INTO greed.stock_current (stock_symbol, value)
            VALUES ('%s', %f)
            ON DUPLICATE KEY UPDATE value = %f;"""

    con = connect()
    cur = con.cursor()

    while i < 16:
        url = prefix

        s = open("./stocklists/stock" + str(i), "r")
        for stock in s.readlines():
            url += str(stock).strip() + '+'

        url = url[:-1] + "&f=sap"

        content = (urllib2.urlopen(url)).read()
        splicelist = content.split("\n")

        for quote in splicelist:
            if quote:
                val = quote.split(',')
                symb = str(val[0])[1:-1]

                if (val[1].strip() != 'N/A'):
                    price = float(val[1])
                    cur.execute(stmt % (symb, price, price))
                elif (val[2].strip() != 'N/A'):
                    price = float(val[2].strip())
                    cur.execute(stmt % (symb, price, price))

                con.commit()
        i = i + 1

# Re-aquire stock data every hour:
    time.sleep(3600)
    main()


if __name__ == "__main__":
    main()