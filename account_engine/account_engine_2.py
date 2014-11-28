#!/usr/bin/python

################################################################################
#  Current status:                                                             #
#    I can't seem to find any glaring errors, but results aren't being	       #
#    displayed to the console                                                  #
################################################################################

import MySQLdb as mdb
import sys
import getopt
#import string

num_users = 0


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ha:f:tA")
    except getopt.GetoptError:
        print
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print
        elif opt == '-a':
            add_user(arg)
        elif opt == 'f':
            find_user(arg)
        elif opt == '-t':
            top_5()
        elif opt == '-A':
            all()


def add_user(uname):
    print(("add_user"))

    try:

        con = connect()
        cur = con.cursor()

        global num_users
        uid = num_users
        cur.execute("INSERT INTO account (id, username) VALUES (" + uid + ", '" + uname + "');")
        cur.execute("INSERT INTO super_portfolio (account_id, name, initial_cash) VALUES(" + uid + ", '" + uname + "', " + 100000 + "');")

        num_users = num_users + 1

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        print(uid)

        return uid


def find_user(uname):
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("SELECT id FROM account WHERE username = '" + uname + "';")
        uid = cur.fetchone()

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        print(uid)

        return uid


# Testing:
def all():
    try:
        print(("\nall()\n"))
        con = connect()
        cur = con.cursor()

        ret = cur.execute("""SELECT * FROM account;""")

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        for a in ret:
            print(a)


def top_5():
    try:
        con = connect()
        cur = con.cursor()

        cmd = cur.execute("""SELECT * FROM account;""")
        accounts = cmd.fetchall()

        sums = [][2]
        for acnt in accounts:
            sums[acnt][0] = accounts[2]
            sums[acnt][1] = cur.execute("SUM(SELECT portfolio_main.cash FROM portfolio_main WHERE owner_account_id = '" + "acnt.id');")

            import numpy as np

        sums = np.array(sums)
        sums.sort(axis=1, kind='mergesort')

        ret = [5][2]
        ret[0][0] = reversed(sums)[0][0]
        ret[0][1] = reversed(sums)[0][0]
        ret[1][0] = reversed(sums)[1][0]
        ret[1][1] = reversed(sums)[1][1]
        ret[2][0] = reversed(sums)[2][0]
        ret[2][1] = reversed(sums)[2][1]
        ret[3][0] = reversed(sums)[3][0]
        ret[3][1] = reversed(sums)[3][1]
        ret[4][0] = reversed(sums)[4][0]
        ret[4][1] = reversed(sums)[4][1]

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        for a_ret in ret:
            print(("%s\n" % (a_ret)))

        return ret
