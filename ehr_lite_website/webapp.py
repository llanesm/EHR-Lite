from flask import Flask, render_template
from flask import request, redirect, url_for
from db_connector.db_connector import connect_to_database, execute_query

import sys

#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!"



@webapp.route('/', methods=['GET', 'POST'])
def home():
    if request.method =='POST':
        print("REQUEST.FORM: ", request.form)

        #if routing to providers
        if request.form['userType'] == "providers":
            print("PRINT: userTYPE:")
            print(request.form['userType'], file=sys.stdout)
            return redirect(url_for('providers')) #pass id number here for redirect

        #if routing to patient
        elif request.form['userType'] =="patient":
            print("PRINT: userTYPE: ")
            print(request.form['userType'], file=sys.stdout)
            return redirect(url_for('patient')) #pass id number here for redirect

        #else reroute back TODO: FIX THIS BREAKS
        else:
            return redirect(url_for('home'))

    return render_template('home.html')

@webapp.route('/patient')
def patient():
    return render_template('patient.html')


@webapp.route('/providers')
def providers():
    #setup for connecting to our database
    db_connection = connect_to_database()

    return render_template('providers.html')
