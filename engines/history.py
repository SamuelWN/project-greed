#!/usr/bin/python
import sys
import MySQLdb as mdb
import json


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main(pid, utime):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        cur.execute("call greed.history('%i', '%i')" % (pid, utime))
        hist = cur.fetchall()

        for info in hist:
            jsonlist.append({'unixtime':int(info[0]), 'cash_value':float(info[1]), 'comp_value':float(info[2]), 'stock_count':str(info[3])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        return json.dumps(jsonlist)


if __name__ == "__main__":
    print main(int(sys.argv[1:][0]), int(sys.argv[1:][1]))

    sys.exit(1)
