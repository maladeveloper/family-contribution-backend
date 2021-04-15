from flask import Flask,request
from flask_cors import CORS, cross_origin
from flask import jsonify
from find_tax_amount import apply_tax
import firebase_admin
from firebase_admin import credentials
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from helper_functions import get_refreshed_dates, get_formatted_dt
from income_submission_functions import get_income_summary, reverse_income_summary
from VARIABLES import TOTAL_TAX_PER_WEEK, WEEKS_PER_PAYMENT



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
Initialises the app by passing in logged on user information and setting the dates
'''
@app.route('/init', methods= ["GET"])
@cross_origin()
def init():

    #Get list of previous dates, refresh them and then add them back to database
    all_dates_dict = db.collection(u'HistoryData').document("PreviousDates").get().to_dict()
    
    db.collection(u'HistoryData').document("PreviousDates").set(get_refreshed_dates(all_dates_dict))

    #Now send back the data of the user
    user_id = request.args.get("userId")
    
    return get_user_info(user_id)
    

@app.route('/getUserInfo', methods=["GET"])
@cross_origin()
def get_user_info(user_id = None):

    if not user_id:

        #Get the user id
        user_id = request.args.get("userId")

    data = db.collection("PersonalInformation").document(user_id).get().to_dict()

    return jsonify(data)





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

    date, user_id  = get_formatted_dt(request.args.get("date")), request.args.get("userId")

    date_info = db.collection('DateSpecificData').document(date).get().to_dict()

    try:

        return jsonify(reverse_income_summary(date_info[user_id])) #Only return the user in information in un-summarised form
    
    except: #User has not submitted any income for this date yet.

        return jsonify([])


    


@app.route('/updateIncomeSubmission', methods=["POST"])
@cross_origin()
def update_income_submission():

    ##Get the information from the request body
    user_id, income_arr, chose_date = [request.json[inf_key] for inf_key in ["userId", "incomeArray", "chosenDate"]]

    inc_summary = get_income_summary(income_arr)

    chose_date = get_formatted_dt(chose_date)

    #First update the income per user
    db.collection(u'HistoryData').document(u'UserPayment').collection(user_id).document(chose_date).set(inc_summary)

    #Update the income per date if date is there
    try:
        
        db.collection(u'DateSpecificData').document(chose_date).update({user_id: inc_summary})
    
    except:
        
        db.collection(u'DateSpecificData').document(chose_date).set({user_id: inc_summary})

    return jsonify(True)

'''
Returns the users who are pending to have paid their income.
'''
@app.route('/getPendingUsers', methods=["GET"])
@cross_origin()
def get_pending_users():

    date = get_formatted_dt(request.args.get("date"))

    all_users = db.collection('UsefulData').document("AllUsers").get().to_dict()
    
    paid_users = db.collection('DateSpecificData').document(date).get().to_dict()
    
    not_paid_users = list(set(all_users.keys()).difference(set(paid_users.keys())))

    not_paid_users = [all_users[user_id] for user_id in not_paid_users] #Return the names and not the ids
    
    ##Return all the paid user information if everyone has paid
    if len(not_paid_users) == 0:

        ##TODO: Get the total tax per person.
        #income_per_person = {name:total_income for key, info"}

        return {"allPaid":True, "Info": {"idToName":all_users, "incomeInfo":paid_users}}

    return jsonify({"allPaid":False, "notPaidUsers": not_paid_users})

    



if __name__ == '__main__':
    app.run(debug=True)