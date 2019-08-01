from badsignout import Base, Patient, Encounter, Location, Provider, Team
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import date
import pytest
import warnings

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def delete_all():
    session.query(Patient).delete()
    session.query(Encounter).delete()
    session.query(Location).delete()
    session.query(Team).delete()
    session.query(Provider).delete()
    session.commit()

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
    delete_all()

def test_patient():
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
    delete_all()

def test_team():
    pat1 = Patient(name='Charles Test', mrn='12345', sex='m', bday=date(1970, 1, 1))
    pat2 = Patient(name='Bob Test', mrn='12335', sex='m', bday=date(1970, 1, 1))
    intern_ = Provider(name='Stupid intern')
    resident = Provider(name='Bad resident')
    team = Team(name='Foolish Ones')
    team.members = [intern_, resident]
    team.patients = [pat1, pat2]
    intern_.patients = [pat1, pat2]
    resident.patients = [pat1, pat2]
    session.add_all([pat1, pat2, intern_, resident, team])
    session.commit()

    for x in session.query(Team):
        assert len(x.members) == 2
        assert len(x.patients) == 2

        for t in x.members:
            assert t.name in ['Stupid intern', 'Bad resident']

        for t in x.patients:
            assert t.name in ['Charles Test', 'Bob Test']
    for p in session.query(Patient):
        for x in p.providers:
            assert x.name in ['Stupid intern', 'Bad resident']
        assert p.team.name == 'Foolish Ones'

    delete_all()
