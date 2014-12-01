#!/usr/bin/python

import MySQLdb as mdb
import sys
import datetime
import pdb


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def tuple_to_str(ret):
        return (str(ret).split('L')[0])[1:]


def main():
    print sys.argv[1:]

    opt = ''

    if((sys.argv[1:]) and (sys.argv[1:][0] in ['-np', '-ncp', '-b', '-s', '-fsup'])):
            opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-np':
        new_portfolio(sys.argv[1:][1])
    elif opt == '-ncp':
        new_comp_portfolio(sys.argv[1:][1], sys.argv[1:][2])
    elif opt == '-b':
        buy_stock(sys.argv[1:][1], sys.argv[1:][2], sys.argv[1:][3])
    elif opt == '-s':
        sell_stock(sys.argv[1:][1], sys.argv[1:][2], sys.argv[1:][3])
    elif opt == '-fsup':
        find_super_portfolio(sys.argv[1:][1])
    elif opt == '-h':
        print("""-np PID                      Create portfolio for super_portfolio PID""")
        print("""-ncp PIDCOMPETITION_ID      Create competition portfolio for super_portfolio PID""")
        print("""-b PID STOCK_ID #STOCKS      Buy #STOCKS number of stock STOCK_ID for super_portfolio PID""")
        print("""-s PID STOCK_ID #STOCKS      Sell #STOCKS number of stock STOCK_ID for super_portfolio PID""")
        print()
        print("""-fsup PORTFOLIO_NAME             Get id of super_portfolio PORTFOLIO_NAME (DEBUGGING)""")


def new_portfolio(pid):
    print "new_portfolio(", pid, ")"

    try:
        con = connect()
        cur = con.cursor()

#sub_portfolio lacks "portfolio_name" field
        statement = """INSERT INTO sub_portfolio
                    (super_portfolio_id) VALUE (%i)""", (pid)
        cur.execute(statement)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

    try:
        con = connect()
        cur = con.cursor()

        statement = """INSERT INTO sub_portfolio
                    (account_id, name, initial_cash)
                    VALUES('%i', '%s', 100000);""" % (uid, pname)
        cur.execute(statement)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return find_super_portfolio(pname)


def new_comp_portfolio(pid, compid):
    print "new_comp_portfolio(", pid, ", ", compid, ")"

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT cash FROM portfolio_value_cash
            WHERE id = %i;""" % (pid)
        cur.execute(stmt)
        cash = float(tuple_to_str(cur.fetchone()))

        stmt = """SELECT entryfee FROM competition
            WHERE id = %i;'""" % compid
        cur.execute(stmt)
        fee = float(tuple_to_str(cur.fetchone()))

        if(cash < fee):
            print "Not enough cash to enter competition"
            return -1

        stmt = """INSERT INTO sub_portfolio
                    (super_portfolio_id, competition_id)
                    VALUE (%i, %i);""", (pid, compid)
        cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def buy_stock(pid, stock_id, num_stocks):
    print "buy_stock(", pid, ", ", stock_id, ", ", num_stocks, ")"

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT value FROM stock_value_latest
                WHERE stock_symbol = '%s';""" % (stock_id)
        cur.execute(stmt)
        stock_val = float(tuple_to_str(cur.fetchone())) * num_stocks

        stmt = """SELECT cash FROM portfolio_value_cash
                WHERE id = %i;""" % (pid)
        cur.execute(stmt)
        cash = float(tuple_to_str(cur.fetchone()))

        if (stock_val > cash):
            print ("Insufficient Funds")
            return -1

        stmt = """INSERT INTO transaction
                (sub_portfolio_id, unixtime, stock_symbol, stock_count, type)
                VALUE (%i, """ + datetime.datetime.now().time() + """'%s',%i,b);
                    """ % (pid, stock_id, num_stocks)
        cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def sell_stock(pid, stock_id, num_stocks):
    print "sell_stock(", pid, ", ", stock_id, ", ", num_stocks, ")"

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT stock_count FROM portfolio_stocks
                WHERE id = %i;""" % (pid)
        cur.execute(stmt)
        owned = int(tuple_to_str(cur.fetchone()))

        if (owned < num_stocks):
            print ("Cannot Sell More Stocks than are Owned")
            return -1

        stmt = """INSERT INTO transaction
                (sub_portfolio_id, unixtime, stock_symbol, stock_count, type)
                VALUE (%i, """ + datetime.datetime.now().time() + """'%s',%i,s);
                    """ % (pid, stock_id, num_stocks)
        cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def find_super_portfolio(pname):
    try:
        con = connect()
        cur = con.cursor()

        statement = """SELECT id FROM super_portfolio
                    WHERE name = '%s';""" % (pname)
        cur.execute(statement)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return int(tuple_to_str(cur.fetchone()))
#Testing
        #pid = tuple_to_int(cur.fetchone())
        #print pname, "    ==    ", pid

        #return pid


if __name__ == "__main__":
    sys.exit(main())
