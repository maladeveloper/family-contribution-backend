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


@app.route('/HistoryData/PreviousDates', methods=["GET"])
@cross_origin()
def get_historic_date_data():

    #Get the for the documents
    field_id = request.args["id"]

    #Get the document from the database
    doc = db.collection(u'HistoryData').document("PreviousDates").get()

    #Get all the dates
    all_dates = doc.get(field_id)

    #Transform the date into display date
    transform_date(all_dates)

    #Return this data as json
    return jsonify(all_dates)

#Function to change date to display date 
def transform_date(date_arr):
    
    #For each date 
    for i in range(len(date_arr)):

        #Get the date in the format now
        original_date = date_arr[i]

        #Split the
        og_split_dates =  original_date.split('-')

        #New display date
        disp_date =''

        #For each of the dates
        for n in range(len(og_split_dates)):

            #Get the split date
            og_split_date = og_split_dates[n]

            #Convert it to display format
            n_split_date = datetime.strptime(og_split_date, '%d/%m/%Y').strftime('%d %b  %y')

            #If it is the second date, add a hyphen before
            if n!= 0:
                disp_date = disp_date+'  -  '+ n_split_date
            else:
                #Otherwise no hyphen 
                disp_date = disp_date + n_split_date
        
        #Replace the former date with the new
        date_arr[i] = {disp_date:original_date}



if __name__ == '__main__':
    app.run(debug=True)