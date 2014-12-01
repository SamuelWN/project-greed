#!/usr/bin/python

import MySQLdb as mdb
import sys

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
        print("""-a USERNAME           Add user USERNAME to database""")
        print("""-f USERNAME           Find user USERNAME in the databse""")
        print("""-t                    Show the top 5 user (determined by net worth)""")
        print("""-A                    Show all user within the database (debugging)""")


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
    ret = [[0.00, ""], [0.00, ""], [0.00, ""], [0.00, ""], [0.00, ""]]
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("""SELECT * FROM account;""")

        sums = [[0, ""] for x in range(cur.rowcount)]

        for n in range(cur.rowcount):
            row = cur.fetchone()

            vals = str(row).split("L, '")
            vals[0] = (vals[0])[1:]
            uid = int(vals[0])
            sums[n][1] = str(vals[1]).split("')")[0]

#TESTING:
            print(("ID:"))
            print((sums[n][0]))
            print(("Username:"))
            print((sums[n][1]))

################################################################################
#    NEED TO CHANGE STATEMENT TO USE:                                          #
#        portforlio_value_stock + portfolio_value_cash                         #
################################################################################

            statement = """SELECT * FROM portfolio_value_total
                                    WHERE id = '%i';""" % (uid)
            sums[n][0] = cur.execute(statement)

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


if __name__ == "__main__":
    sys.exit(main())
