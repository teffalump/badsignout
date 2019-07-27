from sqlalchemy import Column, Integer, String, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .value_sets import SEX

__all__=['Patient', 'Encounter', 'Location']


class Patient(Base):
    __tablename__ = 'patients'

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    mrn = Column(String)
    bday = Column(Date)
    sex = Column(Enum(SEX))
    encounters = relationship("Encounter", back_populates="patient")
    team_id = Column(Integer, ForeignKey("teams.id_"))
    team = relationship("Team", back_populates="patients")

    def __repr__(self):
        return "<Patient(fullname={}, MRN={})>".format(self.name, self.mrn)

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
