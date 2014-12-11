#!/usr/bin/python
import sys
import MySQLdb as mdb


def connect():
    return mdb.connect(host="localhost", user="root", passwd="toor", db="greed")


def main():
    pid = -1
    results = ''

    if(sys.argv[1:]):
        pid = int(sys.argv[1:][0])
    else:
        return -1


    try:
        con = connect()
        cur = con.cursor()

        stmt = """SELECT
	sub_portfolio_delta.id AS id,
    sub_portfolio_delta.unixtime AS unixtime,
    portfolio_cash_value(sub_portfolio_delta.id, sub_portfolio_delta.unixtime) AS cash_value,
    IFNULL(portfolio_competition_reserved_value(sub_portfolio_delta.id, sub_portfolio_delta.unixtime, false), 0) AS comp_value,
    GROUP_CONCAT(
		DISTINCT CONCAT(
			sub_portfolio_stocks.stock_symbol,
			"-",
			NULLIF(
				portfolio_stock_count(sub_portfolio_delta.id, sub_portfolio_delta.unixtime, sub_portfolio_stocks.stock_symbol),
                0
			)
		)
        ORDER BY sub_portfolio_stocks.stock_symbol
		SEPARATOR '/'
	) AS stock_count
FROM sub_portfolio_delta
RIGHT JOIN
	sub_portfolio_stocks
		ON sub_portfolio_delta.id = sub_portfolio_stocks.id
WHERE sub_portfolio_delta.id = %i
GROUP BY sub_portfolio_delta.id, sub_portfolio_delta.unixtime
""" % (pid)



        cur.execute(stmt)
        results = cur.fetchall()

        #ret = ''
        #for val in results:
            #ret = ret + val ','
            #

    except mdb.Error as e:
        print(("Error %d: %s" % (e.args[0], e.args[1])))
        sys.exit(1)

    finally:
        if con:
            con.commit()
            con.close()

        return results







if __name__ == "__main__":
    print main()
    sys.exit(1)