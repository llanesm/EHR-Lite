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

--patients, Select by medical record number
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

--providers' paitents, Select by provider ID
--Query for selecting all patients of a chosen provider based on the provider's id number.
--  $providerID used to denote passed variable from backend Python code representing the
--  provider's unique id from provider portal
--  Example: $providerID = 1
SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate, CONCAT(providers.fname, ' ', providers.lname) AS 'PCP', patients.preferredPharmacy FROM patients
    JOIN providers ON providers.providerID = patients.primaryCarePhysician
    WHERE providers.providerID = $providerID;

--clinics, Select by Clinic ID
--Query for selecting all patients of a chosen clinic based on the clinic's id number.
--  $clinicID used to denote passed variable from backend Python code representing the
--  clinic's unique id from admin portal
--  Example: $clinicID = 1
SELECT patients.medicalRecordNumber, patients.fname, patients.lname, patients.birthdate FROM patients
    JOIN visits ON visits.patient = patients.medicalRecordNumber
    JOIN clinics ON clinics.clinicID = visits.clinic
    WHERE clinics.clinicID = $clinicID;

--TODO:
--providers, Select by Clinic ID  ****************************************NOTE:Are we still Implementing this ?<---
--Query for selecting all providers of a chosen clinic based on the clinic's id number.
--  $clinicID used to denote passed variable from backend Python code representing the
--  clinic's unique id from admin portal
--  Example: $clinicID = 1
SELECT providers.providerID, providers.fname, providers.lname, providers.licenseType, providers.licenseNumber, providers.specialty, providers.primaryCare FROM providers
    JOIN providersClinics ON providersClinics.providerID = providers.providerID
    WHERE providersClinics.clinicID = $clinicID;

-- Deletes --
--TODO:
--patients, Select by medical record number
--visit, Select by account number
--providers, Select by Provider ID
--clinics, Select by Clinic ID

-- Updates --
--TODO:
--patients, Select by patient ID
--visit, Select by account number
--providers, Select by provider ID
--clinics, Select by Clinic ID
