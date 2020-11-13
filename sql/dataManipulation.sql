-- Inserts --

--paitents
--Query for adding a new patient into the system. '$' used to denote variables
--  that will be data from backend Python
INSERT INTO patients (fname, lname, birthdate, preferredPharmacy, primaryCarePhysician)
    VALUES ($fname, $lname, $birthdate, $preferredPharmacy, $providerIdNumber);

--providers
--Query for adding a new provider into the system. '$' used to denote variables
--  that will be data from backend Python
INSERT INTO providers (fname, lname, licenseType, licenseNumber, specialty, primaryCare)
    VALUES ($fname, $lname, $licenseType, $licenseNumber, $specialty, $primaryCare);

--clinics
--Query for adding a new clinic into the system. '$' used to denote variables
--  that will be data from backend Python
INSERT INTO clinics (clinicName, specialty, providerCapacity, examRooms, primaryCare)
    VALUES ($clinicName, $specialty, $providerCapacity, $examRooms, $primaryCare);

--visits
--Query for adding a new visit into the system. '$' used to denote variables
--  that will be data from backend Python
INSERT INTO visits (visitDate, chiefComplaint, diagnosisCode, procedureCode, patientID, providerID, clinicID, providerNotes)
    VALUES ($visitDate, $chiefComplaint, $diagnosisCode, $procedureCode, $patientID, $providerID, $clinicID, $providerNotes);

--------------------------------------------------------------------------------
-- Selects --

--patients, Select by medicalRecordNumber
--Query for selecting the medical history of the current patient based on their
--    medicalRecordNumber(PK). '$medicalRecordNumber' used to denote passed variable
--    from backend Python code representing medicalRecordNumber from patient portal
--    Example: $medicalRecordNumber = 1
SELECT patients.medicalRecordNumber, visits.visitDate, visits.chiefComplaint, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', visits.diagnosisCode, visits.procedureCode, clinics.clinicID, visits.providerNotes FROM visits
    JOIN patients ON patients.medicalRecordNumber = visits.patient
    JOIN clinics  ON clinics.clinicID = visits.clinic
    JOIN providers ON providers.providerID = visits.provider
    WHERE patients.medicalRecordNumber = $medicalRecordNumber;

--visit, Select by date
--Query for selecting all visits in the system based on the date given. $visitDate used
--  to denote passed variable from backend Python code representing date from provider portal
--  Example: $visitDate = '2020-03-20'
SELECT visits.accountNumber, CONCAT(patients.fname, ' ', patients.lname), visits.chiefComplaint, clinics.clinicName, diagnoses.diagnosisName, procedures.procedureName, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', visits.providerNotes FROM visits
    JOIN patients ON patients.medicalRecordNumber = visits.patient
    JOIN clinics  ON clinics.clinicID = visits.clinic
    JOIN diagnoses ON diagnoses.diagnosisCode = visits.diagnosisCode
    JOIN procedures ON procedures.procedureCode = visits.procedureCode
    JOIN providers ON providers.providerID = visits.provider
    WHERE visits.visitDate = $visitDate;

--providers' paitents, Select by providerID
--Query for selecting all patients of a chosen provider based on the provider's id number.
--  $providerID used to denote passed variable from backend Python code representing the
--  provider's unique id from provider portal
--  Example: $providerID = 1
SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', patients.preferredPharmacy FROM patients
    JOIN providers ON providers.providerID = patients.primaryCarePhysician
    WHERE providers.providerID = $providerID;

--clinics, Select by clinicID
--Query1 (using Visits) for selecting all patients of a chosen clinic based on the clinic's id number.
--  $clinicID used to denote passed variable from backend Python code representing the
--  clinic's unique id from admin portal
--  Example: $clinicID = 1
SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate FROM patients
    JOIN visits ON visits.patient = patients.medicalRecordNumber
    JOIN clinics ON clinics.clinicID = visits.clinic
    WHERE clinics.clinicID = $clinicID;
