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

@app.route('/transformDate', methods=["POST"])
@cross_origin()
def transform_date_route():
    
    #Get the date string from the request
    date = request.json["info"]

    #Transform the date into display date
    transformed_date_dict = transform_date([date])
    
    #Return the data with now the tax there 
    return jsonify(transformed_date_dict)

'''
Gets an object with 
{
    displayStr1:dateStr1, 
    displayStr2:dateStr2,
    ...
}
and pushes it to database as
{
    dateStr1: true,
    dateStr2: true,
}
'''
@app.route('/refreshDates', methods=["POST"])
@cross_origin()
def refresh_dates():

    #Get the previous dates from the request
    data = request.json["info"]

    #Make the dictionary with the data that is needed to push
    dates_dict = dict()

    #Get the values from this dictionary
    for k,v in data.items():

        #Set the value as true in the new dict
        dates_dict[v] = True


    #Push the dates_dict data
    db.collection(u'HistoryData').document("PreviousDates").set(dates_dict)

    return jsonify(True)


'''
Gets the previouse dates from the database in format
{
    dateStr1: true,
    dateStr2: true,
}
and reformats it to the display version
{
    displayStr1:dateStr1, 
    displayStr2:dateStr2,
    ...
}
and sends it to caller.
'''
@app.route('/previousDates', methods=["GET"])
@cross_origin()
def get_historic_date_data():

    #Get the document from the database
    all_dates = db.collection(u'HistoryData').document("PreviousDates").get()

    #Change it to a dictionary
    all_dates = all_dates.to_dict()

    #Transform the date into display date
    all_dates_dict = transform_date(list(all_dates.keys()))

    #Return this data as json
    return jsonify(all_dates_dict)


#Function to change date to display date 
def transform_date(date_arr):
    
    #Establish a dictionary to hold each date to its display
    date_dict = dict()

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
        
        #Add it to the dictionary
        date_dict[disp_date] = original_date

    return date_dict



if __name__ == '__main__':
    app.run(debug=True)