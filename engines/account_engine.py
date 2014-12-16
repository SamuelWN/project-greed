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
    if((sys.argv[1:]) and (sys.argv[1:][0] in ['-a', '-f', '-t', '-A', '-iU', '-iI'])):
        opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-a':
        print add_user(str(sys.argv[1:][1]))
    elif opt == '-f':
        print find_user(str(sys.argv[1:][1]))
    elif opt == '-iU':
        print info_uname(str(sys.argv[1:][1]))
    elif opt == '-iI':
        print info_id(int(sys.argv[1:][1]))
    elif opt == '-t':
        print top_5()
    elif opt == '-A':
        print all()
    elif opt == '-h':
        print("-a UNAME               Add user USERNAME to database")
        print("-f UNAME               Find user USERNAME in the databse")
        print("-t                     Show the top 5 user (by net worth)")
        print("-iU UNAME              Get id for user of username UNAME")
        print("-iI UID                Get username for user of id UID")
        print("-A                     Show all user within the database")


def add_user(uname):
    uid = -1
    spid = -1

    try:
        con = connect()
        cur = con.cursor()

        unallowed = ["", "None", "none", "-1", None]

        if uname not in unallowed:

            cur.execute("INSERT INTO account (username) VALUES ('" + uname + "');")

            cur.execute("SELECT LAST_INSERT_ID();")

            uid = int(cur.fetchone()[0])

            statement = """INSERT INTO super_portfolio
                        (account_id, name, initial_cash)
                        VALUES(%i, 'DefaultPortfolio', 100000);""" % (uid)
            cur.execute(statement)

            cur.execute("SELECT LAST_INSERT_ID();")

            spid = int(cur.fetchone()[0])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'account_id':uid, 'super_portfolio_id':spid})


def find_user(uname):
    uid = -1

    try:
        con = connect()
        cur = con.cursor()

        statement = """SELECT id, username FROM greed.account
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


def info_id(uid):
    uname = ""

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT username FROM greed.account
                WHERE id  = %i;""" % (uid)
        cur.execute(stmt)
        uname = cur.fetchone()

        if(uname is not None):
            uname = str(uname[0])

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

    return json.dumps({'id':uid, 'username':uname})


def info_uname(uname):
    uid = -1
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id FROM account
                WHERE username = '%s';""" % (uname)

        cur.execute(stmt)
        uid = cur.fetchone()

        if(uid is not None):
            ret = int(uid[0])
        else:
            ret = -1

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps({'id':ret, 'username':uname})


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
