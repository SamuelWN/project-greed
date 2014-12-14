#!/usr/bin/python
import sys
import MySQLdb as mdb
import json


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main(pid):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        cur.execute("call greed.allstocks('%i')" % pid)
        stocks = cur.fetchall()

        for info in stocks:
            jsonlist.append({'symbol':str(info[0]), 'company':str(info[1]), 'current_value':float(info[2])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        return json.dumps(jsonlist)


if __name__ == "__main__":
    print main(int(sys.argv[1:][0]))

    sys.exit(1)
