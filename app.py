from flask import Flask,request
from flask_cors import CORS, cross_origin
from flask import jsonify
from find_tax_amount import apply_tax
import firebase_admin
from firebase_admin import credentials
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime


#VARIABLES
TOTAL_TAX_PER_WEEK = 700

#Open up the firebase 
cred = credentials.Certificate("Secrets/secret_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
@cross_origin()
def hello():
    return "Hello World!"

'''
Finds the tax amount given the dictionary of each individual with their income amount
'''
@app.route('/findTaxAmount', methods=["POST"])
@cross_origin()
def find_tax_amount():
    
    #Get the tax information from the request
    data = request.json["info"]

    #Find the taxable income from the script
    apply_tax(data,TOTAL_TAX_PER_WEEK)
    
    #Return the data with now the tax there 
    return jsonify(data)


'''
Gets an object with 
[
    dateStr1,dateStr2
    ...
]
and pushes it to database as

'''
@app.route('/refreshDates', methods=["POST"])
@cross_origin()
def refresh_dates():

    #Get the previous dates from the request
    data = request.json["info"]

    #Create a new dates dict 
    dates_dict = dict()

    #Form a dictionary from this array
    for date in data:
        dates_dict[date] = True

    #Push the dates_dict data
    db.collection(u'HistoryData').document("PreviousDates").set(dates_dict)

    return jsonify(True)


'''
Gets the previouse dates from the database in format
{
    dateStr1: true,
    dateStr2: true,
}

'''
@app.route('/previousDates', methods=["GET"])
@cross_origin()
def get_historic_date_data():

    print("HERE")

    #Get the document from the database
    all_dates = db.collection(u'HistoryData').document("PreviousDates").get()

    print(all_dates)

    #Change it to a dictionary
    all_dates = all_dates.to_dict()

    #Get only the keys i.e the date
    all_dates = list(all_dates.keys())

    #Return this data as json
    return jsonify(all_dates)

'''
Find the date data based primarily on the date and the then on the user id.
Input as - 
specified date,user id, 

Output- 
Date, user information.

'''
@app.route('/getDateUserSpecificData', methods=["GET"])
@cross_origin()
def get_date_user_specific_data():

    #Get the date
    date = request.args.get("date")

    #Replace the / with a blank in string
    date = date.replace('/', '')

    #Get the user id
    user_id = request.args.get("userId")

    #Make the call to db to get the date document
    date_info = db.collection('DateSpecificData').document(date).get()

    #Check if the date info exists
    if date_info.exists:

        #If so then change the data into a dictionary
        date_info = date_info.to_dict()

    #Otherwise return false
    else:
        return jsonify(False)

    #Only return the user in information
    return jsonify(date_info[user_id])





if __name__ == '__main__':
    app.run(debug=True)