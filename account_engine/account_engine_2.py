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


# DEBUGGING NOTICE
# https://docs.python.org/2/library/pdb.html
# import "pdb" (python debugger), and place "pdb.set_trace()" in the code where you want a breakpoint.
# when at a breakpoint when running the code, type "c" to continue, "locals()" to see all local variables, and "globals()" to see all global variables
# http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python/
import pdb


num_users = 0


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    try:

# http://stackoverflow.com/questions/1540365/why-isnt-getopt-working-if-sys-argv-is-passed-fully
# I changed sys.argv to sys.argv[1:], so that getopt would work as intended

        opts, args = getopt.getopt(sys.argv[1:], "ha:f:tA")
    except getopt.GetoptError:
        print()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(arg)
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

    uid = 0

    try:

        con = connect()
        cur = con.cursor()

        cur.execute("INSERT INTO account (username) VALUES (uname);")
        uid = find_user(uname)
        cur.execute("INSERT INTO super_portfolio (account_id, name, initial_cash) VALUES(" + uid + "'" + uname + "', " + 100000 + "');")

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
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("SELECT id FROM greed.account WHERE username = '" + uname + "';")
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
    ret = [[0.00, ""], [0.00, ""], [0.00, ""], [0.00, ""], [0.00, ""]]
    try:
        con = connect()
        cur = con.cursor()

#        cmd = cur.execute("""SELECT * FROM account;""")
#        accounts = cmd.fetchall()
#        for acnt in accounts:

        cur.execute("""SELECT * FROM account;""")

        sums = [[0, ""] for x in range(cur.rowcount)]
#        print(("cur.rowcount: "))
#        print ((cur.rowcount))

        for n in range(cur.rowcount):
            row = cur.fetchone()
#            print(('row[', n, '] = ', row))

            vals = str(row).split("L, '")
            vals[0] = (vals[0])[1:]
            sums[n][0] = int(vals[0])
            sums[n][1] = str(vals[1]).split("')")[0]

#TESTING:
            print(("ID:"))
            print((sums[n][0]))
            print(("Username:"))
            print((sums[n][1]))

            sums[n][0] = cur.execute("SUM(SELECT * FROM portfolio_cash WHERE owner_account_id = " + sums[n][0] + ");")

#TESTING:
            print(("Username:"))
            print((sums[n][1]))
            print(("Cash:"))
            print((sums[n][0]))


        import numpy as np

        sums = np.array(sums)
        sums.sort(axis=1, kind='mergesort')
        ordered_sums = reversed(sums)

        ret[0][0] = ordered_sums[0][0]
        ret[0][1] = ordered_sums[0][0]
        ret[1][0] = ordered_sums[1][0]
        ret[1][1] = ordered_sums[1][1]
        ret[2][0] = ordered_sums[2][0]
        ret[2][1] = ordered_sums[2][1]
        ret[3][0] = ordered_sums[3][0]
        ret[3][1] = ordered_sums[3][1]
        ret[4][0] = ordered_sums[4][0]
        ret[4][1] = ordered_sums[4][1]

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

# Testing:
        '''for a_ret in ret:
            for val in a_ret:
                print (val)
            print(("\n"))

#            print(a_ret[0])
 #           print(("    $")
  #          print(a_ret[1])
   #         print(("\n"))
        #print('\n'.join([''.join(['{:4}'.format(item) for item in row])
        #  for row in ret]))
'''
        return ret











# python is interpreted - it needs to actually be told to run your "main" method

if __name__ == "__main__":
    sys.exit(main())
