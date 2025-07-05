import sqlite3
from flask import Flask, request, jsonify

con = sqlite3.connect("journal_entries.db")

cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS JOURNAL_ENTRIES(
            TimeInMilli INTEGER PRIMARY KEY,
            Date TEXT,
            Entry TEXT
            );""")

#function for storing data
def SaveToDB(data):
    #data will be json, make into a list of tuples, then save data
    con = sqlite3.connect("journal_entries.db")
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
    con = sqlite3.connect("journal_entries.db")
    cur = con.cursor()
    result = cur.execute("""SELECT * 
                          FROM JOURNAL_ENTRIES;""")
    AllData = result.fetchall() # ✅ get all the rows while the DB is still open
    con.close()
    return AllData

#api stuff
app = Flask(__name__)

#will take data sent from user
@app.route("/api/save-entry", methods=["POST"]) #POST will be used here cz this will *send* data to the db
def TakeEntry():
    data = request.get_json()

    SaveToDB(data)

    msg = {"success":True, "message": "data successfully stored"}

    return jsonify(msg)

#will send data to the user 
@app.route("/api/get-entries", methods=["GET"]) #GET will be used here cz this will *retrieve* data from the db
def SendEntries():
    DictEntries = RetrieveData()

    EntriesToSend = []

    for entry in DictEntries:
        EntriesToSend.append({"TimeInMilli": entry[0],"Date": entry[1],"Entry": entry[2]})

    return jsonify(EntriesToSend)

con.close()

if __name__ == "__main__":
    app.run(debug=True)