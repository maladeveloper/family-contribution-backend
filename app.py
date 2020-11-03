from flask import Flask,request
from flask_cors import CORS, cross_origin
from flask import jsonify
from find_tax_amount import apply_tax
import firebase_admin
from firebase_admin import credentials
import firebase_admin
from firebase_admin import credentials, firestore



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

    #Return this data as json
    return jsonify(doc.get(field_id))



if __name__ == '__main__':
    app.run(debug=True)