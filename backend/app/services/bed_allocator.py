from sqlalchemy.orm import Session
from app.models.bed import Bed
from app.models.patient import Patient
from typing import Optional, Dict


def allocate_bed(db: Session, category: str) -> Optional[Bed]:
    """Eng mos bo'sh o'rin topish"""
    bed = db.query(Bed).filter(
        Bed.is_available == True,
        Bed.category == category
    ).first()

    # Agar kategoriya bo'yicha bo'sh bo'lmasa, umumiy bo'sh o'rinni olish
    if not bed:
        bed = db.query(Bed).filter(Bed.is_available == True).first()

    if bed:
        bed.is_available = False
        db.commit()
        db.refresh(bed)
    return bed


def get_wait_time(category: str, db: Session) -> int:
    """Kutish vaqtini hisoblash (daqiqa)"""
    waiting = db.query(Patient).filter(
        Patient.status == "waiting",
        Patient.category == category
    ).count()

    wait_times = {
        "urgent": 5,
        "chronic": 20,
        "fast": 10
    }
    base_time = wait_times.get(category, 15)
    return base_time + (waiting * 5)