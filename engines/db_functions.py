#!/usr/bin/python
import sys
import MySQLdb as mdb
import json


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    if((sys.argv[1:]) and
    (sys.argv[1:][0] in ['-a', '-d', '-j', '-A', '-m', '-e'])):
        opt = sys.argv[1:][0]

    if(opt == '-pcv'):
        print portfolio_cash_value(int(sys.argv[1:][1]), float(sys.argv[1:][2]))
    if(opt == '-pcrv'):
        print portfolio_competition_reserved_value(int(sys.argv[1:][1]), float(sys.argv[1:][2]), int(sys.argv[1:][3]))
    if(opt == '-psc'):
        print portfolio_stock_count(int(sys.argv[1:][1]), float(sys.argv[1:][2]), sys.argv[1:][3])
    if(opt == '-psv'):
        print portfolio_stock_value(int(sys.argv[1:][1]), float(sys.argv[1:][2]), sys.argv[1:][3], float(sys.argv[1:][4]))


def portfolio_cash_value(pid, utime):
    pcv = -1.00
    try:
        con = connect()
        cur = con.cursor()

        stmt = "select greed.portfolio_cash_value(%i, '%f')" % (pid, utime)

        cur.execute(stmt)
        pcv = float(cur.fetchone()[0])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'portfolio_cash_value':pcv})


def portfolio_competition_reserved_value(pid, utime, future):
    pcrv = -1.00

    try:
        con = connect()
        cur = con.cursor()

        stmt = """select
         greed.portfolio_competition_reserved_value
         (%i, '%f', '%i');""" % (pid, utime, future)

        cur.execute(stmt)
        pcrv = float(cur.fetchone()[0])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'portfolio_competition_reserved_value':pcrv})


def portfolio_stock_count(pid, utime, stock):
    psc = -1

    try:
        con = connect()
        cur = con.cursor()

        stmt = """select greed.portfolio_stock_count
            (%i, '%f', '%s')""" % (pid, utime, stock)

        cur.execute(stmt)
        psc = int(cur.fetchone()[0])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'portfolio_stock_count':psc})


def portfolio_stock_value(pid, utime, symbl, stockval):
    psv = -1.00
    try:
        con = connect()
        cur = con.cursor()

        stmt = """greed.portfolio_stock_value
            (%i, '%f', '%s', %i);
            """ % (pid, utime, symbl, stockval)
        cur.execute(stmt)

        psv = float(cur.fetchone()[0])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'portfolio_stock_value':psv})


if __name__ == "__main__":
    sys.exit(main())