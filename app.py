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

    #Get the document from the database
    all_dates = db.collection(u'HistoryData').document("PreviousDates").get()

    #Change it to a dictionary
    all_dates = all_dates.to_dict()

    #Get only the keys i.e the date
    all_dates = list(all_dates.keys())

    #Return this data as json
    return jsonify(all_dates)



if __name__ == '__main__':
    app.run(debug=True)