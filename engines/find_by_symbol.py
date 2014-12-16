#!/usr/bin/python
import sys
import MySQLdb as mdb
import json


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main(term):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT * FROM greed.stock
                WHERE (symbol = '""" + term + """');"""

        cur.execute(stmt)
        results = cur.fetchall()
        stmt = """SELECT value FROM greed.stock_current
                WHERE stock_symbol = '%s'"""

        for a_res in results:
            cur.execute(stmt % a_res[0])
            jsonlist.append({'symbol':a_res[0], 'company':a_res[1], 'value':float(cur.fetchone()[0])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


if __name__ == "__main__":
    print main(sys.argv[1:][0])

    sys.exit(1)
