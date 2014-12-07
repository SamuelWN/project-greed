import MySQLdb as mdb
import time


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")

if __name__ == "__main__":
    con = connect()
    cur = con.cursor()

    stmt = "SELECT * FROM greed.competition"

    while(True){
        cur.execute(stmt)

    }