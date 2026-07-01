from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    phone = Column(String, index=True)
    complaint = Column(Text)
    category = Column(String)  # urgent, chronic, fast
    triage_time = Column(DateTime, default=datetime.utcnow)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    status = Column(String, default="waiting")
    estimated_wait = Column(Integer, default=0)  # minutes
    is_online = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    bed = relationship("Bed", back_populates="patient")
    doctor = relationship("Doctor", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")