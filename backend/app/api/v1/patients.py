from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.patient import Patient
from app.models.bed import Bed
from app.models.doctor import Doctor
from app.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from app.services.triage import classify_complaint
from app.services.bed_allocator import allocate_bed, get_wait_time
from app.services.notification import notification_service
from app.core.websocket import manager
from typing import List, Optional

router = APIRouter()


@router.post("/register", response_model=PatientResponse)
async def register_patient(
        patient: PatientCreate,
        db: Session = Depends(get_db)
):
    # 1. AI tasniflagich
    triage_result = classify_complaint(patient.complaint)
    category = triage_result["category"]

    # 2. O'rin ajratish
    bed = allocate_bed(db, category)

    # 3. Shifokor topish
    doctor = db.query(Doctor).filter(
        Doctor.is_available == True
    ).first()

    # 4. Kutish vaqti
    wait_time = get_wait_time(category, db)

    # 5. Bemor yaratish
    new_patient = Patient(
        full_name=patient.full_name,
        phone=patient.phone,
        complaint=patient.complaint,
        category=category,
        bed_id=bed.id if bed else None,
        doctor_id=doctor.id if doctor else None,
        estimated_wait=wait_time,
        is_online=patient.is_online or False
    )
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    if bed:
        bed.is_available = False
        db.commit()

    if doctor:
        doctor.is_available = False
        db.commit()
    notification_service.add_to_queue(
        new_patient.id,
        f"Bemor {new_patient.full_name} ro'yxatga olindi. Kategoriya: {category}"
    )

    # 7. WebSocket orqali yangilash
    await manager.broadcast({
        "type": "new_patient",
        "data": {
            "id": new_patient.id,
            "name": new_patient.full_name,
            "category": category,
            "wait_time": wait_time
        }
    }, room="public")

    # 8. EMR bilan sinxronizatsiya
    # await emr_integration.sync_patient(new_patient.__dict__)

    return new_patient


@router.get("/waiting", response_model=List[PatientResponse])
def get_waiting_list(db: Session = Depends(get_db)):
    return db.query(Patient).filter(Patient.status == "waiting").order_by(
        Patient.triage_time
    ).all()


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(Patient).count()
    waiting = db.query(Patient).filter(Patient.status == "waiting").count()
    urgent = db.query(Patient).filter(Patient.category == "urgent").count()
    chronic = db.query(Patient).filter(Patient.category == "chronic").count()
    fast = db.query(Patient).filter(Patient.category == "fast").count()
    available_beds = db.query(Bed).filter(Bed.is_available == True).count()

    return {
        "total_patients": total,
        "waiting": waiting,
        "urgent": urgent,
        "chronic": chronic,
        "fast": fast,
        "available_beds": available_beds
    }


@router.put("/{patient_id}/status")
def update_status(
        patient_id: int,
        update: Optional[PatientUpdate] = None,
        status: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    new_status = status or (update.status if update else None)
    if not new_status:
        raise HTTPException(status_code=400, detail="Status is required")

    patient.status = new_status

    if new_status == "treated":
        if patient.bed_id:
            bed = db.query(Bed).filter(Bed.id == patient.bed_id).first()
            if bed:
                bed.is_available = True
        if patient.doctor_id:
            doctor = db.query(Doctor).filter(Doctor.id == patient.doctor_id).first()
            if doctor:
                doctor.is_available = True

    db.commit()
    return {"message": "Status updated"}


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket, room="public")
    try:
        while True:
            data = await websocket.receive_text()
            # Yangiliklarni qayta ishlash
            await manager.broadcast({"type": "update", "data": data}, room="public")
    except WebSocketDisconnect:
        manager.disconnect(websocket, room="public")