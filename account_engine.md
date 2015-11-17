#!/usr/bin/python
# -**- coding: utf-8 -**-

import MySQLdb as mdb
import numpy as np
import sys

num\_users = 0

def add\_user(uname):
> try:
> > con = mdb.connect(host="localhost", user="root", passwd="toor", db="account")


> cur = con.cursor()
> uid = num\_users
> cur.execute("INSERT INTO account(uid, username) VALUE(id, uname)")
> cur.execute("INSERT INTO portfolio\_main(name, cash, name, owner\_account\_id) VALUE (uname, 100000, 'Default Portfolio', num\_users)")
> global num\_users = num\_users + 1     #dunno what the syntax error is

> except mdb.Error, e:
> > print "Error %d: %s" % (e.args[0](0.md), e. args[1](1.md))
> > sys.exit(1)


> finally:
> > if con:
> > > con.close()


> return uid

def find\_user(uname):
> try:
> > con = mdb.connect(host="localhost", user="root", passwd="toor", db="account");


> cur = con.cursor()
> cur.execute("SELECT id FROM account where username = uname")
> uid = cur.fetchone()

> except mdb.Error, e:
> > print "Error %d: %s" % (e. args[0](0.md), e.args[1](1.md))
> > sys.exit(1)


> finally:
> > if con:
> > > con.close()


> return uid

def top\_5():
> try:
> > adb = mdb.connect(host="localhost", user="root", passwd="toor", db="account");
> > pdb= mdb.connect(host="localhost", user="root", passwd="toor", db="portfolio\_main");


> cur = adb.cursor()
> cmd = cur.execute("""SELECT **FROM account""")
> accounts = cmd.fetchall()**

> cur = pdb.cursor()
> sums = [.md](.md)[2](2.md)
> for acnt in accounts:
> > sums[acnt](acnt.md)[0](0.md) = accounts[2](2.md)
> > sums[acnt](acnt.md)[1](1.md) = cur.execute("SUM(SELECT portfolio\_main.cash FROM portfolio\_main WHERE owner\_account\_id = acnt.id)")


> sums = np.array(sums)
> sums.sort(axis=1, kind='mergesort')

> ret = [5](5.md)[2](2.md)
> ret[0](0.md)[0](0.md) = reversed(sums)[0](0.md)[0](0.md)
> ret[0](0.md)[1](1.md) = reversed(sums)[0](0.md)[0](0.md)
> ret[1](1.md)[0](0.md) = reversed(sums)[1](1.md)[0](0.md)
> ret[1](1.md)[1](1.md) = reversed(sums)[1](1.md)[1](1.md)
> ret[2](2.md)[0](0.md) = reversed(sums)[2](2.md)[0](0.md)
> ret[2](2.md)[1](1.md) = reversed(sums)[2](2.md)[1](1.md)
> ret[3](3.md)[0](0.md) = reversed(sums)[3](3.md)[0](0.md)
> ret[3](3.md)[1](1.md) = reversed(sums)[3](3.md)[1](1.md)
> ret[4](4.md)[0](0.md) = reversed(sums)[4](4.md)[0](0.md)
> ret[4](4.md)[1](1.md) = reversed(sums)[4](4.md)[1](1.md)

> except mdb.Error, e:
> > print "Error %d: %s" % (e. args[0](0.md), e.args[1](1.md))
> > sys.exit(1)


> finally:
> > if con:
> > > con.close()