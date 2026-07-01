from pydantic import BaseModel
from typing import Optional


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    datetime: str


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    datetime: str
    status: str
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None

    class Config:
        from_attributes = True
