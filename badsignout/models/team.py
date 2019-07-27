from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

__all__=["Team", "Provider"]

patient_assignments_table = Table(
        'patientassignments', Base.metadata,
            Column('provider_id', Integer, ForeignKey("providers.id_"), primary_key=True),
            Column('patient_id', Integer, ForeignKey("patients.id_"), primary_key=True)
        )

class Team(Base):
    __tablename__ = "teams"

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    members = relationship("Provider", back_populates="team")
    patients = relationship("Patient", back_populates="team")

    def __repr__(self):
        return "<Team(name={})>".format(self.name)

class Provider(Base):
    __tablename__ = "providers"

    id_ = Column(Integer, primary_key=True)
    name = Column(String)
    team_id = Column(Integer, ForeignKey("teams.id_"))
    team = relationship("Team", back_populates="members")
    patients = relationship("Patient", secondary=patient_assignments_table, backref="providers")

    def __repr__(self):
        return "<Provider(name={}, team={})>".format(self.name, self.team.name)

