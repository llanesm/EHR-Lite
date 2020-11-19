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



"""
Webapp route for handling frontend <--> backend logic of the providers page
"""
@webapp.route('/providers', methods=['GET', 'POST'])
def providers():
    #setup for connecting to our database
    db_connection = connect_to_database()

    #Handler for parsing requests made from submission of one of the forms
    if request.method =='POST':
        print(request.form)

        #Accessing Patient Information in Providers Portal
        #New Patient = providerNewPatient
        if 'providerNewPatient' in request.form:
            print("ADDING PATIENT INFO")
            print("patient_fname:", request.form['newPatientFirstName'])
            patient_fname = request.form['newPatientFirstName']
            print("patient_lname:", request.form['newPatientLastName'])
            patient_lname = request.form['newPatientBirthdate']
            print("patient_birthdate:", request.form['newPatientBirthdate'])
            patient_birthdate = request.form['newPatientBirthdate']
            print("patient_pcp:", request.form['primaryCarePhysician'])
            patient_pcp = request.form['primaryCarePhysician']
            print("patient_pharamcy:", request.form['patientPreferredPharmacy'])
            patient_pharamcy = request.form['patientPreferredPharmacy']

            #TODO: insert into patients SQL statement in DB

        #Discharge Patient = providerDischargePatient
        elif 'providerDischargePatient' in request.form:
            print("DELETEING PATIENT INFO")
            print("patient_mrn: ", request.form['medicalRecordNumber'])
            patient_mrn = request.form['medicalRecordNumber']

            #TODO: delete from patients SQL statement in DB

        #Enter ID of Patient to update = providerLookupPatient
        elif 'providerLookupPatient' in request.form:
            print("LOOKUP PATIENT INFO")
            print("patient_mrn: ", request.form['patientID'])
            patient_mrn = request.form['patientID']

            #TODO: SELECT from patients SQL, populate forms with retuned info
        #Update Patient Information = providerUpdatePatient
        elif 'providerUpdatePatient' in request.form:
            print("UPDATING PATIENT INFO")

            print("patient_fname:", request.form['fname'])
            patient_fname = request.form['fname']
            print("patient_lname:", request.form['lname'])
            patient_lname = request.form['lname']
            print("patient_birthdate:", request.form['birthdate'])
            patient_birthdate = request.form['birthdate']
            print("patient_pcp_num:", request.form['primaryCarePhysicianNum'])
            patient_pcp_num = request.form['primaryCarePhysicianNum']
            print("patient_pharamcy:", request.form['preferredPharmacy'])
            patient_pharamcy = request.form['preferredPharmacy']

            #TODO: UPDATE patients SQL, update patient in DB

        # Access Visit Information in Providers Portal
        #New Visit = providersNewVisit
        elif 'providersNewVisit' in request.form:
            print("ADDING NEW VISIT")

            print("visit_date:", request.form['visitDate'])
            visit_date = request.form['visitDate']
            print("chief_complaint:", request.form['chiefComplaint'])
            chief_complaint = request.form['chiefComplaint']
            print("diagnosis_code:", request.form['diagnosisCode'])
            diagnosis_code = request.form['diagnosisCode']
            print("procedure_code:", request.form['procedureCode'])
            procedure_code = request.form['procedureCode']
            print("patient_mrn:", request.form['patientID'])
            patient_mrn = request.form['patientID']
            print("clinic_id:", request.form['clinicID'])
            clinic_id = request.form['clinicID']
            print("provider_id:", request.form['providerID'])
            provider_id = request.form['providerID']
            print("notes_string:", request.form['providerNotes'])
            notes_string = request.form['providerNotes']

            #TODO: INSERT into visits SQL

        #Enter ID of Visit to update "Enter Account Number" = providersVisitLookup
        elif 'providersVisitLookup' in request.form:
            print("LOOKING UP VISIT")
            print("visit_id: ", request.form['accountNumber'])
            visit_id = request.form['accountNumber']

            #TODO: SELECT visits SQL, insert into form fields bellow

        #Update Visit Information = providersUpdateVisit
        elif 'providersUpdateVisit' in request.form:
            print("UPDATING NEW VISIT")

            print("visit_date:", request.form['visitDate'])
            visit_date = request.form['visitDate']
            print("chief_complaint:", request.form['chiefComplaint'])
            chief_complaint = request.form['chiefComplaint']
            print("diagnosis_code:", request.form['diagnosisCode'])
            diagnosis_code = request.form['diagnosisCode']
            print("procedure_code:", request.form['procedureCode'])
            procedure_code = request.form['procedureCode']
            print("patient_mrn:", request.form['patientID'])
            patient_mrn = request.form['patientID']
            print("clinic_id:", request.form['clinicID'])
            clinic_id = request.form['clinicID']
            print("provider_id:", request.form['providerID'])
            provider_id = request.form['providerID']
            print("notes_string:", request.form['providerNotes'])
            notes_string = request.form['providerNotes']

            #TODO: UPDATE visits SQL

        #Delete Visit = providersDeleteVisit
        elif 'providersDeleteVisit' in request.form:
            print("DELETING VISIT")

            print("visit_id: ", request.form['accountNumber'])
            visit_id = request.form['accountNumber']

            #TODO: DELETE visits SQL

        #View Visists by Date = viewVisits
        elif 'viewVisits' in request.form:
            print("VIEWING VISITS")

            print("visit_date: ", request.form['visitDate'])
            visit_date = request.form['visitDate']

            #TODO: SELECT visits SQL
            query = """SELECT visits.accountNumber, CONCAT(patients.fname, ' ', patients.lname) AS patient, visits.chiefComplaint, clinics.clinicName, diagnoses.diagnosisName, procedures.procedureName, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', visits.providerNotes FROM visits
                        JOIN patients ON patients.medicalRecordNumber = visits.patient
                        JOIN clinics  ON clinics.clinicID = visits.clinic
                        JOIN diagnoses ON diagnoses.diagnosisCode = visits.diagnosisCode
                        JOIN procedures ON procedures.procedureCode = visits.procedureCode
                        JOIN providers ON providers.providerID = visits.provider
                        WHERE visits.visitDate = '{}';""".format(visit_date)
            result = execute_query(db_connection, query)

            row_headers = [x[0] for x in result.description]
            row_variables = result.fetchall() #be careful, this pop's the data as well
            json_data = []
            for row_string in row_variables:
                json_data.append(dict(zip(row_headers, row_string)))
            print("json_data: ", json_data)


            print('test: ', json_data[0]['accountNumber'])
            return render_template('providers.html', visitData=json_data)

        #View Patients of Provider = viewProviderPatients
        elif 'viewProviderPatients' in request.form:
            print("VIEWING PATIENTS")

            print("provider_id: ", request.form['providerID'])
            provider_id = request.form['providerID']

            #TODO: SELECT patients SQL
            # SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', patients.preferredPharmacy FROM patients
            #     JOIN providers ON providers.providerID = patients.primaryCarePhysician
            #     WHERE providers.providerID = $providerID;

        #reload the same providers page after POST
        return redirect(url_for('providers'))
    return render_template('providers.html')




@webapp.route('/admin')
def admin():
    #setup for connecting to our database
    db_connection = connect_to_database()

    return render_template('admin.html')