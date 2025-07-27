from flask import Flask, request, jsonify
from flask_cors import CORS
from db import SaveToDB, RetrieveData

app = Flask(__name__)

CORS(app, supports_credentials=True)  # This allows all domains to access all routes (for dev it's fine)

#will take data sent from user
@app.route("/api/save-entry", methods=["POST"]) #POST will be used here cz this will *send* data to the db
def TakeEntry():
    data = request.get_json()

    print(data)

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

if __name__ == "__main__":
    app.run(debug=True)