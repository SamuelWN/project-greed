#!/usr/bin/python

import MySQLdb as mdb
import sys
import json
#import pdb


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
        print add_user(sys.argv[1:][1])
    elif opt == '-f':
        print find_user(sys.argv[1:][1])
    elif opt == '-t':
        print top_5()
    elif opt == '-A':
        print all()
    elif opt == '-h':
        print("-a USERNAME           Add user USERNAME to database")
        print("-f USERNAME           Find user USERNAME in the databse")
        print("-t                    Show the top 5 user (by net worth)")
        print("-A                    Show all user within the database")


def add_user(uname):
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("INSERT INTO account (username) VALUES ('" + uname + "');")

        statement = """SELECT id FROM greed.account
                    WHERE username = '%s';""" % (uname)
        cur.execute(statement)

        uid = int(cur.fetchone()[0])

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


def find_user(uname):
    uid = -1

    try:
        con = connect()
        cur = con.cursor()

        statement = """SELECT id FROM greed.account
                    WHERE username = '%s';""" % (uname)
        cur.execute(statement)

        uid = cur.fetchone()[0]

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'id':uid})


def all():
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        cur.execute("SELECT * FROM account;")
        acnts = cur.fetchall()

        print "acnts: \n\t%s\n" % (str(acnts))

        for usr in acnts:
            jsonlist.append({'id':usr[0],'username':usr[1]})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()
        return json.dumps(jsonlist)


def top_5():
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        cur.execute("call greed.top5(Null);")
        top = cur.fetchall()

        for a_top in top:
            jsonlist.append({'id':int(a_top[0]), 'super_portfolio_name':str(a_top[4]),'account_id':int(a_top[3]), 'account_username':str(a_top[6]), 'total_value':float(a_top[7])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        return json.dumps(jsonlist)


if __name__ == "__main__":
    sys.exit(main())