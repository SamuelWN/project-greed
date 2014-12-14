#!/usr/bin/python

import MySQLdb as mdb
import sys
import time
import json
#import pdb


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
    ['-np', '-dp', '-nsp', '-dsp', '-ncp', '-dcp' '-b', '-s', '-fsu', '-fs', '-fc', '-fstd', '-fsv', '-fA'])):
        opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-np':
        new_portfolio(int(sys.argv[1:][1]))
    elif opt == '-nsp':
        new_portfolio(int(sys.argv[1:][1]))
    elif opt == '-dp':
        delete_portfolio(int(sys.argv[1:][1]))
    elif opt == '-dsp':
        new_portfolio(int(sys.argv[1:][1]))
    elif opt == '-ncp':
        print new_comp_portfolio(int(sys.argv[1:][1]), int(sys.argv[1:][2]))
    elif opt == '-dcp':
        print delete_comp_portfolio(int(sys.argv[1:][1]), int(sys.argv[1:][2]))
    elif opt == '-b':
        buy_stock(int(sys.argv[1:][1]), sys.argv[1:][2], int(sys.argv[1:][3]))
    elif opt == '-s':
        sell_stock(int(sys.argv[1:][1]), sys.argv[1:][2], int(sys.argv[1:][3]))
    elif opt == '-fsu':
        print find_super_portfolios_uname(sys.argv[1:][1])
    elif opt == '-fs':
        print find_super_portfolios_id(int(sys.argv[1:][1]))
    elif opt == '-fc':
        print find_comp_portfolios(int(sys.argv[1:][1]))
    elif opt == '-fstd':
        print find_std_sub_portfolios(int(sys.argv[1:][1]))
    elif opt == '-fA':
        print find_all(int(sys.argv[1:][1]))
    elif opt == '-fsv':
        print find_sup_vals(int(sys.argv[1:][1]))
    elif opt == '-h':
        print("""-nsp UID NAME CASH
            Create portfolio for account UID of name NAME with initial cash CASH\n""")
        print("""-dsp SPID
            Dele super_portfolio of id SPID\n""")
        print("""-np SPID
            Create portfolio for super-portfolio SPID\n""")
        print("""-dp PID
            Delete sub_portfolio of id PID\n""")
        print("""-ncp SPID COMPETITION_ID
            Create competition portfolio for super-portfolio SPID\n""")
        print("""-dcp CPID
            Delete competition portfolio CPID\n""")
        print("""-b PID STOCK #STOCKS
            Buy #STOCKS number of stock STOCK for sub-portfolio PID\n""")
        print("""-s PID STOCK #STOCKS
            Sell #STOCKS number of stock STOCK for sub-portfolio PID\n""")
        print("""-fsv UID
            Get the total value for all subportfolios assocated with user UID\n""")
        print("""-fsU UNAME
            Get all super-portfolios for user by username UNAME\n""")
        print("""-fs UID
            Get all super-portfolios for user by user id UID\n""")
        print("""-fc SPID
            Get all competition portfolios for user UID\n""")
        print("""-fstd SPID
            Get all standard (non-competition) sub-portfolios for super_portfolio_id SPID\n""")
        print("""-fA SPID
            Get all sub_portfolios for super_portfolio_id SPID\n""")


def new_super_portfolio(uid, name, cash):
    #print "new_portfolio(", pid, ")"

    try:
        con = connect()
        cur = con.cursor()

        statement = """INSERT INTO super_portfolio
                    (account_portfolio_id, name, initial_cash)
                    VALUE (%i, '%s', %f)
                    """ % (uid, name, cash)
        cur.execute(statement)

        stmt = "SELECT LAST_INSERT_ID();"
        cur.execute(stmt)
        pid = cur.fetchone()[0]

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return pid


def delete_super_portfolio(spid):
    try:
        con = connect()
        cur = con.cursor()

        stmt = """DELETE FROM greed.sub_portfolio
                WHERE id = %i;""" % (spid)
        cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def new_portfolio(spid):
    #print "new_portfolio(", pid, ")"
    pid = -1
    try:
        con = connect()
        cur = con.cursor()

        stmt = """INSERT INTO sub_portfolio
                (super_portfolio_id) VALUE (%i)""" % (spid)
        cur.execute(stmt)

        stmt = "SELECT LAST_INSERT_ID();"
        cur.execute(stmt)
        pid = cur.fetchone()[0]

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return pid


def delete_portfolio(pid):
    try:
        con = connect()
        cur = con.cursor()

        stmt = """DELETE FROM greed.sub_portfolio
                WHERE id = %i;""" % (pid)
        cur.execute(stmt)

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
            stmt = """SELECT greed.portfolio_cash_value(%i, %i)""" % (pid, time.time())
            cur.execute(stmt)
            cash = float(cur.fetchone()[0])

            cur.execute(stmt)

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


def delete_comp_portfolio(cpid):
    try:
        con = connect()
        cur = con.cursor()

        stmt = """DELETE FROM greed.subportfolio
                WHERE cpid = %i;""" % (cpid)
        cur.execute(stmt)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


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
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT * FROM super_portfolio
                WHERE id  = %i;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            for folio in folios:
                jsonlist.append({'id':int(folio[0]), 'account_id':int(folio[1]), 'name':str(folio[2]), 'initial_cash':float(folio[3])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

    return json.dumps(jsonlist)


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
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id, competition_id FROM sub_portfolio
            WHERE
                super_portfolio_id  = %i
            AND
                competition_id IS NOT NULL;
            """ % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            for folio in folios:
                jsonlist.append({'id':int(folio[0]), 'competition_id':int(folio[1])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


def find_std_sub_portfolios(uid):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id FROM sub_portfolio
                WHERE super_portfolio_id  = %i AND competition_id IS NULL;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            for folio in folios:
                jsonlist.append({'id':folio[0]})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


def find_sup_vals(uid):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id, name FROM greed.super_portfolio
                WHERE account_id = %i;""" % (uid)
        cur.execute(stmt)
        folios = cur.fetchall()

        stmt = """SELECT id FROM greed.sub_portfolio
                WHERE super_portfolio_id = %i
                AND competition_id IS NULL;"""
        cashstmt = "SELECT greed.portfolio_total_current_value(%i);"

        pval = 0.0
        if(folios is not None):
            for folio in folios:
                cur.execute(stmt % (folio[0]))
                pid = int(cur.fetchone()[0])

                cur.execute(cashstmt % (pid))
                pval = pval + float(cur.fetchone()[0])

                jsonlist.append({'id':folio[0], 'name':folio[1], 'total_current_value':pval})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


def find_all(spid):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT * FROM sub_portfolio
                WHERE super_portfolio_id  = %i;""" % (spid)
        cur.execute(stmt)
        folios = cur.fetchall()

        if(folios is not None):
            for folio in folios:
                jsonlist.append({'id':folio[0], 'super_portfolio_id':folio[1], 'competition_id':folio[2]})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


if __name__ == "__main__":
    sys.exit(main())