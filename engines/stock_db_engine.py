#!/usr/bin/python

import MySQLdb as mdb
import urllib2
import time
import sys


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    i = 1
    prefix = "http://finance.yahoo.com/d/quotes.csv?s="

    stmt = """INSERT INTO greed.stock
            (symbol, company) VALUES (\"%s\", \"%s\")
            ON DUPLICATE KEY UPDATE symbol = symbol;"""

    con = connect()
    cur = con.cursor()

    while i < 16:
        url = prefix

        s = open("./stocklists/stock" + str(i), "r")
        for stock in s.readlines():
            url += str(stock).strip() + '+'

        url = url[:-1] + "&f=sn"

        content = (urllib2.urlopen(url)).read()
        splicelist = content.split("\n")

        for quote in splicelist:
            if quote:
                val = quote.split("\",\"")
                symb = (str(val[0])[1:]).strip()
                comp = (str(val[1])[:-2]).strip()
                cur.execute(stmt % (symb, comp))

        i = i + 1

    if con:
        con.commit()
        con.close()


if __name__ == "__main__":
    sys.exit(main())