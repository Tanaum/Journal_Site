import sqlite3, uuid, hashlib

PATH =r"E:\Journal_Site\journal_entries.db"

con = sqlite3.connect(PATH)

cur = con.cursor()

cur.execute("PRAGMA foreign_keys = ON;")    # it prevents a fk in entries that doesnt exist as a pk in users 

cur.execute('''CREATE TABLE IF NOT EXISTS "USERS" (
	"user_id"	TEXT NOT NULL UNIQUE,
	"Username"	TEXT NOT NULL UNIQUE,
	"Password"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
);''')

cur.execute('''CREATE TABLE IF NOT EXISTS "JOURNAL_ENTRIES" (
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

def SignUp(username:str, psw:str):
    # get user and psw
    # ensure data doesnt already exist
    # if exists, tell user to enter unique details
    # generate uuid
    con = sqlite3.connect(PATH)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    id = str(uuid.uuid4())
    hashed_password = str(hashlib.sha256(psw.encode("utf-8")).hexdigest())

    try:
        cur.execute("INSERT INTO USERS (user_id, Username, Password) VALUES(?,?,?);", (id, username, hashed_password))
    except sqlite3.IntegrityError:
        print('USERNAME ALREADY TAKEN')
    finally:
        con.commit()
        con.close()

def LogIn(username:str, psw:str):
    # get user creds
    # check whether user exists
    # proceed if creds are correct
    con = sqlite3.connect(PATH)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    hashed_password = str(hashlib.sha256(psw.encode("utf-8")).hexdigest())

    result = cur.execute("""SELECT Username, Password
                         FROM USERS
                         WHERE Username = ?;""", (username,))
    data = result.fetchall()
    
    if data == []:
        print('User does not exist')

    elif username == data[0][0] and hashed_password == data[0][1]:
        print('Logged in')

    else:
        print('Incorrect username or password')

    cur.close()