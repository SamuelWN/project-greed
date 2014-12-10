#!/usr/bin/python

import MySQLdb as mdb
import sys
import time
#from datetime import datetime
import pdb


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def tuplestocsv(val_list):
    ret = ""
    for vals in val_list:
        for val in vals:
            if(val is not None):
                ret += str(val) + ','

        ret = ret[:-1]
        ret += "\n"

    return ret[:-1]


def main():
    #print sys.argv[1:]

    opt = ''

    if((sys.argv[1:]) and (sys.argv[1:][0] in
    ['-np', '-ncp', '-b', '-s', '-fsu', '-fs', '-fc', '-fstd', '-fA'])):
        opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-np':
        new_portfolio(int(sys.argv[1:][1]))
    elif opt == '-ncp':
        print new_comp_portfolio(int(sys.argv[1:][1]), int(sys.argv[1:][2]))
    elif opt == '-b':
        buy_stock(int(sys.argv[1:][1]), sys.argv[1:][2], int(sys.argv[1:][3]))
    elif opt == '-s':
        sell_stock(int(sys.argv[1:][1]), sys.argv[1:][2], int(sys.argv[1:][3]))
    elif opt == '-fsu':
        print find_super_portfolios_uname(sys.argv[1:][1])
    elif opt == '-fs':
        print find_super_portfolios_id(int(sys.argv[1:][1]))
    elif opt == '-fc':
        print find_comp_portfolios(sys.argv[1:][1])
    elif opt == '-fstd':
        print find_std_sub_portfolios(int(sys.argv[1:][1]))
    elif opt == '-fA':
        print find_all(int(sys.argv[1:][1]))
    elif opt == '-h':
        print("""-np PID
            Create portfolio for super-portfolio PID\n""")
        print("""-ncp PID COMPETITION_ID
            Create competition portfolio for super-portfolio PID\n""")
        print("""-b PID STOCK #STOCKS
            Buy #STOCKS number of stock STOCK for sub-portfolio PID\n""")
        print("""-s PID STOCK #STOCKS
            Sell #STOCKS number of stock STOCK for sub-portfolio PID\n""")
        print("""-fsU UNAME
            Get all super-portfolios for user by username\n""")
        print("""-fs UID
            Get all super-portfolios for user UID\n""")
        print("""-fc UID
            Get all competition portfolios for user UID\n""")
        print("""-fstd UID
            Get all standard (non-competition) sub-portfolios for user UID""")
        print("""-fA UID
            Get all sub-portfolios for user UID\n""")


def new_portfolio(pid):
    #print "new_portfolio(", pid, ")"

    try:
        con = connect()
        cur = con.cursor()

        statement = """INSERT INTO sub_portfolio
                    (super_portfolio_id) VALUE (%i)""" % (pid)
        cur.execute(statement)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def new_comp_portfolio(pid, compid):
    #print "new_comp_portfolio(", pid, ", ", compid, ")"
    cpid = -1
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT EXISTS (
            SELECT * FROM greed.sub_portfolio
            WHERE super_portfolio_id = %i
            AND competition_id = %i
            );""" % (pid, compid)
        cur.execute(stmt)
        cpid = int(cur.fetchone()[0])

        if (cpid == 0):
            stmt = """SELECT cash FROM greed.portfolio_value_cash
                WHERE id = %i;""" % (pid)
            cur.execute(stmt)
            cash = float(cur.fetchone()[0])

            print "stmt = \n    " + stmt + "\n"
            cur.execute(stmt)
            print "stmt executed\n"

            cur.close()
            cur = con.cursor()

            stmt = """SELECT entryfee FROM greed.competition
                WHERE id = %i;""" % (compid)
            cur.execute(stmt)
            fee = float(cur.fetchone()[0])

            cur.execute(stmt)

            if(cash < fee):
                print "Not enough cash to enter competition"
            else:
                stmt = """INSERT INTO greed.sub_portfolio
                    (super_portfolio_id, competition_id)
                    VALUE (%i, %i);""" % (pid, compid)

                cur.execute(stmt)

                stmt = """SELECT LAST_INSERT_ID();"""
                cur.execute(stmt)
                cpid = cur.fetchone()[0]
        else:
            stmt = """SELECT id FROM greed.sub_portfolio
            WHERE super_portfolio_id = %i
            AND competition_id = %i;""" % (pid, compid)
            cur.execute(stmt)
            cpid = cur.fetchone()[0]
    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return cpid


def buy_stock(pid, stock_id, num_stocks):
    #print "buy_stock(", pid, ", ", stock_id, ", ", num_stocks, ")"

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT value FROM stock_current
                WHERE stock_symbol = '%s';""" % (stock_id)
        cur.execute(stmt)
        stock_val = float(cur.fetchone()[0]) * num_stocks

        stmt = """SELECT cash FROM portfolio_value_cash
                WHERE id = %i;""" % (pid)
        cur.execute(stmt)
        cash = float(cur.fetchone()[0])

        if (stock_val > cash):
            print ("Insufficient Funds")
        else:
            stmt = """INSERT INTO transaction
                (sub_portfolio_id, unixtime, stock_symbol, stock_count, stock_value, type)
                VALUE (%i, %f, '%s', %i,
                    (SELECT value FROM greed.stock_current
                    WHERE stock_symbol = '%s'),
                'p');""" % (pid, time.time(), stock_id, num_stocks, stock_id)
            cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def sell_stock(pid, stock_id, num_stocks):
    #print "sell_stock(", pid, ", ", stock_id, ", ", num_stocks, ")"

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT stock_count FROM portfolio_stocks
                WHERE id = %i;""" % (pid)
        cur.execute(stmt)
        owned = int(cur.fetchone()[0])

        if (owned < num_stocks):
            print ("Cannot Sell More Stocks than are Owned")
        else:
            stmt = """INSERT INTO transaction
                (sub_portfolio_id, unixtime, stock_symbol, stock_count, stock_value, type)
                VALUE (%i, %f, '%s', %i,
                    (SELECT value FROM greed.stock_current
                    WHERE stock_symbol = '%s'),
                's');""" % (pid, time.time(), stock_id, num_stocks, stock_id)
            cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def find_super_portfolios_id(uid):
    ret = ""
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT * FROM super_portfolio
                WHERE id  = %i;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            ret = tuplestocsv(folios)
            #print ret

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

    return ret


def find_super_portfolios_uname(uname):
    ret = ""
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id FROM account
                WHERE username = '%s';""" % (uname)

        cur.execute(stmt)
        uid = cur.fetchone()

        if(uid is not None):
            ret = find_super_portfolios_id(int(uid[0]))

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return ret


def find_comp_portfolios(uid):
    ret = ""
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id, competition_id FROM sub_portfolio
                WHERE super_portfolio_id  = %i AND competition_id IS NOT NULL;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            ret = tuplestocsv(folios)
            #print ret

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return ret


def find_std_sub_portfolios(uid):
    ret = ""
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id FROM sub_portfolio
                WHERE super_portfolio_id  = %i AND competition_id IS NULL;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            ret = tuplestocsv(folios)
            #print ret

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return ret


def find_all(uid):
    ret = ""
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT * FROM sub_portfolio
                WHERE id  = %i;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            ret = tuplestocsv(folios)
            #print ret

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return ret


if __name__ == "__main__":
    sys.exit(main())