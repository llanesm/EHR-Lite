from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!"



@webapp.route('/')
def index():
    return render_template('home.html')

@webapp.route('/patients')
def index():
    return render_template('patients.html')

@webapp.route('/providers')
def home():
    #setup for connecting to our database
    db_connection = connect_to_database()

    return render_template('providers.html')
