from flask import Flask, render_template
from flask import request, redirect, url_for
from flask import session
from db_connector.db_connector import connect_to_database, execute_query

import sys
cache= {}
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!"



@webapp.route('/', methods=['GET', 'POST'])
def home():
    #establish sessions keys to prevent keyErrors
    session['visitData'] = 0
    session['patientData'] = 0
    session['providerUpdateVisitID'] = 0
    session['providerUpdateVisitObj'] = 0
    session['patient_mrn'] = 0
    session['providerPatientObj'] = 0
    session['diagnosisOptions'] = 0
    session['procedureOptions'] = 0
    session["patientID"] = 0
    session["clinicOptions"] = 0
    session['patientOptions'] = 0

    session['adminClinicData'] = 0
    session['adminProviderData'] = 0
    session['adminPatientData'] = 0
    session['provider_id'] = 0
    session['adminProviderObj'] = 0
    session['clinic_id'] = 0
    session['adminClinicObj'] = 0

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
            session["patientID"] = request.form['userID']
            return redirect(url_for('patient')) #pass id number here for redirect
        #if routing to admin
        elif request.form['userType'] =="admin":
            print("PRINT: userTYPE: ")
            print(request.form['userType'], file=sys.stdout)
            return redirect(url_for('admin')) #pass id number here for redirect

    return render_template('home.html')



