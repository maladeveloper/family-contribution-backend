from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials, firestore

##Initialise the firebase database.
cred = credentials.Certificate("secrets/secret_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


##Initialise the application
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.db = db #Add the database to the application context.


##Register the different blueprints
with app.app_context():
    
    ##Basics register
    from src.basics import routes as basic_routes
    app.register_blueprint(basic_routes.basics_bp, url_prefix="/basics")

    ##Payment register
    from src.payment import routes as payment_routes
    app.register_blueprint(payment_routes.payment_bp, url_prefix="/payment")


##Homepage.
@app.route('/')
@cross_origin()
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)