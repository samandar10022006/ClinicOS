from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Bed(Base):
    __tablename__ = "beds"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String)
    ward = Column(String)
    is_available = Column(Boolean, default=True)
    category = Column(String)  # urgent, chronic, fast
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)

    hospital = relationship("Hospital", back_populates="beds")
    patient = relationship("Patient", back_populates="bed", uselist=False)