@webapp.route('/patient', methods=['GET', 'POST'])
def patient():
    #setup for connecting to our database
    db_connection = connect_to_database()

    try:
        session['providerOptions']
        session["clinicOptions"]
    except KeyError as error:
        session['providerOptions'] = 0
        session["clinicOptions"] = 0
        print("caught keyerror", error)

    if session["clinicOptions"]:
        clinicOptions = session['clinicOptions']
    else:
        query = "SELECT clinicID, clinicName FROM clinics"
        result = execute_query(db_connection, query)
        row_headers = [x[0] for x in result.description]
        row_variables = result.fetchall()
        json_data = []
        for row_string in row_variables:
            json_data.append(dict(zip(row_headers, row_string)))
        clinicOptions = json_data
        session['clinicOptions'] = clinicOptions

    #patientClinic information
    if session["patientID"]:
        query = """SELECT patients.medicalRecordNumber, CONCAT(patients.fname, ' ', patients.lname) AS 'patientName', clinics.clinicID, clinics.clinicName from patients
                        JOIN patientsClinics ON patientsClinics.patientID = patients.medicalRecordNumber
                        JOIN clinics ON clinics.clinicID = patientsClinics.clinicID
                        WHERE patients.medicalRecordNumber= {};""".format(session["patientID"])
        result = execute_query(db_connection, query)
        row_headers = [x[0] for x in result.description]
        row_variables = result.fetchall() #be careful, this pop's the data as well
        json_data = []
        for row_string in row_variables:
            json_data.append(dict(zip(row_headers, row_string)))
        patientClinics = json_data
        session['patientClinics'] = patientClinics
    else:
        patientClinics = None

    #patient Medical History information
    if session["patientID"]:
        query = """SELECT patients.medicalRecordNumber, visits.visitDate, visits.chiefComplaint, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', diagnoses.diagnosisName, procedures.procedureName, clinics.clinicName, visits.providerNotes FROM visits
                    JOIN patients ON patients.medicalRecordNumber = visits.patient
                    JOIN clinics  ON clinics.clinicID = visits.clinic
                    JOIN providers ON providers.providerID = visits.provider
                    JOIN diagnoses ON diagnoses.diagnosisCode = visits.diagnosisCode
                    JOIN procedures ON procedures.procedureCode = visits.procedureCode
                    WHERE patients.medicalRecordNumber = {};""".format(session["patientID"])
        result = execute_query(db_connection, query)
        row_headers = [x[0] for x in result.description]
        row_variables = result.fetchall() #be careful, this pop's the data as well
        json_data = []
        for row_string in row_variables:
            json_data.append(dict(zip(row_headers, row_string)))
        patientHistory = json_data
        session['patientHistory'] = patientHistory
    else:
        patientHistory = None

    #Provider Options:
    query = "SELECT providerID, CONCAT(fname, ' ', lname) AS 'providerName' FROM providers"
    result = execute_query(db_connection, query)
    row_headers = [x[0] for x in result.description]
    row_variables = result.fetchall()
    json_data = []
    for row_string in row_variables:
        json_data.append(dict(zip(row_headers, row_string)))
    providerOptions = json_data
    session['providerOptions'] = providerOptions

    if request.method =='POST':
        #Accessing Patient Information in Providers Portal
        #New Patient = providerNewPatient
        if 'patientNewPatient' in request.form:
            print("ADDING PATIENT INFO")

            patient_fname = request.form['newPatientFirstName']
            patient_lname = request.form['newPatientLastName']
            patient_birthdate = request.form['newPatientBirthdate']
            patient_pcp = request.form['primaryCarePhysician']
            patient_pharamcy = request.form['patientPreferredPharmacy']

            query = """INSERT INTO patients (fname, lname, birthdate, preferredPharmacy, primaryCarePhysician)
                            VALUES ('{}', '{}', '{}', '{}', {});""".format(patient_fname, patient_lname, patient_birthdate, patient_pharamcy,  patient_pcp)

            execute_query(db_connection, query)

        if 'deletePatientClinicRelation' in request.form:
            print("DELETING PATIENTCLINICS RELATION")

            patient_mrn = request.form['deletePatientClinicRelationPatient']
            clinicID = request.form['deletePatientClinicRelationClinic']
            query = """DELETE FROM patientsClinics WHERE patientsClinics.patientID={} AND patientsClinics.clinicID={}""".format(patient_mrn, clinicID)

            execute_query(db_connection, query)

            #do a refresh query to update the table as well
            query = """SELECT patients.medicalRecordNumber, CONCAT(patients.fname, ' ', patients.lname) AS 'patientName', clinics.clinicID, clinics.clinicName from patients
                        JOIN patientsClinics ON patientsClinics.patientID = patients.medicalRecordNumber
                        JOIN clinics ON clinics.clinicID = patientsClinics.clinicID
                        WHERE patients.medicalRecordNumber= {};""".format(session["patientID"])
            result = execute_query(db_connection, query)
            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall() #be careful, this pop's the data as well
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            patientClinics = json_data
            session['patientClinics'] = patientClinics

        if 'updatePatientClinicRelation' in request.form:
            print("UPDATING PATIENTCLINICS RELATION")

            patient_mrn = request.form['deletePatientClinicRelationPatient']
            clinicID = request.form['updatePatientClinicRelationClinic']
            oldClinicID = request.form['deletePatientClinicRelationClinic']

            preExistingRelation = False
            #check for existing relationship, reject SQL
            for row in session['patientClinics']:
                print("row['clinicID']", row['clinicID'])
                print("clinicID: ", clinicID)
                if int(clinicID) == int(row['clinicID']):
                    preExistingRelation = True
                    print("REJECTING UPDATE <-------------------------------------")
            if not preExistingRelation:
                query = """UPDATE patientsClinics SET clinicID = {}
                                WHERE patientsClinics.patientID={} AND patientsClinics.clinicID={}""".format(clinicID, patient_mrn, oldClinicID)


                execute_query(db_connection, query)

                #do a refresh query to update the table as well
                query = """SELECT patients.medicalRecordNumber, CONCAT(patients.fname, ' ', patients.lname) AS 'patientName', clinics.clinicID, clinics.clinicName from patients
                            JOIN patientsClinics ON patientsClinics.patientID = patients.medicalRecordNumber
                            JOIN clinics ON clinics.clinicID = patientsClinics.clinicID
                            WHERE patients.medicalRecordNumber= {};""".format(session["patientID"])
                result = execute_query(db_connection, query)
                row_headers = [x[0] for x in result.description]
                row_variables = result.fetchall() #be careful, this pop's the data as well
                json_data = []
                for row_string in row_variables:
                    json_data.append(dict(zip(row_headers, row_string)))
                patientClinics = json_data
                session['patientClinics'] = patientClinics

        return render_template('patient.html', clinicOptions=clinicOptions, patientClinics=patientClinics, providerOptions=providerOptions, patientHistory=patientHistory)

    return render_template('patient.html', clinicOptions=clinicOptions, patientClinics=patientClinics, providerOptions=providerOptions, patientHistory=patientHistory)