--Query2 (Using patientsClinics) for selecting all patients of a chosen clinic based on the clinic's id number.
--  $clinicID used to denote passed variable from backend Python code representing the
--  clinic's unique id from admin portal
--  Example: $clinicID = 1
SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate FROM patients
    JOIN patientsClinics ON patientsClinics.patientID = patients.medicalRecordNumber
    JOIN clinics ON clinics.clinicID = patientsClinics.clinicID
    WHERE clinics.clinicID = $clinicID;

--providers, Select by Clinic ID
--Query for selecting all providers of a chosen clinic based on the clinic's id number.
--  $clinicID used to denote passed variable from backend Python code representing the
--  clinic's unique id from admin portal
--  Example: $clinicID = 1
SELECT providers.providerID, providers.fname, providers.lname, providers.licenseType, providers.licenseNumber, providers.specialty, providers.primaryCare FROM providers
    JOIN providersClinics ON providersClinics.providerID = providers.providerID
    WHERE providersClinics.clinicID = $clinicID;

--------------------------------------------------------------------------------
-- Deletes --

--patients, Select by medicalRecordNumber ***NOTE: this table needs ON DELETE CASCADE <------
--Query for deleting a patient from the system based on their unique medicalRecordNumber.
--  Will follow ON DELETE CASCADE referential action. $medicalRecordNumber used to
--  denote passed from backend Python representing user input from provider portal.
--  Example: $medicalRecordNumber = 1
DELETE FROM patients WHERE medicalRecordNumber = $medicalRecordNumber;

--visit, Select by accountNumber
--Query for deleting a visit from the system based on its unique accountNumber.
--  Will follow ON DELETE CASCADE referential action. $accountNumber used to
--  denote passed from backend Python representing user input from provider portal.
--  Example: $accountNumber = 1
DELETE FROM visits WHERE accountNumber = $accountNumber;

--providers, Select by providerID ***NOTE: this table needs ON DELETE CASCADE <-------
--Query for deleting a provider from the system based on their unique providerID.
--  Will follow ON DELETE CASCADE referential action. $providerID used to
--  denote passed from backend Python representing user input from admin portal.
--  Example: $providerID = 1
DELETE FROM providers WHERE providerID = $providerID;

--TODO:
--clinics, Select by clinicID
--Query for deleting a clinic from the system based on its unique clinicID.
--  Will follow ON DELETE CASCADE referential action. $clinicID used to
--  denote passed from backend Python representing user input from admin portal.
--  Example: $providerID = 1
DELETE FROM clinics WHERE clinicID = $providerID;

--------------------------------------------------------------------------------
-- Updates --

--patients, Select by patientID
--Query for updating a patient's information based on their unique medicalRecordNumber.
--  '$' used to denote variables that are passed from backend Python representing user
--  input in the relavent fields.
UPDATE patients SET fname = $fname, lname = $lname, birthdate = $birthdate, primaryCarePhysician = $primaryCarePhysician, preferredPharmacy = $preferredPharmacy
    WHERE medicalRecordNumber = $medicalRecordNumber;

--visit, Select by accountNumber
--Query for updating a visit's information based on their unique accountNumber.
--  '$' used to denote variables that are passed from backend Python representing user
--  input in the relavent fields.
UPDATE visits SET visitDate = $visitDate, chiefComplaint = $chiefComplaint, diagnosisCode = $diagnosisCode, procedureCode = $procedureCode, patient = $patientID, clinic = $clinicID, provider = $providerID, providerNotes = $providerNotes
    WHERE accountNumber = $accountNumber;

--providers, Select by providerID *****NOTE: Add fname to this query and html form? <-----
--Query for updating a provider's information based on their unique providerID.
--  '$' used to denote variables that are passed from backend Python representing user
--  input in the relavent fields.
UPDATE providers SET lname = $fname, licenseType = $licenseType, licenseNumber = $licenseNumber, specialty = $specialty, primaryCare = $primaryCare
    WHERE providerID = $providerID;

--clinics, Select by clinicID *****NOTE: Add clinicName to this query and html form? <-----
--Query for updating a clinics's information based on their unique clinicID.
--  '$' used to denote variables that are passed from backend Python representing user
--  input in the relavent fields.
UPDATE clinics SET specialty = $specialty, providerCapacity = $providerCapacity, examRooms = $examRooms, primaryCare = $primaryCare
    WHERE clinicID = $clinicID;
