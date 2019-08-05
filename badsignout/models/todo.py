from sqlalchemy import Column, Integer, String, Enum, Time, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .value_sets import ACTION

__all__=['Todo']

class Todo(Base):
    __tablename__ = 'todo'

    id_ = Column(Integer, primary_key=True)
    patient = relationship("Patient", back_populates="todos")
    patient_id = Column(Integer, ForeignKey('patients.id_'))
    action = Column(Enum(ACTION))
    target = Column(String)
    when = Column(Time)
    guidance = Column(String)
    freetext = Column(String)