"""
Webapp route for handling frontend <--> backend logic of the providers page
"""
@webapp.route('/providers', methods=['GET', 'POST'])
def providers():
    #setup for connecting to our database
    db_connection = connect_to_database()

    try:
        session['visitData']
        session['patientData']
        session['providerUpdateVisitID']
        session['providerUpdateVisitObj']
        session['patient_mrn']
        session['providerPatientObj']
        session['diagnosisOptions']
        session['procedureOptions']
        session['providerOptions']
        session['patientOptions']
        session["clinicOptions"]
    except KeyError as error:
        session['patient_mrn'] = 0
        session['providerPatientObj'] = 0
        session['visitData'] = 0
        session['patientData'] = 0
        session['providerUpdateVisitID'] = 0
        session['providerUpdateVisitObj'] = 0
        session['diagnosisOptions'] = 0
        session['procedureOptions'] = 0
        session['providerOptions'] = 0
        session['patientOptions'] = 0
        session["clinicOptions"] = 0
        print("caught keyerror", error)

    #Dynamic Combobox information:
    #Clinic Options
    query = "SELECT clinicID, clinicName FROM clinics"
    result = execute_query(db_connection, query)
    row_headers = [x[0] for x in result.description]
    row_variables = result.fetchall()
    json_data = []
    for row_string in row_variables:
        json_data.append(dict(zip(row_headers, row_string)))
    clinicOptions = json_data
    session['clinicOptions'] = clinicOptions

    #Diagnosis Codes
    query = "SELECT diagnosisCode FROM diagnoses"
    result = execute_query(db_connection, query)
    row_headers = [x[0] for x in result.description]
    row_variables = result.fetchall()
    diagnosisOptions = []
    for row_string in row_variables:
        diagnosisOptions.append(row_string[0])
    session['diagnosisOptions'] = diagnosisOptions

    #Provider ID's and names
    query = "SELECT providerID, CONCAT(fname, ' ', lname) AS 'providerName' FROM providers"
    result = execute_query(db_connection, query)
    row_headers = [x[0] for x in result.description]
    row_variables = result.fetchall()
    json_data = []
    for row_string in row_variables:
        json_data.append(dict(zip(row_headers, row_string)))
    providerOptions = json_data
    session['providerOptions'] = providerOptions

    #Patient ID's and names
    query = "SELECT medicalRecordNumber, CONCAT(fname, ' ', lname) AS 'patientName' FROM patients"
    result = execute_query(db_connection, query)
    row_headers = [x[0] for x in result.description]
    row_variables = result.fetchall()
    json_data = []
    for row_string in row_variables:
        json_data.append(dict(zip(row_headers, row_string)))
    patientOptions = json_data
    session['patientOptions'] = patientOptions

    #Procedures IDs
    query = "SELECT procedureCode FROM procedures"
    result = execute_query(db_connection, query)
    row_headers = [x[0] for x in result.description]
    row_variables = result.fetchall()
    procedureOptions = []
    for row_string in row_variables:
        procedureOptions.append(row_string[0])
    session['procedureOptions'] = procedureOptions

    if session['patient_mrn']:
        patient_mrn = session['patient_mrn']
    else:
        patient_mrn = -1

    if session['providerPatientObj']:
        providerPatientObj = session['providerPatientObj']
    else:
        providerPatientObj = {}

    if session['visitData']:
        visitData = session['visitData']
    else:
        visitData = {}

    if session['patientData']:
        patientData = session['patientData']
    else:
        patientData = {}

    if session['providerUpdateVisitID'] :
        providerUpdateVisitID = session['providerUpdateVisitID']
    else:
        providerUpdateVisitID = -1

    if session['providerUpdateVisitObj']:
        providerUpdateVisitObj = session['providerUpdateVisitObj']
    else:
        providerUpdateVisitObj = {}


    #Handler for parsing requests made from submission of one of the forms
    if request.method =='POST':
        #Accessing Patient Information in Providers Portal
        #New Patient = providerNewPatient
        if 'providerNewPatient' in request.form:
            print("ADDING PATIENT INFO")

            patient_fname = request.form['newPatientFirstName']
            patient_lname = request.form['newPatientLastName']
            patient_birthdate = request.form['newPatientBirthdate']
            patient_pcp = request.form['primaryCarePhysician']
            patient_pharamcy = request.form['patientPreferredPharmacy']

            query = """INSERT INTO patients (fname, lname, birthdate, preferredPharmacy, primaryCarePhysician)
                            VALUES ('{}', '{}', '{}', '{}', {});""".format(patient_fname, patient_lname, patient_birthdate, patient_pharamcy,  patient_pcp)

            execute_query(db_connection, query)

        #Discharge Patient = providerDischargePatient
        elif 'providerDischargePatient' in request.form:
            print("DELETEING PATIENT INFO")

            patient_mrn = request.form['medicalRecordNumber']
            if patient_mrn:
                query = """DELETE FROM patients WHERE medicalRecordNumber = {};""".format(patient_mrn)

                execute_query(db_connection, query)

        #Enter ID of Patient to update = providerLookupPatient
        elif 'providerLookupPatient' in request.form:
            print("LOOKUP PATIENT INFO")

            #save patient id for update query form
            patient_mrn = request.form['patientID']

            if patient_mrn:
                session['patient_mrn'] = patient_mrn

                query = """SELECT medicalRecordNumber, fname, lname, birthdate, primaryCarePhysician, preferredPharmacy FROM patients
                                WHERE medicalRecordNumber = {};""".format(patient_mrn)
                result = execute_query(db_connection, query)

                row_headers = [x[0] for x in result.description]
                row_variables = result.fetchall() #be careful, this pop's the data as well
                json_data = []
                for row_string in row_variables:
                    json_data.append(dict(zip(row_headers, row_string)))

                #save patient info to load into refreshed page
                providerPatientObj = json_data
                session['providerPatientObj'] = providerPatientObj

        #Update Patient Information = providerUpdatePatient
        elif 'providerUpdatePatient' in request.form:
            print("UPDATING PATIENT INFO")

            patient_mrn = session['patient_mrn']

            if patient_mrn:
                #gather form information for SQL query
                patient_fname = request.form['fname']
                patient_lname = request.form['lname']
                patient_birthdate = request.form['birthdate']
                patient_pcp_num = request.form['primaryCarePhysicianNum']
                patient_pharamcy = request.form['preferredPharmacy']

                query = """UPDATE patients SET fname = '{}', lname = '{}', birthdate = '{}', primaryCarePhysician = {}, preferredPharmacy = '{}'
                                WHERE medicalRecordNumber = {};""".format(patient_fname, patient_lname, patient_birthdate, patient_pcp_num, patient_pharamcy, patient_mrn)

                execute_query(db_connection, query)

                #clear the Update Patient Fields in case user wants to update with a new patient
                session['providerPatientObj'] = {}
                providerPatientObj = {}

        # Access Visit Information in Providers Portal
        #New Visit = providersNewVisit
        elif 'providersNewVisit' in request.form:
            print("ADDING NEW VISIT")

            visit_date = request.form['visitDate']
            chief_complaint = request.form['chiefComplaint']
            diagnosis_code = request.form['diagnosisCode']
            procedure_code = request.form['procedureCode']
            patient_mrn = request.form['patientID']
            clinic_id = request.form['clinicID']
            provider_id = request.form['providerID']
            notes_string = request.form['providerNotes']

            query = """INSERT INTO visits (visitDate, chiefComplaint, diagnosisCode, procedureCode, patient, provider, clinic, providerNotes)
                            VALUES ('{}', '{}', '{}', '{}', {}, {}, {}, '{}');
                            """.format(visit_date, chief_complaint, diagnosis_code, procedure_code, patient_mrn, provider_id, clinic_id, notes_string)
            execute_query(db_connection, query)

        #Enter ID of Visit to update "Enter Account Number" = providersVisitLookup
        elif 'providersVisitLookup' in request.form:
            print("LOOKING UP VISIT BEFORE UPDATE")

            #save visit id for update query form
            visit_id = request.form['accountNumber']

            if visit_id:
                session['providerUpdateVisitID'] = visit_id

                query = """SELECT visitDate, chiefComplaint, diagnosisCode, procedureCode, patient, clinic, provider, providerNotes  FROM visits
                            WHERE accountNumber = {};""".format(visit_id)
                result = execute_query(db_connection, query)

                row_headers = [x[0] for x in result.description]
                row_variables = result.fetchall() #be careful, this pop's the data as well
                json_data = []
                for row_string in row_variables:
                    json_data.append(dict(zip(row_headers, row_string)))

                providerUpdateVisitObj = json_data
                session['providerUpdateVisitObj'] = providerUpdateVisitObj

        #Update Visit Information = providersUpdateVisit
        elif 'providersUpdateVisit' in request.form:
            print("UPDATING NEW VISIT")
            account_number = session['providerUpdateVisitID']

            visit_date = request.form['visitDate']
            chief_complaint = request.form['chiefComplaint']
            diagnosis_code = request.form['diagnosisCode']
            procedure_code = request.form['procedureCode']
            patient_mrn = request.form['patientID']
            clinic_id = request.form['clinicID']
            provider_id = request.form['providerID']
            notes_string = request.form['providerNotes']

            query = """UPDATE visits SET visitDate = '{}', chiefComplaint = '{}', diagnosisCode = '{}', procedureCode = '{}', patient = {}, clinic = {}, provider = {}, providerNotes = '{}'
                        WHERE accountNumber = {};""".format(visit_date, chief_complaint, diagnosis_code, procedure_code, patient_mrn, clinic_id, provider_id, notes_string, account_number)
            execute_query(db_connection, query)

            #clear the Update Visit Fields
            session['providerUpdateVisitObj'] = {}
            providerUpdateVisitObj = {}

        #Delete Visit = providersDeleteVisit
        elif 'providersDeleteVisit' in request.form:
            print("DELETING VISIT")
            visit_id = request.form['accountNumber']

            if visit_id:
                query = """DELETE FROM visits WHERE accountNumber = {};""".format(visit_id)
                execute_query(db_connection, query)

        #View Visists by Date = viewVisits
        elif 'providersViewVisits' in request.form:
            print("VIEWING VISITS")

            query = """SELECT visits.accountNumber, CONCAT(patients.fname, ' ', patients.lname) AS patient, visits.chiefComplaint, clinics.clinicName, diagnoses.diagnosisName, procedures.procedureName, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', visits.providerNotes FROM visits
                        JOIN patients ON patients.medicalRecordNumber = visits.patient
                        JOIN clinics  ON clinics.clinicID = visits.clinic
                        LEFT JOIN diagnoses ON diagnoses.diagnosisCode = visits.diagnosisCode
                        JOIN procedures ON procedures.procedureCode = visits.procedureCode
                        JOIN providers ON providers.providerID = visits.provider;"""
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall() #be careful, this pop's the data as well
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            visitData = json_data

            #save for this session in case of further page refreshes
            session['visitData'] = visitData

        #View Patients of Provider = viewProviderPatients
        elif 'viewProviderPatients' in request.form:
            print("VIEWING PATIENTS")

            provider_id = request.form['providerID']

            query = """SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', patients.preferredPharmacy FROM patients
                            JOIN providers ON providers.providerID = patients.primaryCarePhysician
                            WHERE providers.providerID = {};""".format(provider_id)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall() #be careful, this pop's the data as well
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            patientData = json_data

            #save for this session in case of further page refreshes
            session['patientData'] = patientData

        return render_template('providers.html', clinicOptions=clinicOptions, patientOptions=patientOptions, providerOptions=providerOptions, procedureOptions=procedureOptions, diagnosisOptions=diagnosisOptions, patientData=patientData, visitData = visitData, providerUpdateVisitObj = providerUpdateVisitObj, providerPatientObj=providerPatientObj)

    return render_template('providers.html',  clinicOptions=clinicOptions, patientOptions=patientOptions, providerOptions=providerOptions, procedureOptions=procedureOptions, diagnosisOptions=diagnosisOptions, patientData=patientData, visitData = visitData, providerUpdateVisitObj = providerUpdateVisitObj, providerPatientObj=providerPatientObj)


