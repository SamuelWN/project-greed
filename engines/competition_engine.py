#!/usr/bin/python

import sys
import MySQLdb as mdb
import time
import json
import portfolio_engine


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    #print sys.argv[1:]

    if((sys.argv[1:]) and (sys.argv[1:][0]
    in ['-a', '-d', '-i', '-A', '-m', '-t'])):
        opt = sys.argv[1:][0]
    else:
        opt = '-h'

    if opt == '-a':
        print create_new(int(sys.argv[1:][1]),
                str(sys.argv[1:][2]),
                float(sys.argv[1:][3]),
                float(sys.argv[1:][4]),
                float(sys.argv[1:][5]))
    elif opt == '-d':
        delete_comp(int(sys.argv[1:][1]), int(sys.argv[1:][2]))
    elif opt == '-i':
        print comp_info(int(sys.argv[1:][1]))
    elif opt == '-A':
        print all()
    elif opt == '-m':
        print comp_members(int(sys.argv[1:][1]))
    elif opt == '-t':
        print top_5(int(sys.argv[1:][1]))
    elif opt == '-h':
        print("""-a UID NAME START END FEE    Add new competition
                            (Returns 'Competition_ID,Comp_Portfolio_ID')\n""")
        print("""-d UID COMPID                Delete competition COMPID\n""")
        print("""-i COMPID                    Return all information for competition COMPID\n""")
        print("""-A                           Return all information for all competitions
                            (Past, Present, and Future)\n""")
        print("""-m COMPID                    List all members of competition COMPID\n""")
        print("""-t COMPID                    Determine the top 5 players in competition COMPID""")


def all():
    #print "all()"
    jsonlist = []
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("SELECT * FROM greed.competition;")

        comps = cur.fetchall()

        for acomp in comps:
            jsonlist.append({'id':int(acomp[0]), 'owner_account_id':int(acomp[1]), 'name':str(acomp[2]), 'entryfee':float(acomp[3]), 'unixtime_start':int(acomp[4]), 'unixtime_length':int(acomp[5]), 'cancelled':bool(int(acomp[6]) == 1)})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


def comp_info(compid):
    #print "comp_info(%i)" % compid
    jsondict = {}
    try:
        con = connect()
        cur = con.cursor()

        cur.execute("""SELECT * FROM greed.competition
                    WHERE id = %i;""" % compid)

        info = cur.fetchone()

        jsondict['id'] = int(info[0])
        jsondict['owner_account_id'] = int(info[1])
        jsondict['name'] = str(info[2])
        jsondict['entryfee'] = float(info[3])
        jsondict['unixtime_start'] = int(info[4])
        jsondict['unixtime_length'] = int(info[5])
        jsondict['cancelled'] = bool(int(info[6]) == 1)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsondict)


def create_new(uid, name, start, end, fee):
    compid = -1
    cpid = -1

    try:
        con = connect()
        cur = con.cursor()

        length = end - start

        stmt = """SELECT greed.portfolio_total_current_value(%i);""" % (uid)
        cur.execute(stmt)
        cash = float(cur.fetchone()[0])

        if (cash < fee):
            print "Not enough funds"
        elif (start < time.time()):
            print "'start' time is in the past"
        elif (start > end):
            print "'start' time is after 'end' time"
        else:
            stmt = """INSERT INTO greed.competition
                    (owner_account_id, name, unixtime_start,
                        unixtime_length, entryfee)
                    VALUES('%s','%s', %f, %f, %f);
                        """ % (uid, name, start, length, fee)
            print "stmt = \n\t%s\n" % (stmt)
            cur.execute(stmt)
            cur.execute("SELECT LAST_INSERT_ID();")

            compid = int(cur.fetchone()[0])
            print "compid: " + str(compid)
            con.commit()

            cpid = portfolio_engine.new_comp_portfolio(uid, compid)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps([{'competion_id':int(compid), 'sub_portfolio_id':int(cpid)}])


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


def comp_members(compid):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT id FROM greed.sub_portfolio
                WHERE competition_id = %i;""" % (compid)

        cur.execute(stmt)

        members = cur.fetchall()

        stmt = "SELECT greed.portfolio_total_current_value(%i)"

        jsondict = {}

        for mem in members:
            mem = int(mem[0])

            jsondict['sub_portfolio_id'] = mem
            cur.execute(stmt % (mem))
            jsondict['total_current_value'] = float(cur.fetchone()[0])

            jsonlist.append(jsondict)

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return json.dumps(jsonlist)


def top_5(compid):
    jsonlist = []

    try:
        con = connect()
        cur = con.cursor()

        stmt = """call greed.top5('%i');""" % (compid)
        cur.execute(stmt)
        top = cur.fetchall()

        for a_top in top:
            jsonlist.append({'competition_name':str(a_top[5]), 'id':int(a_top[0]), 'account_id':int(a_top[3]), 'account_username':str(a_top[6]), 'total_value':float(a_top[7])})

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        return json.dumps(jsonlist)


if __name__ == "__main__":
    sys.exit(main())