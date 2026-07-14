import sqlite3

PATH = "E:\Journal_Site\journal_entries.db"

con = sqlite3.connect(PATH)

cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON;")    # it prevents a fk in entries that doesnt exist as a pk in users 

cur.execute('''CREATE TABLE "USERS" (
	"user_id"	TEXT NOT NULL UNIQUE,
	"Username"	TEXT NOT NULL UNIQUE,
	"Password"	INTEGER NOT NULL,
	PRIMARY KEY("user_id")
);''')

cur.execute('''CREATE TABLE "JOURNAL_ENTRIES" (
	"TimeInMilli"	INTEGER,
	"user_id_FK"	INTEGER,
	"Date"	TEXT,
	"Entry"	TEXT,
	PRIMARY KEY("TimeInMilli"),
	FOREIGN KEY("user_id_FK") REFERENCES "USERS"("user_id")
);''')

con.commit()
con.close()

#function for storing data
def SaveToDB(data):
    #data will be json, make into a list of tuples, then save data
    con = sqlite3.connect(PATH)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    time = data["TimeInMilli"]
    date = data["Date"]
    entry = data["Entry"]
    cur.execute("INSERT INTO JOURNAL_ENTRIES (TimeInMilli, Date, Entry) VALUES(?, ?, ?);", (time, date, entry))
    con.commit()
    con.close()

#function for retrieving data
def RetrieveData(PrimKey="*"):
    con = sqlite3.connect(PATH)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")
    if PrimKey == '*':
        #data is returned as lists of tuples from the db
        result = cur.execute("""SELECT * 
                            FROM JOURNAL_ENTRIES
                            ORDER BY TimeInMilli DESC;""")
        AllData = result.fetchall() # ✅ get all the rows while the DB is still open
    else:
        result = cur.execute("""SELECT * 
                            FROM JOURNAL_ENTRIES
                            WHERE TimeInMilli = ?;""", (int(PrimKey),))
        AllData = result.fetchall() # ✅ get all the rows while the DB is still open
    
    con.close()
    return AllData