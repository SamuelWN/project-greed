#!/usr/bin/python

import sys
import MySQLdb as mdb
import time
import portfolio_engine


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


#def dbg():
    #print sys.argv[1:]
    #print "num args: ", len(sys.argv[1:])

    #i = 0
    #while i < len(sys.argv[1:]):
        #print 'sys.argv[1:][', str(i), "] = ", sys.argv[1:][int(i)]
        #i = i + 1

    #print "------------------------------\n"


def main():
    #dbg()

    if((sys.argv[1:]) and (sys.argv[1:][0]
    in ['-a', '-d', '-j', '-A', '-m', '-e'])):
        opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-a':
        print create_new(int(sys.argv[1:][1]),
                str(sys.argv[1:][2]), float(sys.argv[1:][3]),
                float(sys.argv[1:][4]), float(sys.argv[1:][5]))
    elif opt == '-d':
        delete_comp(int(sys.argv[1:][1]), int(sys.argv[1:][2]))
    elif opt == '-j':
        join_comp(sys.argv[1:][1], str(sys.argv[1:][2]))
    elif opt == '-A':
        print all()
    elif opt == '-m':
        print comp_members(sys.argv[1:][1])
    elif opt == '-e':
        print comp_end(sys.argv[1:][1])
    elif opt == '-h':
        print("""-a UID NAME START END FEE
            Add new competition\n""")
        print("""-d UID COMPID
            Delete competition COMPID\n""")
        print("""-j COMPID
            Join competition COMPID\n""")
        print("""-m COMPID
            List all members of competition COMPID\n""")
        print("""-e COMPID
            Determine the top 5 players in competition COMPID""")


def all():
    #print "all()"
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("SELECT * FROM greed.competition;")

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        for n in range(cur.rowcount):
            row = cur.fetchone()
            return row


def create_new(uid, name, start, end, fee):
    try:
        con = connect()
        cur = con.cursor()

        length = end - start

        stmt = """SELECT cash FROM stock_current
                WHERE id = %i;""" % (uid)
        cur.execute(stmt)
        cash = float(cur.fetchone()[0])

        if (cash > fee):
            print "Not enough funds"
        elif (start < time.gmtime):
            print "'start' time is in the past"
        elif (start > end):
            print "'start' time is after 'end' time"
        else:
            stmt = """INSERT INTO greed.competition
                    (owner_account_id, name, unixtime_start,
                        unixtime_length, entryfee)
                    VALUES('%s','%s', %f, %f, %f);
                        """ % (uid, name, start, length, fee)

            cur.execute(stmt)

            stmt = """SELECT id FROM greed.competition
                    WHERE owner_account_id = '%s'
                    AND name = '%s'""" % (uid, name)

            cur.execute(stmt)
            compid = cur.fetchone()[0]

            portfolio_engine.new_comp_portfolio(uid, compid)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()
        return compid


def delete_comp(uid, compid):
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT owner_account_id
                FROM greed.competition
                WHERE id = %i;""" % (compid)

        cur.execute(stmt)

        owner = int(cur.fetchone()[0])
        print owner

        stmt = """DELETE FROM greed.competition
                WHERE owner_account_id = %i
                AND id = %i;""" % (uid, compid)

        if(owner == uid):
            print "owner == uid"
            cur.execute(stmt)
        else:
            print "owner != uid"

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()


def join_comp(uid, compid):
    cpid = -1
    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT unixtime_start FROM greed.competition
                WHERE id = """ + compid + ";"

        cur.execute(stmt)

        stime = cur.fetchone()[0]

        if(stime < time.gmtime()):
            stmt = """SELECT entryfee FROM greed.competition
                WHERE id = """ + compid + ";"
            cur.execute(stmt)
            fee = float(cur.fetchone()[0])

            stmt = """SELECT cash FROM portfolio_value_cash
                WHERE id = """ + uid + ";"

            cur.execute(stmt)
            cash = float(cur.fetchone()[0])

            if(fee < cash):
                cpid = portfolio_engine.new_comp_portfolio(uid, compid)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()
        return cpid


def comp_members(compid):
    ret = ""

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id FROM greed.sub_portfolio
                WHERE competition_id = """ + compid + ";"

        cur.execute(stmt)

        members = cur.fetchall()

        for mem in members:
            ret = ret + str(mem[0]) + ","

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return ret[:-1]


def comp_end(compid):
    ret = ""
    try:
        con = connect()
        cur = con.cursor()

        mems = comp_members(compid)

        stmt = """SELECT * FROM greed.portfolio_value_total
                WHERE id IN (""" + mems + """)
                ORDER BY comp_value DESC LIMIT 5;"""

        cur.execute(stmt)

        winners = cur.fetchall()

        for win in winners:
            ret = ret + str(win[0]) + ","

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()
        return ret[:-1]

if __name__ == "__main__":
    sys.exit(main())