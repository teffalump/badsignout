from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .value_sets import SEX

__all__=['Patient', 'Encounter', 'Location', 'MedicalHistory', 'HereFor']


class Patient(Base):
    __tablename__ = 'patients'

    id_ = Column(Integer, primary_key=True)
    mrn = Column(String)
    name = Column(String)
    bday = Column(Date)
    sex = Column(Enum(SEX))
    encounters = relationship("Encounter", back_populates="patient")
    reasons = relationship("HereFor", back_populates="patient")
    history = relationship("MedicalHistory", back_populates="patient")
    todos = relationship("Todo", back_populates="patient")
    team_id = Column(Integer, ForeignKey("teams.id_"))
    team = relationship("Team", back_populates="patients")

    def __repr__(self):
        return "<Patient(fullname={}, MRN={})>".format(self.name, self.mrn)

class MedicalHistory(Base):
    __tablename__ = 'medical_history'

    id_ = Column(Integer, primary_key=True)
    condition = Column(String)
    short = Column(String)  #e.g., "HTN"
    suffix = Column(String) #e.g., "s/p thrombectomy"
    prefix = Column(String) #e.g., "recently diagnosed"
    patient = relationship("Patient", back_populates="history")
    patient_id = Column(Integer, ForeignKey('patients.id_'))

    def __repr__(self):
        return "<PMHx(condition={})".format(' '.join([self.prefix, self.condition, self.suffix]))

class HereFor(Base):
    __tablename__ = 'here_for'

    id_ = Column(Integer, primary_key=True)
    reason = Column(String)
    patient = relationship("Patient", back_populates="reasons")
    patient_id = Column(Integer, ForeignKey('patients.id_'))

    def __repr__(self):
        return "<HereFor(reason={})".format(self.reason)

class Encounter(Base):
    __tablename__ = 'encounters'

    id_ = Column(Integer, primary_key=True)
    admission = Column(Date)
    discharge = Column(Date)
    patient = relationship("Patient", back_populates="encounters")
    patient_id = Column(Integer, ForeignKey('patients.id_'))
    locations = relationship("Location", back_populates="encounter")

    def __repr__(self):
        return "<Encounter(patient={}, admission={}, discharge={})>".format(self.patient.name, self.admission, self.discharge)

class Location(Base):
    __tablename__ = 'locations'

    id_ = Column(Integer, primary_key=True)
    location = Column(String)
    encounter_id = Column(Integer, ForeignKey('encounters.id_'))
    encounter = relationship("Encounter", back_populates="locations")

    def __repr__(self):
        return "<Location(bed={}, encounter={})".format(self.location, self.encounter.id_)
