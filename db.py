import sqlite3, uuid, hashlib

PATH =r"E:\Journal_Site\journal_entries.db"

def CreateDBs():
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
        CreateDBs()
        Message = {"Message" : "User account created successfully"}
    except sqlite3.IntegrityError:
        Message = {"Message" : "Username already taken"}
    finally:
        con.commit()
        con.close()
    return Message

def LogIn(username:str, psw:str):
    # get user creds
    # check whether user exists
    # proceed if creds are correct
    con = sqlite3.connect(PATH)
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    hashed_password = str(hashlib.sha256(psw.encode("utf-8")).hexdigest())

    result = cur.execute("""SELECT user_id, Username, Password
                         FROM USERS
                         WHERE Username = ?;""", (username,))
    data = result.fetchall()
    cur.close()

    if data and username == data[0][1] and hashed_password == data[0][2]:
        # USER_ID = 
        # i think user id would need to be returned instead global cz heres the thing, this file wont be running. yea. yea.
        message = {"Message":"Log in successful",
                   "User ID": data[0][0]}
        return message

    else:
        message = {"Message":"Username or password incorrect"}
        return message