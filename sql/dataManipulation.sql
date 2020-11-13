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
VALUES ($date, $chiefComplaint, $diagnosisCode, $procedureCode, $patientID, $providerID, $clinicID, $providerNotes);

--------------------------------------------------------------------------------
-- Selects --

--patients, Select by medical record number
--Query for selecting the medical history of the current patient based on their
--    medicalRecordNumber(PK). '$medicalRecordNumber' used to denote passed variable
--    from backend Python code representing medicalRecordNumber from patient portal
--    Example: $medicalRecordNumber = 1
SELECT patients.medicalRecordNumber, visits.visitDate, visits.chiefComplaint, CONCAT(providers.fname, ' ', providers.lname), visits.diagnosisCode, visits.procedureCode, clinics.clinicID, visits.providerNotes FROM visits
    JOIN patients ON patients.medicalRecordNumber = visits.patient
    JOIN clinics  ON clinics.clinicID = visits.clinic
    JOIN providers ON providers.providerID = visits.provider
    WHERE patients.medicalRecordNumber = $medicalRecordNumber;

--visit, Select by date
--Query for selecting all visits in the system based on the date given. $visitDate used
--  to denote passed variable from backend Python code representing date from provider portal
--  Example: $visitDate = '2020-03-20'
SELECT visits.accountNumber, CONCAT(patients.fname, ' ', patients.lname), visits.chiefComplaint, clinics.clinicName, diagnoses.diagnosisName, procedures.procedureName, CONCAT(providers.fname, ' ', providers.lname), visits.providerNotes FROM visits
    JOIN patients ON patients.medicalRecordNumber = visits.patient
    JOIN clinics  ON clinics.clinicID = visits.clinic
    JOIN diagnoses ON diagnoses.diagnosisCode = visits.diagnosisCode
    JOIN procedures ON procedures.procedureCode = visits.procedureCode
    JOIN providers ON providers.providerID = visits.provider
    WHERE visits.visitDate = $visitDate;


--TODO:
--providers' paitents, Select by provider ID
--clinics, Select by Clinic ID


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
