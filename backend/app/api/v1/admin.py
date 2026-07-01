from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.bed import Bed
from app.models.patient import Patient
from app.schemas.bed import BedCreate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/beds")
def create_bed(
        bed: BedCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    new_bed = Bed(
        room_number=bed.room_number,
        ward=bed.ward,
        category=bed.category,
        hospital_id=bed.hospital_id
    )
    db.add(new_bed)
    db.commit()
    return {"message": "Bed created", "id": new_bed.id}


@router.get("/beds")
def get_beds(db: Session = Depends(get_db)):
    return db.query(Bed).all()


@router.get("/doctors")
def get_doctors(db: Session = Depends(get_db)):
    from app.models.doctor import Doctor
    return db.query(Doctor).all()


@router.get("/dashboard")
def get_admin_dashboard(db: Session = Depends(get_db)):
    total_beds = db.query(Bed).count()
    available_beds = db.query(Bed).filter(Bed.is_available == True).count()
    total_patients = db.query(Patient).count()
    waiting_patients = db.query(Patient).filter(Patient.status == "waiting").count()

    return {
        "total_beds": total_beds,
        "available_beds": available_beds,
        "occupancy_rate": round((total_beds - available_beds) / total_beds * 100, 2) if total_beds else 0,
        "total_patients": total_patients,
        "waiting_patients": waiting_patients,
    }