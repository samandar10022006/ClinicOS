from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from typing import List

router = APIRouter()


@router.post("/book")
def book_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    new_appointment = Appointment(
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        datetime=appointment.datetime,
        status="scheduled",
    )
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return {"message": "Appointment booked successfully", "id": new_appointment.id}


@router.get("", response_model=List[AppointmentResponse])
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).filter(Appointment.status == "scheduled").all()
    result = []
    for appt in appointments:
        patient = db.query(Patient).filter(Patient.id == appt.patient_id).first()
        doctor = db.query(Doctor).filter(Doctor.id == appt.doctor_id).first()
        result.append(
            AppointmentResponse(
                id=appt.id,
                patient_id=appt.patient_id,
                doctor_id=appt.doctor_id,
                datetime=appt.datetime,
                status=appt.status,
                patient_name=patient.full_name if patient else None,
                doctor_name=doctor.full_name if doctor else None,
            )
        )
    return result
