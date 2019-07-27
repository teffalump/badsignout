from badsignout import Base, Patient, Encounter, Location
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
import pytest
import warnings

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def test_add_patient():
    patient = Patient(name='Charles Test', mrn='12345', sex='m', bday=date(1970, 1, 1))
    session.add(patient)
    session.commit()

    for x in session.query(Patient):
        n = x.name
        s = x.sex.value
        m = x.mrn
        b = x.bday

    assert n == 'Charles Test'
    assert s == 'male'
    assert m == '12345'
    assert b == date(1970, 1, 1)
    session.query(Patient).delete()
    session.commit()

def test_patient_encounter_location():
    pat = Patient(name='Charles Test', mrn='12345', sex='m', bday=date(1970, 1, 1))
    loc = Location(location='D787-1')
    enc = Encounter(admission=date(2019,7,26))
    enc.locations.append(loc)
    pat.encounters.append(enc)

    session.add_all([pat, loc, enc])
    session.commit()

    for x in session.query(Patient):
        assert x.encounters[0].locations[0].location == 'D787-1'

    for x in session.query(Encounter):
        assert x.patient.name == 'Charles Test'
        assert x.locations[0].location == 'D787-1'

    for x in session.query(Location):
        assert x.encounter.patient.name == 'Charles Test'
        assert x.encounter.admission == date(2019, 7, 26)
