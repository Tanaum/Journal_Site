from flask import Flask, request, jsonify
from flask_cors import CORS
from db import SaveToDB, RetrieveData, SignUp, LogIn

app = Flask(__name__)

CORS(app, supports_credentials=True)  # This allows all domains to access all routes (for dev it's fine)

# SignUp
@app.route('/sign-up', methods=["POST"])
def Sign_Up():
    data = request.get_json()   # will contain username and psw
    
    username, password = data["username"], data["password"]

    ReturnValue = SignUp(username, password)
    if ReturnValue["Account Created"]:
        return jsonify(ReturnValue), 200
    else:
        return jsonify(ReturnValue), 400

# LogIn
@app.route('/log-in', methods=['POST'])
def Log_In():
    data = request.get_json()   # will contain username and psw
    
    username, password = data["username"], data["password"]

    ReturnValue = LogIn(username, password)
    if ReturnValue["Logged In"]:
        return jsonify(ReturnValue), 200
    else:
        return jsonify(ReturnValue), 400

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

#retrieve entry to be edited
@app.route("/api/edit-entry/<TimeInMilli>", methods=["GET"])
def EditEntry(TimeInMilli):
    OriginalEntry = RetrieveData(TimeInMilli)

    return jsonify(OriginalEntry)

if __name__ == "__main__":
    app.run(debug=True)