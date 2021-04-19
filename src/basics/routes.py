from flask import Blueprint, current_app, request, jsonify
from flask_cors import CORS, cross_origin
from .functions import get_refreshed_dates

basics_bp = Blueprint("basics_bp", __name__)

db=current_app.db#Get the initialised database.

@basics_bp.route('/')
@cross_origin()
def hello():
    return "Hello World!"



'''
Initialises the app by passing in logged on user information and setting the dates.
Then returns the user information.
'''
@basics_bp.route('/authId', methods= ["GET"])
@cross_origin()
def authorise_id():

    user_id = request.args.get("userId")

    return jsonify(True if user_id in db.collection('UsefulData').document("AllUsers").get().to_dict() else False)


@basics_bp.route('/init', methods= ["GET"])
@cross_origin()
def init():

    #Get list of previous dates, refresh them and then add them back to database
    all_dates_dict = db.collection(u'HistoryData').document("PreviousDates").get().to_dict()
    
    db.collection(u'HistoryData').document("PreviousDates").set(get_refreshed_dates(all_dates_dict))

    return get_user_info(request.args.get("userId")) #Return user information.



@basics_bp.route('/userInfo', methods=["GET"])
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
@basics_bp.route('/previousDates', methods=["GET"])
@cross_origin()
def get_historic_date_data():

    all_dates = db.collection(u'HistoryData').document("PreviousDates").get().to_dict()

    return jsonify(all_dates)