import sqlite3

con = sqlite3.connect("E:\journal_entries.db")

cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS JOURNAL_ENTRIES(
            TimeInMilli INTEGER PRIMARY KEY,
            Date TEXT,
            Entry TEXT
            );""")

#function for storing data
def SaveToDB(data):
    #data will be json, make into a list of tuples, then save data
    con = sqlite3.connect("E:\journal_entries.db")
    cur = con.cursor()
    time = data["TimeInMilli"]
    date = data["Date"]
    entry = data["Entry"]
    cur.execute("INSERT INTO JOURNAL_ENTRIES (TimeInMilli, Date, Entry) VALUES(?, ?, ?);", (time, date, entry))
    con.commit()
    con.close()

#function for retrieving data
def RetrieveData():
    #data is returned as lists of tuples from the db
    con = sqlite3.connect("E:\journal_entries.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * 
                        FROM JOURNAL_ENTRIES
                        ORDER BY TimeInMilli DESC;""")
    AllData = result.fetchall() # ✅ get all the rows while the DB is still open
    con.close()
    return AllData