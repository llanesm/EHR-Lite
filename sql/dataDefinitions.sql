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
    `licenseNumber` int(11) UNIQUE,
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
    FOREIGN KEY (`providerID`) REFERENCES providers(`providerID`) ON DELETE CASCADE,
    FOREIGN KEY (`clinicID`) REFERENCES clinics(`clinicID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `patientsClinics` (
    `patientID` int(11),
    `clinicID` int(11),
    FOREIGN KEY (`patientID`) REFERENCES patients(`medicalRecordNumber`) ON DELETE CASCADE,
    FOREIGN KEY (`clinicID`) REFERENCES clinics(`clinicID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Insertions to populate each table.

INSERT INTO clinics (clinicName, specialty, providerCapacity, examRooms, primaryCare)
VALUES ("Max Health Plaza", "Family Medicine", 5, 5, TRUE),
("Max Orthopedics", "Orthopedic Surgery", 2, 2, FALSE);

INSERT INTO providers (fname, lname, licenseType, licenseNumber, specialty, primaryCare)
VALUES ("John", "Smith", "Medical Doctor", 1234, "Family Medicine", TRUE),
("Mary", "Jane", "Medical Doctor", 9482, "Family Medicine", TRUE),
("Martha", "Mathers", "Nurse Practitioner", 2856, "Family Medicine", TRUE),
("Gerald", "Bones", "Medical Doctor", 8546, "Orthopedic Surgery", FALSE),
("Jerry", "Knee", "Physician Assistant", 1112, "Orthopedic Surgery", FALSE);

INSERT INTO patients (fname, lname, birthdate, preferredPharmacy, primaryCarePhysician)
VALUES ("Deborah", "Donahugh", "1972-06-12", "Walgreens",
(SELECT providerID FROM providers WHERE fname="John" AND lname="Smith")),
("Maddie", "Acosta", "1994-04-20", "RiteAid",
(SELECT providerID FROM providers WHERE fname="Mary" AND lname="Jane")),
("Ember", "Bobember", "2018-03-16", "Walmart",
(SELECT providerID FROM providers WHERE fname="Martha" AND lname="Mathers")),
("Bob", "Burgers", "1956-12-10", "Walgreens",
(SELECT providerID FROM providers WHERE fname="John" AND lname="Smith")),
("Rick", "Sanchez", "1950-01-01", "Shmorkazorp Medicinals",
(SELECT providerID FROM providers WHERE fname="Martha" AND lname="Mathers"));

INSERT INTO procedures (procedureCode, procedureName)
VALUES (99214, "General Checkup"),
(29880, "Arthroscopy, knee, surgical; with meniscectomy"),
(11730, "Avulsion of nail plate, partial or complete, simple, single");

INSERT INTO diagnoses (diagnosisCode, diagnosisName)
VALUES ("I10", "Essential Hypertension"),
("E11*", "Type 2 Diabetes Mellitus"),
("L60.0", "Ingrown toenail"),
("S83", "Torn meniscus");

INSERT INTO visits (visitDate, chiefComplaint, diagnosisCode, procedureCode, patient, provider, clinicID, providerNotes)
VALUES ("2020-03-20", "Wellness",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Essential Hypertension"),
    (SELECT procedureCode FROM procedures WHERE procedureName="General Checkup"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Deborah" AND lname="Donahugh" AND birthdate="1972-06-12"),
    (SELECT providerID FROM providers WHERE fname="John" AND lname="Smith"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza"),
    "Deborah got her yearly wellness, hypertension continues to be stable on current medication"),
("2020-07-03", "Wellness",
    NULL,
    (SELECT procedureCode FROM procedures WHERE procedureName="General Checkup"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Maddie" AND lname="Acosta" AND birthdate="1994-04-20"),
    (SELECT providerID FROM providers WHERE fname="Mary" AND lname="Jane"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza"),
    "Maddie got her yearly wellness, continues to be a picture of health"),
("2020-02-18", "Wellness",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Essential Hypertension"),
    (SELECT procedureCode FROM procedures WHERE procedureName="General Checkup"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Ember" AND lname="Bobember" AND birthdate="2018-03-16"),
    (SELECT providerID FROM providers WHERE fname="Martha" AND lname="Mathers"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza"),
    "Ember in today for wellness, vitals higher than normal,
    adjusting medications, prescription sent to Walmart pharmacy"),
("2020-02-18", "Wellness",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Ingrown toenail"),
    (SELECT procedureCode FROM procedures WHERE procedureName="General Checkup"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Bob" AND lname="Burgers" AND birthdate="1956-12-10"),
    (SELECT providerID FROM providers WHERE fname="John" AND lname="Smith"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza"),
    "Mr. Burgers in for his wellness, reports pain in toe, upon examination found nail ingrown with mild
    infection, antibiotics prescription sent to Walgreens, will come back next week for removal"),
("2020-03-18", "Ingrown toenail removal",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Ingrown toenail"),
    (SELECT procedureCode FROM procedures
        WHERE procedureName="Avulsion of nail plate, partial or complete, simple, single"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Bob" AND lname="Burgers" AND birthdate="1956-12-10"),
    (SELECT providerID FROM providers WHERE fname="John" AND lname="Smith"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza"),
    "Inflammation down enough to remove ingrown toenail, no complications"),
("2020-11-09", "Wellness",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Torn meniscus"),
    (SELECT procedureCode FROM procedures WHERE procedureName="General Checkup"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Rick" AND lname="Sanchez" AND birthdate="1950-01-01"),
    (SELECT providerID FROM providers WHERE fname="Martha" AND lname="Mathers"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza"),
    "Rick came in for his wellness. Seems to have a significant limp. Patient
    claimed it to be only giving him mild pain. Upon palpation and subsequent x-ray,
    patient has slight tear in meniscus, will be referred to Max Orthopedics"),
("2020-12-22", "Knee surgery for torn meniscus",
    (SELECT diagnosisCode FROM diagnoses WHERE diagnosisName="Torn meniscus"),
    (SELECT procedureCode FROM procedures WHERE procedureName="Arthroscopy, knee, surgical; with meniscectomy"),
    (SELECT medicalRecordNumber FROM patients WHERE fname="Rick" AND lname="Sanchez" AND birthdate="1950-01-01"),
    (SELECT providerID FROM providers WHERE fname="Gerald" AND lname="Bones"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Orthopedics"),
    "Meniscus cartilage shaved down where tear occurred, no complications.
    Rick will be sent home with a walker and be referred to a week of physical therapy");

INSERT INTO providersClinics (providerID, clinicID)
VALUES ((SELECT providerID FROM providers WHERE fname="John" AND lname="Smith"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT providerID FROM providers WHERE fname="Mary" AND lname="Jane"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT providerID FROM providers WHERE fname="Martha" AND lname="Mathers"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT providerID FROM providers WHERE fname="Gerald" AND lname="Bones"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Orthopedics")),
((SELECT providerID FROM providers WHERE fname="Jerry" AND lname="Knee"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Orthopedics"));

INSERT INTO patientsClinics (patientID, clinicID)
VALUES
((SELECT medicalRecordNumber FROM patients WHERE fname="Deborah" AND lname="Donahugh" AND birthdate="1972-06-12"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT medicalRecordNumber FROM patients WHERE fname="Maddie" AND lname="Acosta" AND birthdate="1994-04-20"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT medicalRecordNumber FROM patients WHERE fname="Ember" AND lname="Bobember" AND birthdate="2018-03-16"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT medicalRecordNumber FROM patients WHERE fname="Bob" AND lname="Burgers" AND birthdate="1956-12-10"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT medicalRecordNumber FROM patients WHERE fname="Rick" AND lname="Sanchez" AND birthdate="1950-01-01")
    (SELECT clinicID FROM clinics WHERE clinicName="Max Health Plaza")),
((SELECT medicalRecordNumber FROM patients WHERE fname="Rick" AND lname="Sanchez" AND birthdate="1950-01-01"),
    (SELECT clinicID FROM clinics WHERE clinicName="Max Orthopedics"));