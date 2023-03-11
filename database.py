import sqlite3

con= sqlite3.connect("CourierB.db")
print("Database opened Succesfully")

con.execute("""CREATE TABLE "mytable" (
	"id"	INTEGER NOT NULL,
	"pname"	TEXT NOT NULL,
	"pemail"	TEXT NOT NULL,
	"pphone"	TEXT NOT NULL,
	"paddress"	TEXT NOT NULL,
	"dname"	TEXT NOT NULL,
	"demail"	TEXT NOT NULL,
	"dphone"	INTEGER NOT NULL,
	"daddress"	TEXT NOT NULL,
	"dphoto"	BLOB NOT NULL,
	"weight"	INTEGER NOT NULL,
	"distance"	INTEGER NOT NULL,
	"cost"	INTEGER NOT NULL,
	"remarks"	TEXT,
	"ddate"	INTEGER,
	
)""")


print("Table created succesfully")
con.close()