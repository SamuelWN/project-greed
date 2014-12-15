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
                WHERE
                    (symbol LIKE '%""" + term + """%')
                OR
                    (company LIKE '%""" + term + """%');"""

        cur.execute(stmt)
        results = cur.fetchall()

        for a_res in results:
            jsonlist.append({'symbol':a_res[0], 'company':a_res[1]})

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
