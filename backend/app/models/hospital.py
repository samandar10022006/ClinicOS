from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    is_active = Column(Boolean, default=True)

    beds = relationship("Bed", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")
    users = relationship("User", back_populates="hospital")
