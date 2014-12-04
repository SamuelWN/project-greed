#!/usr/bin/python

import MySQLdb as mdb
import sys
import numpy as np

import pdb


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")

def tuple_to_str(ret):
        return (str(ret).split('L')[0])[1:]


def main():
    if((sys.argv[1:]) and (sys.argv[1:][0] in ['-a', '-f', '-t', '-A'])):
            opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-a':
        add_user(sys.argv[1:][1])
    elif opt == '-f':
        find_user(sys.argv[1:][1])
    elif opt == '-t':
        top_5()
    elif opt == '-A':
        all()
    elif opt == '-h':
        print("-a USERNAME           Add user USERNAME to database")
        print("-f USERNAME           Find user USERNAME in the databse")
        print("-t                    Show the top 5 user (determined by net worth)")
        print("-A                    Show all user within the database (debugging)")


def add_user(uname):
    print(("add_user"))

    try:
        con = connect()
        cur = con.cursor()

        cur.execute("INSERT INTO account (username) VALUES ('" + uname + "');")

        statement = """SELECT id FROM greed.account
                    WHERE username = '%s';""" % (uname)
        cur.execute(statement)

        uid = int(tuple_to_str(cur.fetchone()))

        statement = """INSERT INTO super_portfolio
                    (account_id, name, initial_cash)
                    VALUES(%i, 'DefaultPortfolio', 100000);""" % (uid)
        cur.execute(statement)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        print()


def find_user(uname):
    userid = -1

    try:
        con = connect()
        cur = con.cursor()

        statement = """SELECT id FROM greed.account
                    WHERE username = '%s';""" % (uname)
        cur.execute(statement)

        uid = cur.fetchone()
        print "uid = cur.fetchone()     =    ", uid
        print "uid = tuple_to_str(uid)    =    ", tuple_to_str(uid)
        uid = str(uid).split('L')[0]

        userid = int((uid)[1:])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        print userid

        return int(tuple_to_str(userid))


# Testing:
def all():
    try:
        print(("\nall()\n"))
        con = connect()
        cur = con.cursor()

        cur.execute("""SELECT * FROM account;""")

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

    for n in range(cur.rowcount):
        row = cur.fetchone()
        print (row)


def top_5():
    ret = [''][0]
    try:
        con = connect()
        con2 = connect()
        usr = con.cursor()
        val = con2.cursor()

        stmt = "SELECT total_value FROM greed.portfolio_value_total WHERE id = "

        val.execute("SELECT COUNT(*) FROM greed.account")
        numusers = int(tuple_to_str(val.fetchone()))

        usr.execute("SELECT id FROM account;")

        sums = [[0, 0] for x in range(numusers)]

        ret = [["", 0.00] for x in range(5 if (numusers >= 5) else numusers)]

        i = 0
        while i < numusers:
            sums[i][0] = int(tuple_to_str(usr.fetchone()))
            val.execute(stmt + str(sums[i][0]) + ";")
            sums[i][1] = float(str(val.fetchone()).split("'")[1])

            i = i + 1

        sums = np.matrix(sums)
        sums.sort(axis=1, kind='mergesort')
        ordered_sums = sums[::-1].tolist()

        stmt = "SELECT username FROM greed.account WHERE id = "

        i = 0
        while i < (5 if (numusers >= 5) else numusers):
            usr.execute(stmt + str(int(ordered_sums[i][0])) + ";")
            ret[i][0] = str(usr.fetchone()).split("'")[1]
            ret[i][1] = ordered_sums[i][1]

            i = i + 1

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        i = 0
        while i < (5 if (numusers >= 5) else numusers):
            print "ret[", i, "][0] = ", ret[i][0]
            print "ret[", i, "][1] = ", ret[i][1]
            print
            i = i + 1

        return ret


if __name__ == "__main__":
    sys.exit(main())