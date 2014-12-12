#!/usr/bin/python
import sys
import MySQLdb as mdb


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main(term):
    results = ''
    ret = ""

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT * FROM greed.stock
                WHERE
                    (symbol LIKE '%""" + term + """"%')
                OR
                    (company LIKE '%""" + term + """%');"""

        cur.execute(stmt)
        results = cur.fetchall()

        for a_res in results:
            ret = ret + a_res[0] + "," + a_res[1] + '\n'

        ret = ret[:-1]
    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return ret


if __name__ == "__main__":
    if(sys.argv[1:]):
        term = sys.argv[1:][0]

    print main(term)
    sys.exit(1)
