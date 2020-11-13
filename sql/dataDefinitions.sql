-- Tables initialization
DROP TABLE IF EXISTS providersClinics;
DROP TABLE IF EXISTS patientsClinics;

DROP TABLE IF EXISTS visits;
DROP TABLE IF EXISTS procedures;
DROP TABLE IF EXISTS diagnoses;
DROP TABLE IF EXISTS clinics;

DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS providers;

CREATE TABLE `clinics` (
    `clinicID` int(11) AUTO_INCREMENT NOT NULL,
    `clinicName` varchar(255),
    `specialty` varchar(255),
    `providerCapacity` int(11) NOT NULL,
    `examRooms` int(11) NOT NULL,
    `primaryCare` boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (`clinicID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `providers` (
    `providerID` int(11) AUTO_INCREMENT NOT NULL,
    `fname` varchar(255),
    `lname` varchar(255),
    `licenseType` varchar(255),
    `licenseNumber` int(11),
    `specialty` varchar(255),
    `primaryCare` boolean NOT NULL DEFAULT 0,
    PRIMARY KEY (`providerID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `patients` (
    `medicalRecordNumber` int(11) AUTO_INCREMENT NOT NULL,
    `birthdate` date,
    `fname` varchar(255),
    `lname` varchar(255),
    `primaryCarePhysician` int(11),
    `preferredPharmacy` varchar(255),
    PRIMARY KEY (`medicalRecordNumber`),
    FOREIGN KEY (`primaryCarePhysician`) REFERENCES providers(`providerID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `procedures` (
    `procedureCode` varchar(5) NOT NULL,
    `procedureName` varchar(255),
    PRIMARY KEY (`procedureCode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `diagnoses` (
    `diagnosisCode` varchar(6) NOT NULL,
    `diagnosisName` varchar(255),
    PRIMARY KEY (`diagnosisCode`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `visits` (
    `accountNumber` int(11) AUTO_INCREMENT NOT NULL,
    `visitDate` date,
    `chiefComplaint` varchar(255),
    `diagnosisCode` varchar(6),
    `procedureCode` varchar(5),
    `patient` int(11),
    `provider` int(11),
    `providerNotes` varchar(1000),
    `clinic` int(11),
    PRIMARY KEY (`accountNumber`),
    FOREIGN KEY (`diagnosisCode`) REFERENCES diagnoses(`diagnosisCode`),
    FOREIGN KEY (`procedureCode`) REFERENCES procedures(`procedureCode`),
    FOREIGN KEY (`patient`) REFERENCES patients(`medicalRecordNumber`),
    FOREIGN KEY (`provider`) REFERENCES providers(`providerID`),
    FOREIGN KEY (`clinic`) REFERENCES clinics(`clinicID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `providersClinics` (
    `providerID` int(11),
    `clinicID` int(11),
    FOREIGN KEY (`providerID`) REFERENCES providers(`providerID`),
    FOREIGN KEY (`clinicID`) REFERENCES clinics(`clinicID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `patientsClinics` (
    `patientID` int(11),
    `clinicID` int(11),
    FOREIGN KEY (`patientID`) REFERENCES patients(`medicalRecordNumber`),
    FOREIGN KEY (`clinicID`) REFERENCES clinics(`clinicID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insertions to populate each table.

INSERT INTO clinics (clinicName, specialty, providerCapacity, examRooms, primaryCare)
VALUES ("Health Plaza", "Family Medicine", 5, 5, TRUE);

INSERT INTO providers (fname, lname, licenseType, licenseNumber, specialty, primaryCare)
VALUES ("John", "Smith", "Medical Doctor", 1234, "Family Medicine", TRUE);

INSERT INTO patients (fname, lname, birthdate, preferredPharmacy, primaryCarePhysician)
VALUES ("Deborah", "Donahugh", "1972-06-12", "Walgreens",
(SELECT providerID FROM providers WHERE fname="John" AND lname="Smith"));

INSERT INTO procedures (procedureCode, procedureName)
VALUES (99214, "General Checkup");

INSERT INTO diagnoses (diagnosisCode, diagnosisName)
VALUES ("I10", "Essential Hypertension");

INSERT INTO visits (visitDate, chiefComplaint, diagnosisCode, procedureCode, patient, provider, clinicID, providerNotes)
VALUES ("2020-03-20", "Wellness",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Essential Hypertension"),
    (SELECT procedureCode FROM procedures WHERE procedureName="General Checkup"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Deborah" AND lname="Donahugh" AND birthdate="1972-06-12"),
    (SELECT providerID FROM providers WHERE fname="John" AND lname="Smith"),
    (SELECT clinicID FROM clinics WHERE clinicName="Health Plaza"),
    "Deborah got her yearly wellness, hypertension continues to be stable on current medication"
);