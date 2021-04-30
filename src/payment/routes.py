from flask import Blueprint, current_app, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from pprint import pprint

from .functions import get_income_summary, reverse_income_summary, get_inc_per_user, format_users_tax, apply_tax, get_inc_from_average, min_tax_dicts
from date_functions import get_average_dates, convert_to_db_date
from VARIABLES import BACKEND_URL as BASE_URL



payment_bp = Blueprint("payment_bp", __name__)

db=current_app.db

@payment_bp.route('/')
@cross_origin()
def hello():
    return "Hello World!"

'''
Find the income data based primarily on the date and the then on the user id.
Input: specified date, user id 
Output: User Income submissions on that date.
'''
@payment_bp.route('/dateUserSpecificData', methods=["GET"])
@cross_origin()
def get_date_user_specific_data():

    date, user_id  = convert_to_db_date(request.args.get("date")), request.args.get("userId")

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
@payment_bp.route('/incomeUpdate', methods=["POST"])
@cross_origin()
def update_income_submission():

    ##Get the information from the request body
    user_id, income_arr, chose_date = [request.json[inf_key] for inf_key in ["userId", "incomeArray", "chosenDate"]]

    inc_summary = get_income_summary(income_arr)

    chose_date = convert_to_db_date(chose_date)

    #First update the income per user
    db.collection(u'HistoryData').document(u'UserPayment').collection(user_id).document(chose_date).set(inc_summary)

    #Update the income per date if date is there
    try:
        
        db.collection(u'DateSpecificData').document(chose_date).update({user_id: inc_summary})
    
    except: #Otherwise set the income since it is the first submission for this date.
        
        db.collection(u'DateSpecificData').document(chose_date).set({user_id: inc_summary})
    
    ##Broadcast this event to all of the clients via dynamic backend.
    print(requests.get(url=BASE_URL+"incomeUpdateEvent"))


    return jsonify(True)


'''
Returns the users who are pending to have paid their income otherwise directs them to
get everyone's taxed amount.

'''
@payment_bp.route('/pendingPaymentUsers', methods=["GET"])
@cross_origin()
def get_pending_users():

    date = convert_to_db_date(request.args.get("date"))

    all_users = db.collection('UsefulData').document("AllUsers").get().to_dict()
    
    paid_users_data = db.collection('DateSpecificData').document(date).get().to_dict()
    
    not_paid_users = list(set(all_users.keys()).difference(set(paid_users_data.keys())))

    not_paid_users = [all_users[user_id] for user_id in not_paid_users] #Return the names and not the ids
    
    ##Return tax information if all users have paid.
    if len(not_paid_users) == 0:

        return find_tax_amount(all_users=all_users, date=date)

    return jsonify(format_users_tax(False, not_paid_users=not_paid_users))

    
'''
Finds the tax amount of ASSUMING all users who have submitted their income.
Input: NULL
Output:TODO
'''
@payment_bp.route('/taxAmount', methods=["GET"])
@cross_origin()
def find_tax_amount(all_users=None, date=None):
    
    if all_users is None:

        date = convert_to_db_date(request.args.get("date"))

        all_users = db.collection('UsefulData').document("AllUsers").get().to_dict()
        
    #paid_users_data = db.collection('DateSpecificData').document(date).get().to_dict()
    all_dates = db.collection(u'HistoryData').document("PreviousDates").get().to_dict().keys()

    average_dates = get_average_dates(date, all_dates) #Get the dates to average income over

    #Get the paid data for these dates
    date_pays = [db.collection('DateSpecificData').document(convert_to_db_date(date)).get().to_dict() for date in average_dates]

    income_dict = get_inc_from_average(date_pays, all_users)
    
    #curr_income_dict = get_inc_from_average([db.collection('DateSpecificData').document(convert_to_db_date(date)).get().to_dict()], all_users)

    #final_income_dict = min_tax_dicts(curr_income_dict,income_dict)
    final_income_dict  = income_dict
    
    tax_dict = apply_tax(final_income_dict)
    
    formatted_tax_dict = format_users_tax(True, users_income=final_income_dict, users_tax=tax_dict, all_users=all_users)

    return jsonify(formatted_tax_dict)