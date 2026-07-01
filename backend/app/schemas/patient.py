from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    full_name: str
    phone: str
    complaint: str
    is_online: bool = False


class PatientUpdate(BaseModel):
    status: str


class PatientResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    complaint: str
    category: str
    status: str
    bed_id: Optional[int] = None
    doctor_id: Optional[int] = None
    estimated_wait: int
    is_online: bool = False
    triage_time: Optional[datetime] = None

    class Config:
        from_attributes = True
