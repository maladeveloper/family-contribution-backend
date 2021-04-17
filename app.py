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
from income_submission_functions import get_income_summary, reverse_income_summary, get_inc_per_user, format_users_tax
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
Initialises the app by passing in logged on user information and setting the dates.
Then returns the user information.
'''
@app.route('/init', methods= ["GET"])
@cross_origin()
def init():

    #Get list of previous dates, refresh them and then add them back to database
    all_dates_dict = db.collection(u'HistoryData').document("PreviousDates").get().to_dict()
    
    db.collection(u'HistoryData').document("PreviousDates").set(get_refreshed_dates(all_dates_dict))

    
    return get_user_info(request.args.get("userId")) #Return user information.
    

@app.route('/getUserInfo', methods=["GET"])
@cross_origin()
def get_user_info(user_id = None):

    user_id = request.args.get("userId") if not user_id else user_id #Get the user id from url if it hasnt been passed in by function.

    data = db.collection("PersonalInformation").document(user_id).get().to_dict()

    return jsonify(data)


'''
Gets the previouse dates from the database in format
Input: NULL
Output:[dateStr1, dateStr2, ...]
'''
@app.route('/previousDates', methods=["GET"])
@cross_origin()
def get_historic_date_data():

    #Since the dates are stored as {dateStr:True,...} in db get only the keys and change to a list.
    all_dates = list(db.collection(u'HistoryData').document("PreviousDates").get().to_dict().keys())

    return jsonify(all_dates)


'''
Find the date data based primarily on the date and the then on the user id.
Input: specified date, user id 
Output: User Income submissions on that date.
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

'''
Updates the income submission for a specific date and user.
Input: date, user id
Output: Bool True
'''
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
    
    except: #Otherwise set the income since it is the first submission for this date.
        
        db.collection(u'DateSpecificData').document(chose_date).set({user_id: inc_summary})

    return jsonify(True)

'''
Returns the users who are pending to have paid their income otherwise directs them to
get everyone's taxed amount.

'''
@app.route('/getPendingUsers', methods=["GET"])
@cross_origin()
def get_pending_users():

    date = get_formatted_dt(request.args.get("date"))

    all_users = db.collection('UsefulData').document("AllUsers").get().to_dict()
    
    paid_users_data = db.collection('DateSpecificData').document(date).get().to_dict()
    
    not_paid_users = list(set(all_users.keys()).difference(set(paid_users_data.keys())))

    not_paid_users = [all_users[user_id] for user_id in not_paid_users] #Return the names and not the ids
    
    ##Return tax information if all users have paid.
    if len(not_paid_users) == 0:

        return find_tax_amount(paid_users_data)

    return jsonify(format_users_tax(False, not_paid_users=not_paid_users))

    
'''
Finds the tax amount of ASSUMING all users who have submitted their income.
Input: NULL
Output:TODO
'''
@app.route('/findTaxAmount', methods=["GET"])
@cross_origin()
def find_tax_amount(paid_users_data=None, date=None):
    
    if paid_users_data is None:

        date = get_formatted_dt(request.args.get("date"))
        
        paid_users_data = db.collection('DateSpecificData').document(date).get().to_dict()

    income_dict = get_inc_per_user(paid_users_data)

    tax_dict = apply_tax(income_dict)

    formatted_tax_dict = format_users_tax(True, users_income=income_dict, users_tax=tax_dict)

    return jsonify(formatted_tax_dict)



if __name__ == '__main__':
    app.run(debug=True)