@webapp.route('/admin', methods=['GET', 'POST'])
def admin():
    #setup for connecting to our database
    db_connection = connect_to_database()

    try:
        session['adminClinicData']
        session['adminPatientData']
        session['adminProviderData']
        session['provider_id']
        session['adminProviderObj']
        session['clinic_id']
        session['adminClinicObj']
    except KeyError as error:
        session['adminClinicData'] = 0
        session['adminPatientData'] = 0
        session['adminProviderData'] = 0
        session['provider_id'] = 0
        session['adminProviderObj'] = 0
        session['clinic_id'] = 0
        session['adminClinicObj'] = 0
        print("caught keyerror", error)


    if session['adminPatientData']:
        adminPatientData = session['adminPatientData']
    else:
        adminPatientData = {}

    if session['adminProviderData']:
        adminProviderData = session['adminProviderData']
    else:
        adminProviderData = {}

    if session['provider_id']:
        provider_id = session['provider_id']
    else:
        provider_id = 0

    if session['adminProviderObj']:
        adminProviderObj = session['adminProviderObj']
    else:
        adminProviderObj = {}

    if session['clinic_id']:
        clinic_id = session['clinic_id']
    else:
        clinic_id = 0

    if session['adminClinicObj']:
        adminClinicObj = session['adminClinicObj']
    else:
        adminClinicObj = {}

    if session['adminClinicData']:
        adminClinicData = session['adminClinicData']
    else:
        adminClinicData = {}

    # Handles all button presses
    if request.method == 'POST':

        # Populate clinics table
        if 'viewUpdateClinicTable' in request.form:
            print('LOOKING UP CLINICS')

            query = """SELECT * from clinics"""

            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            adminClinicData = json_data
            session['adminClinicData'] = adminClinicData

            # display true or false on table vs 1 or 0
            for row in adminClinicData:
                if row['primaryCare'] == 1:
                    row['primaryCare'] = True
                else:
                    row['primaryCare'] = False

            session['adminClinicData'] = adminClinicData

        # Add new provider
        elif 'adminNewProvider' in request.form:
            print('ADDING NEW PROVIDER')

            fname = request.form['fname']
            lname = request.form['lname']
            license_type = request.form['licenseType']
            license_number = request.form['licenseNumber']
            specialty = request.form['specialty']
            primary_care = request.form['primaryCare']

            query = """INSERT INTO providers (fname, lname, licenseType, licenseNumber, specialty, primaryCare)
                VALUES ('{}', '{}', '{}', {}, '{}', {});
                """.format(fname, lname, license_type, license_number, specialty, primary_care)

            execute_query(db_connection, query)

        # Add new clinic
        elif 'adminNewClinic' in request.form:
            print('ADDING NEW CLINIC')

            name = request.form['clinicName']
            specialty = request.form['specialty']
            providerCapacity = request.form['providerCapacity']
            examRooms = request.form['examRooms']
            primaryCare = request.form['primaryCare']

            query = """
                    INSERT INTO clinics (clinicName, specialty, providerCapacity, examRooms, primaryCare)
                    VALUES ('{}', '{}', {}, {}, {});
                    """.format(name, specialty, providerCapacity, examRooms, primaryCare)
            execute_query(db_connection, query)

            # Update clinic table view
            query = """SELECT * from clinics"""

            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            adminClinicData = json_data
            session['adminClinicData'] = adminClinicData

            # display true or false on table vs 1 or 0
            for row in adminClinicData:
                if row['primaryCare'] == 1:
                    row['primaryCare'] = True
                else:
                    row['primaryCare'] = False

            session['adminClinicData'] = adminClinicData

        # Remove provider from health system
        elif 'adminDeleteProviderFromSystem' in request.form:
            print('REMOVING PROVIDER FROM SYSTEM')

            provider_fname = request.form['fname']
            provider_lname = request.form['lname']

            query = """DELETE FROM providers WHERE fname = '{}' AND lname = '{}';""".format(provider_fname, provider_lname)

            execute_query(db_connection, query)

        # Remove clinic from health system
        elif 'adminDeleteClinicFromSystem' in request.form:
            print('REMOVING CLINIC FROM SYSTEM')

            clinic_name = request.form['clinicName']

            query = """DELETE FROM clinics WHERE clinicName = '{}';""".format(clinic_name)

            execute_query(db_connection, query)

            # Update clinic table view
            query = """SELECT * from clinics"""

            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            adminClinicData = json_data
            session['adminClinicData'] = adminClinicData

            # display true or false on table vs 1 or 0
            for row in adminClinicData:
                if row['primaryCare'] == 1:
                    row['primaryCare'] = True
                else:
                    row['primaryCare'] = False

            session['adminClinicData'] = adminClinicData

        # Lookup provider to update
        elif 'adminLookupProvider' in request.form:
            print("LOOKING UP PROVIDER INFO")

            # save provider id for update query form
            provider_id = request.form['providerID']
            if provider_id == '':
                provider_id = 0
            session['provider_id'] = provider_id

            query = """SELECT fname, lname, licenseType, licenseNumber, specialty, primaryCare
                        FROM providers WHERE providerID = {};""".format(provider_id)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()  # be careful, this pop's the data as well
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))

            # save provider info to load into refreshed page
            adminProviderObj = json_data
            session['adminProviderObj'] = adminProviderObj

        # Update provider
        elif 'adminUpdateProvider' in request.form:
            print("UPDATING PROVIDER INFO")

            # fetch providerID from lookup form
            provider_id = session['provider_id']

            # data for query
            fname = request.form['fname']
            lname = request.form['lname']
            license_type = request.form['licenseType']
            license_number = request.form['licenseNumber']
            specialty = request.form['specialty']
            primary_care = request.form['primaryCare']

            query = """UPDATE providers SET fname = '{}', lname = '{}', licenseType = '{}', licenseNumber = {},
                    specialty = '{}', primaryCare = {} WHERE providerID = {};
                    """.format(fname, lname, license_type, license_number, specialty, primary_care, provider_id)

            execute_query(db_connection, query)

            # clear the Update Provider fields
            session['adminProviderObj'] = {}
            adminProviderObj = {}

        # Lookup clinic to update
        elif 'adminLookupClinic' in request.form:
            print("LOOKING UP CLINIC INFO")

            # save clinicID for update query form
            clinic_id = request.form['clinicID']
            if clinic_id == '':
                clinic_id = 0
            session['clinic_id'] = clinic_id

            query = """SELECT clinicName, specialty, providerCapacity, examRooms, primaryCare
                        FROM clinics WHERE clinicID = {};""".format(clinic_id)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()  # be careful, this pop's the data as well
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))

            # save clinic info to load into refreshed page
            adminClinicObj = json_data
            session['adminClinicObj'] = adminClinicObj

        # Update clinic
        elif 'adminUpdateClinic' in request.form:
            print("UPDATING CLINIC INFO")

            # fetch clinicID from lookup form
            clinic_id = session['clinic_id']

            # data for query
            clinic_name = request.form['clinicName']
            specialty = request.form['specialty']
            provider_capacity = request.form['providerCapacity']
            exam_rooms = request.form['examRooms']
            primary_care = request.form['primaryCare']

            query = """UPDATE clinics SET clinicName = '{}', specialty = '{}', providerCapacity = {},
                        examRooms = {}, primaryCare = {} WHERE clinicID = {};
                        """.format(clinic_name, specialty, provider_capacity, exam_rooms, primary_care, clinic_id)

            execute_query(db_connection, query)

            # clear the Update Clinic fields
            session['adminClinicObj'] = {}
            adminClinicObj = {}

            # Update clinic table view
            query = """SELECT * from clinics"""

            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            adminClinicData = json_data
            session['adminClinicData'] = adminClinicData

            # display true or false on table vs 1 or 0
            for row in adminClinicData:
                if row['primaryCare'] == 1:
                    row['primaryCare'] = True
                else:
                    row['primaryCare'] = False

            session['adminClinicData'] = adminClinicData

        # Insert procedure
        elif 'adminNewProcedure' in request.form:
            print('ADDING NEW PROCEDURE')

            procedure_code = request.form['procedureCode']
            procedure_name = request.form['procedureName']

            query = """INSERT INTO procedures (procedureCode, procedureName)
                        VALUES ('{}', '{}');""".format(procedure_code, procedure_name)

            execute_query(db_connection, query)

        # Insert diagnosis
        elif 'adminNewDiagnosis' in request.form:
            print('ADDING NEW DIAGNOSIS')

            diagnosis_code = request.form['diagnosisCode']
            diagnosis_name = request.form['diagnosisName']

            query = """INSERT INTO diagnoses (diagnosisCode, diagnosisName)
                        VALUES ('{}', '{}');""".format(diagnosis_code, diagnosis_name)

            execute_query(db_connection, query)

        # Display table of patients that are patients of a given clinic
        elif 'viewPatientsClinicClinicID' in request.form:
            print('LOOKING UP CLINIC')

            if request.form['clinicID'] != '':
                patientsClinicID = request.form['clinicID']
            else:
                patientsClinicID = 0

            query = """SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate,
                        patients.primaryCarePhysician, patients.preferredPharmacy FROM patients
                        JOIN patientsClinics ON patientsClinics.patientID = patients.medicalRecordNumber
                        JOIN clinics ON clinics.clinicID = patientsClinics.clinicID
                        WHERE clinics.clinicID = {};""".format(patientsClinicID)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall()
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            adminPatientData = json_data
            session['adminPatientData'] = adminPatientData

        # Display table of providers that practice at a given clinic
        elif 'viewClinicsProviders' in request.form:
            print('LOOKING UP CLINIC')

            if request.form['clinicID'] != '':
                providersClinicID = request.form['clinicID']
            else:
                providersClinicID = 0

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
            adminProviderData = json_data

            # display true or false on table vs 1 or 0
            for row in adminProviderData:
                if row['primaryCare'] == 1:
                    row['primaryCare'] = True
                else:
                    row['primaryCare'] = False

            session['adminProviderData'] = adminProviderData

        return render_template('admin.html', adminClinicData=adminClinicData, adminPatientData=adminPatientData,
                               adminProviderData=adminProviderData, provider_id=provider_id,
                               adminProviderObj=adminProviderObj, clinic_id=clinic_id, adminClinicObj=adminClinicObj)

    return render_template('admin.html')


webapp.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
