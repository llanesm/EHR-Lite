from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import session
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
        #TODO: 2 patient pages, those who have an existing id (are in the db) and those who need to create a new patient
        elif request.form['userType'] =="patient":
            print("PRINT: userTYPE: ")
            print(request.form['userType'], file=sys.stdout)
            return redirect(url_for('patient')) #pass id number here for redirect

        #TODO: ADD HTML PAGE
        elif request.form['userType'] =="admin":
            print("PRINT: userTYPE: ")
            print(request.form['userType'], file=sys.stdout)
            return redirect(url_for('admin')) #pass id number here for redirect

    return render_template('home.html')

@webapp.route('/patient')
def patient():
    return render_template('patient.html')


@webapp.route('/providers')
def providers():
    #setup for connecting to our database
    db_connection = connect_to_database()

    return render_template('providers.html')

@webapp.route('/admin', methods=['GET', 'POST'])
def admin():
    #setup for connecting to our database
    db_connection = connect_to_database()

    try:
        session['patientData']
        session['providerData']
    except KeyError as error:
        session['patientData'] = 0
        session['providerData'] = 0
        print("caught keyerror", error)

    if session['patientData']:
        patientData = session['patientData']
    else:
        session['patientData'] = {}

    if session['providerData']:
        providerData = session['providerData']
    else:
        providerData = {}

    if request.method == 'POST':

        # Add new provider
        if 'adminNewProvider' in request.form:
            print('ADDING NEW PROVIDER')

            fname = request.form['fname']
            lname = request.form['lname']
            licenseType = request.form['licenseType']
            licenseNumber = request.form['licenseNumber']
            specialty = request.form['specialty']
            primaryCare = request.form['primaryCare']

            query = """
                    INSERT INTO providers (fname, lname, licenseType, licenseNumber, specialty, primaryCare)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}');
                    """.format(fname, lname, licenseType, licenseNumber, specialty, primaryCare)
            execute_query(db_connection, query)

        # Add new clinic
        elif 'adminNewClinic' in request.form:
            print('ADDING NEW CLINIC')

            specialty = request.form['specialty']
            providerCapacity = request.form['providerCapacity']
            examRooms = request.form['examRooms']
            primaryCare = request.form['primaryCare']

            query = """
                    INSERT INTO clinics (clinicName, specialty, providerCapacity, examRooms, primaryCare)
                    VALUES ('{}', '{}', '{}', '{}');
                    """.format(specialty, providerCapacity, examRooms, primaryCare)
            execute_query(db_connection, query)

        # Display table of patients that are patients of a given clinic
        elif 'adminsViewPatients' in request.form:
            print('LOOKING UP CLINIC')

            patientsClinicID = request.form['clinicID']

            query = """SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate
                        FROM patients
                        JOIN visits ON visits.patient = patients.medicalRecordNumber
                        JOIN clinics ON clinics.clinicID = visits.clinic
                        WHERE clinics.clinicID = {};""".format(patientsClinicID)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            patientData = json_data
            session['patientData'] = patientData

        # Display table of providers that practice at a given clinic
        elif 'adminsViewProviders' in request.form:
            print('LOOKING UP CLINIC')

            providersClinicID = request.form['clinicID']

            query = """SELECT providers.providerID, providers.fname, providers.lname, providers.licenseType,
                        providers.licenseNumber, providers.specialty, providers.primaryCare
                        FROM providers
                        JOIN providersClinics ON providersClinics.providerID = providers.providerID
                        WHERE providersClinics.clinicID = {};""".format(providersClinicID)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            providerData = json_data
            session['providerData'] = providerData

        return render_template('admin.html', patientData=patientData, providerData=providerData)

    return render_template('admin.html')

webapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'